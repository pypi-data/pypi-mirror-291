"""Common shared repository for AVA platform modules."""

from typing import List, Dict, Any, Optional, Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated
from uuid import uuid4

from ava_shared_resources.constants import (
    WEEKLY,
    DAILY,
    VALID_ARTICLE_TYPE,
)


class ClientConfig(BaseModel):
    """Configuration for a client in the AVA platform."""

    deployment: str
    business_unit: str
    language: str

    def __hash__(self):
        """Create a function for Hash calculation.

        Calculates hash value for Client object for possibility to use Client as a key for dictionaries
        """
        return hash((self.deployment, self.business_unit, self.language))

    def __eq__(self, other):
        """Create a function for Equal check.

        Checks the equals the Clients for possibility to use Client as a key for dictionaries
        """
        if isinstance(other, ClientConfig):
            return (self.deployment, self.business_unit, self.language) == (
                other.deployment,
                other.business_unit,
                other.language,
            )
        return False

    def __str__(self):
        """Create a string representation.

        Create string for ClientConfig
        """
        return (
            f"{self.deployment}_{self.business_unit}_{self.language}".replace("-", "_")
            .lower()
            .capitalize()
        )


class ClassifierConfig(BaseModel):
    """Configuration for a classifier in the AVA platform."""

    classification_type: str


class QueryFilterConfig(BaseModel):
    """Configuration for query filters."""

    field_name: str
    field_values: list[str]


class EntityExtraction(BaseModel):
    """Defines the field name specifying the data to be extracted from the index."""

    field_name: Annotated[str, Field(validate_default=True)]

    @field_validator("field_name", mode="before")
    def validate_field_name_str(cls, value):
        """Validate the 'field_name' attribute to ensure it is a non-empty string."""
        if not isinstance(value, str):
            raise ValueError("field_name must be a string.")
        if value.strip() == "":
            raise ValueError("field_name text cannot be empty.")
        return value


class SearchConfig(BaseModel):
    """Configuration for article search in the AVA platform."""

    query_filters: list[QueryFilterConfig]
    display_threshold: int = 20
    seen_ids: list = []


class Query(BaseModel):
    """Configuration for Input query for the Model Manager in the AVA platform."""

    text: Annotated[list[str], Field(validate_default=True)]
    text_log: Annotated[Optional[list[str]], Field(validate_default=True)] = None

    @field_validator("text", mode="before")
    def enforce_list_of_str(cls, value):
        """Validate for text."""
        if isinstance(value, str):
            value = [value]
        elif isinstance(value, list):
            pass
        else:
            raise ValueError("Text must be a string or a list of strings.")
        if any([val.strip() == "" for val in value]):
            raise ValueError("Query text cannot be empty.")
        return value

    @field_validator("text_log", mode="before")
    def validate_text_log(cls, value, values):
        """Validate for text_log."""
        # If text_log is empty then copy value from 'text'
        if not value:
            text_value = values.data.get("text")
            if isinstance(text_value, str):
                return [text_value]
            elif isinstance(text_value, list):
                return text_value[:]
        elif isinstance(value, str):
            return [value]
        elif isinstance(value, list):
            return value
        raise ValueError("text_log must be a string or a list of strings.")


class Metadata(BaseModel):
    """Metadata from UI for each request."""

    sessionId: str
    userId: str
    timestamp: str
    conversation_id: str
    originatingapp: str
    module: str
    correlationId: Annotated[Optional[str], Field(validate_default=True)] = None

    @field_validator("correlationId", mode="before")
    def set_correlation_id(cls, value, values):
        """Generate unique correlationId if not present."""
        return value if value else str(uuid4())


class Content(BaseModel):
    """Content data structure in the AVA platform."""

    data: list[dict]
    mode: str
    article_type: str


class QueryEmbedding(BaseModel):
    """Output from Model Manager for Preprocessing and Vectorizing user-queries in the AVA platform."""

    data: list[list[float]]


class ContentEmbedding(BaseModel):
    """Output from Model Manager for Preprocessing and Vectorizing content in the AVA platform."""

    data: Dict[str, list[float]]


