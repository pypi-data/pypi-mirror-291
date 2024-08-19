import io
import os
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import grpc

from ._common import (
    BAUPLAN_VERSION,
    _get_or_validate_branch,
    _lifecycle,
    _OperationContainer,
    _print_debug,
)
from ._protobufs.bauplan_pb2 import (
    RunnerInfo,
    TriggerRunRequest,
)
from .state import RunState

JOB_STATUS_FAILED = 'FAILED'
JOB_STATUS_SUCCESS = 'SUCCESS'
JOB_STATUS_CANCELLED = 'CANCELLED'
JOB_STATUS_TIMEOUT = 'TIMEOUT'
JOB_STATUS_REJECTED = 'REJECTED'
JOB_STATUS_UNKNOWN = 'UNKNOWN'


@dataclass
class JobStatus:
    canceled: str = JOB_STATUS_CANCELLED
    cancelled: str = JOB_STATUS_CANCELLED
    failed: str = JOB_STATUS_FAILED
    rejected: str = JOB_STATUS_REJECTED
    success: str = JOB_STATUS_SUCCESS
    timeout: str = JOB_STATUS_TIMEOUT
    unknown: str = JOB_STATUS_UNKNOWN


def _upload_files(
    project_dir: str, temp_dir: str, parameters: Dict[str, Union[str, int, float, bool]]
) -> List[str]:
    upload_files = []

    for file in os.listdir(project_dir):
        if file.endswith(('.py', '.sql', 'requirements.txt', 'bauplan_project.yml')):
            src_path = os.path.join(project_dir, file)
            dst_path = os.path.join(temp_dir, file)
            shutil.copy(src_path, dst_path)
            upload_files.append(dst_path)

    if 'bauplan_project.yml' not in [os.path.basename(file) for file in upload_files]:
        raise Exception('bauplan_project.yml not found in project directory.')

    parameter_entries = [f"    '{key}': {_python_code_str(value)}," for key, value in parameters.items()]
    parameter_entries_str = '\n'.join(parameter_entries)
    internal_py_content = f"""
_user_params = {{
{parameter_entries_str}
}}
"""

    internal_py_path = os.path.join(temp_dir, '_internal.py')
    fp = Path(internal_py_path)
    fp.write_text(internal_py_content, encoding='UTF-8')

    upload_files.append(internal_py_path)

    return upload_files


def _create_trigger_run_request(
    project_dir: str,
    id: str,
    args: Optional[Dict[str, Any]],
    parameters: Dict[str, Union[str, int, float, bool]],
) -> TriggerRunRequest:
    trigger_run_request = TriggerRunRequest(
        module_version=BAUPLAN_VERSION,
        args=args or {},
    )
    if id:
        trigger_run_request.run_id = id
    with tempfile.TemporaryDirectory() as temp_dir:
        upload_files = _upload_files(project_dir, temp_dir, parameters)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in upload_files:
                zipf.write(file, os.path.basename(file))

    trigger_run_request.zip_file = zip_buffer.getvalue()
    trigger_run_request.client_hostname = os.uname().nodename

    return trigger_run_request


def _python_code_str(value: Any) -> str:
    if isinstance(value, str):
        return f"'{value}'"
    if isinstance(value, bool):
        return str(value)
    return repr(value)


def _create_run_state(job_id: str, project_dir: str) -> RunState:
    return RunState(
        job_id=job_id,
        project_dir=project_dir,
    )


def _process_logs(log_stream: grpc.Call, run_state: RunState) -> None:
    for log in log_stream:
        _print_debug(log)
        if _handle_log(log, run_state):
            break


def _handle_log(log: RunnerInfo, run_state: RunState) -> bool:
    runner_event = log.runner_event
    event_type = runner_event.WhichOneof('event')
    run_state.runner_events.append(runner_event)
    if event_type == 'task_start':
        ev = runner_event.task_start
        run_state.tasks_started[ev.task_name] = datetime.now()
    elif event_type == 'task_completion':
        ev = runner_event.task_completion
        run_state.tasks_stopped[ev.task_name] = datetime.now()
    elif event_type == 'job_completion':
        match runner_event.job_completion.WhichOneof('outcome'):
            case 'success':
                run_state.job_status = JOB_STATUS_SUCCESS
            case 'failure':
                run_state.job_status = JOB_STATUS_FAILED
            case 'rejected':
                run_state.job_status = JOB_STATUS_REJECTED
            case 'cancellation':
                run_state.job_status = JOB_STATUS_CANCELLED
            case 'timeout':
                run_state.job_status = JOB_STATUS_TIMEOUT
            case _:
                run_state.job_status = JOB_STATUS_UNKNOWN
        return True
    elif event_type == 'runtime_user_log':
        ev = runner_event.runtime_user_log
        run_state.user_logs.append(ev)
    else:
        _print_debug('Unknown event type')
    return False


class _Run(_OperationContainer):
    @_lifecycle
    def run(
        self,
        project_dir: str,
        id: Optional[str] = None,
        args: Optional[Dict[str, Any]] = None,
        parameters: Optional[Dict[str, Union[str, int, float, bool]]] = None,
        branch_name: Optional[str] | None = None,
    ) -> RunState:
        """
        Run a Bauplan project and return the state of the run. This is the equivalent of
        running through the CLI the ``bauplan run`` command.

        :param project_dir: The directory of the project (where the ``bauplan_project.yml`` file is located).
        :param id: The ID of the run (optional). This can be used to re-run a previous run, e.g., on a different branch.
        :param args: Additional arguments (optional).
        :param parameters: Parameters for templating into SQL or Python models.
        :param parameters: Parameters for templating into SQL or Python models.
        :return: The state of the run.
        """
        if parameters is None:
            parameters = {}

        if args is not None and not isinstance(args, dict):
            raise ValueError('args must be a dict or None')
        if args:
            if branch_name and ('write-branch' in args or 'read-branch' in args):
                raise ValueError(
                    'either pass branch_name or pass args["read-branch"] and args["write-branch"]'
                )
            if any(['write-branch' in args, 'read-branch' in args]):
                if not all(['write-branch' in args, 'read-branch' in args]):
                    raise ValueError(
                        'either pass branch_name or pass args["read-branch"] and args["write-branch"]'
                    )
            if 'write-branch' in args:
                branch_name = args['write-branch']

        client, metadata = self._common.get_commander_and_metadata(args)
        branch_name = _get_or_validate_branch(profile=self.profile, branch_name=branch_name)
        trigger_run_request = _create_trigger_run_request(project_dir, id, args, parameters)
        trigger_run_request.args['write-branch'] = branch_name
        job_id = client.TriggerRun(trigger_run_request, metadata=metadata)
        log_stream: grpc.Call = client.SubscribeLogs(job_id, metadata=metadata)
        run_state = _create_run_state(job_id, project_dir)
        _process_logs(log_stream, run_state)
        return run_state
