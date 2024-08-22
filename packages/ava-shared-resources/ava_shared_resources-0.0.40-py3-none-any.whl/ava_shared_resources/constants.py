"""File containing all constants."""

# Application Type for logging
NLU_APPLICATION_TYPE = "AVA_NLU"
CONTENT_PROCESSOR_APPLICATION_TYPE = "Content_Processor"

# Constants related to Collection Mapping File Conversion
EXCEL_FILE_METADATA_COLUMN = "Metadata Value"
EXCEL_FILE_COLLECTION_COLUMN = "Collection"
TOML_FILE_COLLECTION_HEADER = "collections"
TOML_FILE_DEFAULT_HEADER = "default"
TOML_FILE_DEFAULT_COLLECTION_KEY = "default_collection_name"

# Log-related constants
ERROR = "error"
INFO = "info"
DEBUG = "debug"

# White-list events for DynamoDB logging
DYNAMODB_WHITE_LIST_EVENTS = [
    "NLU_CONTROLLER_CONVERSE_RESPONSE",
    "NLU_CONTROLLER_INTENT_DETECTION_RESPONSE",
    "NLU_CONTROLLER_SIMILAR_CONTENT_RESPONSE",
]


# Constants for content accessor.
WEEKLY = "WEEKLY"
DAILY = "DAILY"
KB = "KB"
USERDOCS = "USERDOCS"
VALID_ARTICLE_TYPE = [KB, USERDOCS]
