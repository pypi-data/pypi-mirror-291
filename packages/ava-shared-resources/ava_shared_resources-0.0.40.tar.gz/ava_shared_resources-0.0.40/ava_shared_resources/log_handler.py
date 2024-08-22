"""Log handler.

Script contains uniform format for log messages
"""

import os
import logging
from datetime import datetime
from typing import Optional, Union, Dict, List
from copy import deepcopy
from uuid import uuid4

import boto3
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated


from ava_shared_resources.configurations.config import ClientConfig, Metadata
from ava_shared_resources.configurations.gunicorn_config import GunicornConfigModel
from ava_shared_resources import constants as const
from ava_shared_resources.dynamodb_utils import insert_item, get_ttl

logger = logging.getLogger(__name__)
cfg = GunicornConfigModel()


class ConversationLogInformation(BaseModel):
    """Store all necessary information related Conversation Management for analysis purpose."""

    is_genai_enabled: bool
    ui_product: Optional[Union[str, List[str]]] = None
    intent: str
    flow: Optional[str] = None
    entity: Optional[dict] = None
    seen_ids: Optional[list] = None
    actual_question: Optional[list[str]] = None
    get_action: Optional[dict] = None
    show_action: Optional[dict] = None


class GenAITaskLogInformation(BaseModel):
    """Store all necessary information related the Tasks in Gen-AI service response for analysis purpose."""

    model_used: str
    fallback_model_used: str
    time_in_seconds: float
    input_tokens_used: int
    output_tokens_used: int
    completion: str
    content_filter_results: dict


class GenAILogInformation(BaseModel):
    """Store all necessary information related Gen-AI service response for analysis purpose."""

    number_of_llm_calls: int
    total_time_in_seconds: float
    total_input_tokens_used: int
    total_output_tokens_used: int
    rails: Optional[Dict[str, GenAITaskLogInformation]] = None


