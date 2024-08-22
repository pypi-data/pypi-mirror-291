"""Response handler.

Script contains uniform format for success and failed responses
"""

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from ava_shared_resources.log_handler import NLULogHandler, CPLogHandler
from ava_shared_resources.configurations.config import Metadata


def handle_response(
    content: object, status_code: int = 200, resp_status: str = "success"
) -> JSONResponse:
    """Handle response.

    :param content: content with returned values
    :param status_code: status_code of request processing
    :param resp_status: status_code of request processing
    :return: response
    """
    return JSONResponse(
        content={
            "content": jsonable_encoder(content),
            "status_code": status_code,
            "status": resp_status,
        },
        status_code=status_code,
    )


def handle_error(
    log_handler: str,
    application_version: str,
    component_name: str,
    component_version: str,
    deployment: str,
    flow: str = None,
    event_name: str = None,
    request_body: dict = None,
    metadata: Metadata = None,
    function_name: str = None,
    message: str = "Server Error",
    exc: Exception = None,
    resp_status: str = "error",
    status_code: int = 500,
    stacktrace: str = None,
) -> JSONResponse:
    """Handle error.

    :param log_handler: Log handler class name to be used to log the error occurred
    :param application_version: Application version where error occurred
    :param component_name: Component where error occurred
    :param component_version: Component version where error occurred
    :param deployment: Deployment where error occurred
    :param flow: Application flow
    :param event_name: Event to log along with error
    :param request_body: Request that was being processed when error occured
    :param metadata: UI metadata corresponding to the request that was being processed when error occured
    :param function_name: Function where error occurred
    :param message: message from exception
    :param exc: exception if present
    :param resp_status: response status
    :param status_code: status_code of request processing
    :param stacktrace: stacktrace if present
    :return: response
    """
    message = "Server Error" if message == "" else message
    exc = str(exc).replace("\n", " ") if exc else None
    stacktrace = stacktrace.replace("\n", " ") if stacktrace else None

    if log_handler == NLULogHandler.__name__:
        NLULogHandler(
            application_version=application_version,
            component=component_name,
            component_version=component_version,
            deployment=deployment,
            flow=flow,
            event_name=event_name,
            request_body=request_body,
            metadata=metadata,
            function_name=function_name,
            level="error",
            message=f"message: {message} status_code: {status_code} response_status: {resp_status} "
            f"exception: {exc} stacktrace: {stacktrace}",
        ).log()
    else:
        CPLogHandler(
            application_version=application_version,
            component=component_name,
            component_version=component_version,
            deployment=deployment,
            flow=flow,
            event_name=event_name,
            request_body=request_body,
            metadata=metadata,
            function_name=function_name,
            level="error",
            message=f"message: {message} status_code: {status_code} response_status: {resp_status} "
            f"exception: {exc} stacktrace: {stacktrace}",
        ).log()

    return handle_response(
        content={"message": message}, status_code=status_code, resp_status=resp_status
    )