class ContentAccess(BaseModel):
    """Represents access to content with specified attributes."""

    mode: str
    article_type: str
    date: str | None = None

    @field_validator("mode")
    def convert_mode_to_upper(cls, v: str | None) -> str | None:
        """
        Convert the 'mode' parameter to uppercase if not None.

        :param v: Mode value to be converted.
        :type v: str | None

        :return: Uppercase mode value if not None.
        :rtype: str | None
        """
        if v is not None:
            v = v.upper()
        return v

    @field_validator("mode")
    def validate_mode_values(v: str) -> str:
        """
        Validate the 'mode' parameter values.

        :param v: Mode value to be validated.
        :type v: str

        :raises ValueError: If the provided mode is not 'WEEKLY' or 'DAILY'.
        :return: Validated mode value.
        :rtype: str
        """
        if v not in (WEEKLY, DAILY):
            raise ValueError(
                f"Invalid mode. Mode must be {WEEKLY} or {DAILY} (case-insensitive)."
            )
        return v

    @field_validator("article_type")
    def convert_article_type_to_upper(cls, v: str | None) -> str | None:
        """
        Convert the 'article_type' parameter to uppercase if not None.

        :param v: Article type value to be converted.
        :type v: str | None

        :return: Uppercase article type value if not None.
        :rtype: str | None
        """
        if v is not None:
            v = v.upper()
        return v

    @field_validator("article_type")
    def validate_article_type_values(v: str) -> str:
        """
        Validate the 'article_type' parameter values.

        :param v: Article type value to be validated.
        :type v: str

        :raises ValueError: If the provided article type is not 'KB' or 'USERDOCS'.
        :return: Validated article type value.
        :rtype: str
        """
        if v not in VALID_ARTICLE_TYPE:
            raise ValueError(
                (
                    f"Invalid article_type. Article type must be from the following "
                    f"options: {', '.join(VALID_ARTICLE_TYPE)} (case-insensitive)."
                )
            )
        return v


class IntentDetectionOutput(BaseModel):
    """Output from Model Manager for Intent Detection in the AVA platform."""

    model_type: str
    intent_type: Union[str, list]
    confidence: Optional[str] = None
    scores: Dict[str, float]


class ArticleSnippet(BaseModel):
    """Configuration for Input to GenAI service for article summarizations in the AVA platform."""

    articles: list[Dict[str, Any]]


class Conversation(BaseModel):
    """Conversation for follow up questions in the AVA platform."""

    query: str
    generated_text: str


class ConversationHistory(BaseModel):
    """Conversation history for follow up questions in the AVA platform."""

    conversations: List[Conversation]


class ProcessDataQueueMessage(BaseModel):
    """Format for Process-Data-SQS queue messages."""

    bucket_name: str
    export_file_key: str
    content_processor_version: str


class VectorizeDataSQSMessage(BaseModel):
    """Message format for Vectorize-Data-SQS Queue."""

    client_config: ClientConfig
    mode: str
    article_type: str
    file_key: str
    bucket: str
    content_processor_version: str
    nlu_version: str
    deployment_version: str


class IndexDataFileKey(BaseModel):
    """File key for Index-Data-SQS Queue Message."""

    content: str
    vector: str


class IndexDataSQSMessage(BaseModel):
    """Message format for Index-Data-SQS Queue."""

    client_config: ClientConfig
    mode: str
    article_type: str
    file_key: IndexDataFileKey
    bucket: str
    content_processor_version: str
    nlu_version: str
    deployment_version: str


class AnnotatedEntity(BaseModel):
    """Format for annotated entities available in articles."""

    id: str
    label: str
    type: str

    def __eq__(self, other):
        """Compare two AnnotatedEntity objects."""
        return (
            isinstance(other, self.__class__)
            and self.id == other.id
            and self.label == other.label
            and self.type == other.type
        )

    def __hash__(self):
        """Return hash code of object."""
        return hash((self.id, self.label, self.type))


class ProcessedArticle(BaseModel):
    """Validates the processed articles with its types."""

    title: str
    body: str
    collections: List[str]
    url: str
    content: Dict[str, str]
    role: str | None
    annotations: List[AnnotatedEntity]
    article_type: str
    article_number: str | None
    document_id: str
    chunk_id: int
    segment_id: str
    token_count: int