class LogHandler(BaseModel):
    """Configuration for log entry."""

    message: Annotated[str, Field(validate_default=True)]
    level: Annotated[str, Field(validate_default=True)]
    application_type: str
    application_version: str
    component: str
    component_version: str
    deployment: str

    function_name: Optional[str] = None
    client_config: Optional[ClientConfig] = None
    event_name: Optional[str] = None
    flow: Optional[str] = None
    input_text: Optional[list[str]] = None
    request_body: Optional[dict] = None
    response_body: Optional[Union[dict, list]] = None

    process_id: Annotated[Optional[str], Field(validate_default=True)] = None
    event_id: Annotated[Optional[str], Field(validate_default=True)] = None
    timestamp: Annotated[Optional[str], Field(validate_default=True)] = None
    date: Annotated[Optional[str], Field(validate_default=True)] = None

    # Fields containing information from UI metadata
    metadata: Optional[Metadata] = None
    ui_timestamp: Annotated[Optional[str], Field(validate_default=True)] = None
    user_id: Annotated[Optional[str], Field(validate_default=True)] = None
    session_id: Annotated[Optional[str], Field(validate_default=True)] = None
    correlation_id: Annotated[Optional[str], Field(validate_default=True)] = None
    conversation_id: Annotated[Optional[str], Field(validate_default=True)] = None
    originatingapp: Annotated[Optional[str], Field(validate_default=True)] = None
    ui_module: Annotated[Optional[str], Field(validate_default=True)] = None

    conversation_info: Optional[ConversationLogInformation] = None
    gen_ai_response_info: Optional[GenAILogInformation] = None

    # DynamoDB logging related fields
    dynamodb_retries: Optional[int] = None
    dynamodb_retries_delay: Optional[int] = None
    dynamodb_ttl_attribute: Optional[str] = None
    dynamodb_ttl_value: Optional[int] = None

    @field_validator("event_id", mode="before")
    def set_event_id(cls, value, values):
        """Generate unique event_id for each log."""
        return str(uuid4())

    @field_validator("timestamp", mode="before")
    def set_timestamp(cls, value, values):
        """Set current datetime as timestamp."""
        return datetime.utcnow().isoformat()

    @field_validator("date", mode="before")
    def set_date(cls, value, values):
        """Set current date as date."""
        return datetime.utcnow().strftime("%Y-%m-%d")

    @field_validator("process_id", mode="before")
    def set_process_id(cls, value):
        """Set process_id."""
        if cfg.gunicorn_loglevel == "debug":
            return str(os.getpid())

    @field_validator("message", mode="before")
    def format_message(cls, value):
        """Remove newline characters in message field."""
        return value.replace("\n", " ")

    @field_validator("level", mode="before")
    def validate_level(cls, value):
        """Validate for level."""
        valid_levels = ["info", "error", "debug", "warning"]

        if value not in valid_levels:
            raise ValueError(f"Invalid log level: {value}")
        return value

    @field_validator("ui_timestamp", mode="before")
    def extract_ui_timestamp(cls, v, values, **kwargs):
        """Extract timestamp from metadata."""
        return (
            values.data.get("metadata").timestamp
            if values.data.get("metadata", None)
            else None
        )

    @field_validator("user_id", mode="before")
    def extract_user_id(cls, v, values, **kwargs):
        """Extract user_id from metadata."""
        return (
            values.data.get("metadata").userId
            if values.data.get("metadata", None)
            else None
        )

    @field_validator("session_id", mode="before")
    def extract_session_id(cls, v, values, **kwargs):
        """Extract session_id from metadata."""
        return (
            values.data.get("metadata").sessionId
            if values.data.get("metadata", None)
            else None
        )

    @field_validator("correlation_id", mode="before")
    def extract_correlation_id(cls, v, values, **kwargs):
        """Extract correlation_id from metadata."""
        return (
            values.data.get("metadata").correlationId
            if values.data.get("metadata", None)
            else None
        )

    @field_validator("conversation_id", mode="before")
    def extract_conversation_id(cls, v, values, **kwargs):
        """Extract conversation_id from metadata."""
        return (
            values.data.get("metadata").conversation_id
            if values.data.get("metadata", None)
            else None
        )

    @field_validator("originatingapp", mode="before")
    def extract_originatingapp(cls, v, values, **kwargs):
        """Extract originatingapp from metadata."""
        return (
            values.data.get("metadata").originatingapp
            if values.data.get("metadata", None)
            else None
        )

    @field_validator("ui_module", mode="before")
    def extract_ui_module(cls, v, values, **kwargs):
        """Extract ui_module from metadata."""
        return (
            values.data.get("metadata").module
            if values.data.get("metadata", None)
            else None
        )

    def log(
        self,
        table_handler: Optional[boto3.resource] = None,
        dynamodb_client: Optional[boto3.client] = None,
    ):
        """Create a log entry.

        :param table_handler: The boto3 resource representing the DynamoDB Log table.
        :param dynamodb_client: The boto3 dynamodb client.
        """
        log_functions = {
            "info": logger.info,
            "error": logger.error,
            "debug": logger.debug,
            "warning": logger.warning,
        }
        # Loading extra fields into dictionary
        log_message = jsonable_encoder(self)
        log_message = filter_query(log_message)

        # Removing 'message' field as logger doesn't allow 'extra' fields with certain list of names.
        log_message.pop("message")

        # Removing 'metadata' field as the values are copied to independent fields 'ui_timestamp',
        # 'user_id', and 'session_id'.
        log_message.pop("metadata")

        # Removing fields with value None
        log_message = {
            key: value for key, value in log_message.items() if value is not None
        }

        # Removing fields related to DynamoDB logging settings
        dynamodb_settings_fields = [
            "dynamodb_retries",
            "dynamodb_retries_delay",
            "dynamodb_ttl_attribute",
            "dynamodb_ttl_value",
        ]
        log_message = {
            key: value
            for key, value in log_message.items()
            if key not in dynamodb_settings_fields
        }

        log_function = log_functions.get(self.level)

        log_function(self.message, extra=log_message)

        # Insert log data in DynamoDB table for white-listed events
        if self.event_name in const.DYNAMODB_WHITE_LIST_EVENTS:
            if table_handler:
                log_data = deepcopy(log_message)
                # Add 'message' field that was earlier removed
                log_data["message"] = self.message

                insert_log_data(
                    table_handler=table_handler,
                    dynamodb_client=dynamodb_client,
                    retries=self.dynamodb_retries,
                    retries_delay=self.dynamodb_retries_delay,
                    dynamodb_ttl_attribute=self.dynamodb_ttl_attribute,
                    dynamodb_ttl_value=self.dynamodb_ttl_value,
                    log_data=log_data,
                )
            else:
                logger.warning(
                    f"ERROR: DynamoDB 'table handler' parameter value not present for log with "
                    f"event id: {self.event_id}, event name:{self.event_name} and message: {self.message}. "
                    f"Therefore, the event is not be logged in DynamoDB."
                )


def filter_query(log_message: dict):
    """Mask 'text' in query object with empty string in request_body if present.

    :param log_message: log message
    :return: filtered log message
    """
    if log_message.get("request_body", None):
        if log_message["request_body"].get("query", None):
            log_message["request_body"]["query"]["text"] = [""]

    return log_message


def insert_log_data(
    table_handler: boto3.resource,
    dynamodb_client: boto3.client,
    retries: int,
    retries_delay: int,
    dynamodb_ttl_attribute: str,
    dynamodb_ttl_value: int,
    log_data: dict,
):
    """Insert log into DynamoDB table.

    :param table_handler: The boto3 resource representing the DynamoDB Log table.
    :param dynamodb_client: AWS dynamodb client instance.
    :param retries: Number of retries for reading items from DynamoDB table.
    :param retries_delay: Delay in seconds between retries for reading items from DynamoDB table.
    :param dynamodb_ttl_attribute: TTL attribute name configured in DynamoDB table.
    :param dynamodb_ttl_value: TTL attribute value in days to used in DynamoDB table.
    :param log_data: A dictionary representing the log item to be inserted into the DynamoDB Log table.
    """
    logger.info("Inserting log into DynamoDB...")
    # Add TTL field
    log_data[dynamodb_ttl_attribute] = get_ttl(days=dynamodb_ttl_value)

    insert_item(
        client=dynamodb_client,
        table_handler=table_handler,
        item=log_data,
        dynamodb_retries=retries,
        dynamodb_retries_delay=retries_delay,
    )
    logger.info("Inserted log into DynamoDB...")


class NLULogHandler(LogHandler):
    """Configuration for log entry on NLU components."""

    application_type: str = const.NLU_APPLICATION_TYPE

    def log(
        self,
        table_handler: Optional[boto3.resource] = None,
        dynamodb_client: Optional[boto3.client] = None,
    ):
        """Create a log entry.

        :param table_handler: The boto3 resource representing the DynamoDB Log table.
        :param dynamodb_client: The boto3 dynamodb client.
        """
        super(NLULogHandler, self).log(
            table_handler=table_handler,
            dynamodb_client=dynamodb_client,
        )


class CPLogHandler(LogHandler):
    """Configuration for log entry on Content Processor components."""

    application_type: str = const.CONTENT_PROCESSOR_APPLICATION_TYPE

    def log(
        self,
        table_handler: Optional[boto3.resource] = None,
        dynamodb_client: Optional[boto3.client] = None,
    ):
        """Create a log entry.

        :param table_handler: The boto3 resource representing the DynamoDB Log table.
        :param dynamodb_client: The boto3 dynamodb client.
        """
        super(CPLogHandler, self).log(
            table_handler=table_handler,
            dynamodb_client=dynamodb_client,
        )
