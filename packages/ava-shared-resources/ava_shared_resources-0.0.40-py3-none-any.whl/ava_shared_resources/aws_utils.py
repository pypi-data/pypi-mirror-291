"""Utility for managing aws related operation."""

import json
import logging
import os
from io import BytesIO
from typing import Dict, Any, List, Union

import boto3
import pandas as pd
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)


def create_session() -> boto3.Session:
    """
    Create a session which stores configuration state and allows creating service clients and resources.

    :return: session object.
    """
    if "AWS_PROFILE" in os.environ and "AWS_REGION" in os.environ:
        log.info("Creating a session using AWS PROFILE ...")
        return boto3.Session(
            profile_name=os.environ["AWS_PROFILE"], region_name=os.environ["AWS_REGION"]
        )
    elif (
        "AWS_ACCESS_KEY_ID" in os.environ
        and "AWS_SECRET_ACCESS_KEY" in os.environ
        and "AWS_SESSION_TOKEN" in os.environ
        and "AWS_REGION" in os.environ
    ):
        log.info("Creating a session using AWS Credentials ...")
        return boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=os.environ["AWS_SESSION_TOKEN"],
            region_name=os.environ["AWS_REGION"],
        )
    else:
        log.info("Creating a session using default AWS Profile or Role ...")
        return boto3.Session()


def create_client(session: boto3.session, service: str) -> boto3.client:
    """
    Create low-level client from specified session object.

    :param session: configured session object
    :param service: The name of an AWS service, e.g. ‘s3’ or ‘ec2’.
    :return: configured client object
    """
    log.info("Creating aws client ...")
    client = session.client(service)
    return client


def get_file_list_s3(
    s3_client: boto3.client,
    s3_bucket: str,
    s3_input_prefix: str,
    recursive: bool = False,
) -> set:
    """Extract all files inside the specified S3 path.

    :param s3_client: AWS S3 client instance.
    :param s3_bucket: S3 bucket name.
    :param s3_input_prefix: Prefix of the S3 path.
    :param recursive: is recursive approach used.
    :return: A set of file names in the given S3 path.
    """
    try:
        # Ensure the input path has a trailing slash for consistency
        s3_input_prefix = s3_input_prefix.rstrip("/") + "/"

        # Retrieve S3 objects with the specified prefix
        s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_input_prefix)

        # Extract both files and folders from the response
        contents = [entry["Key"] for entry in s3_objects.get("Contents", [])]

        if contents:
            prefix_length = len(s3_input_prefix)
            if recursive:
                file_set = set(
                    # Extract the part of the path after 's3_input_prefix'
                    [
                        path[prefix_length:]
                        for path in contents
                        # Check if the path starts with 's3_input_prefix'
                        if path.startswith(s3_input_prefix) and
                        # Exclude empty string paths (e.g., if 's3_input_prefix' is the entire path)
                        path[prefix_length:] != ""
                    ]
                )
            else:
                file_set = set(
                    # Extract the part of the path after 's3_input_prefix'
                    [
                        path[prefix_length:]
                        for path in contents
                        # Check if the path starts with 's3_input_prefix'
                        if path.startswith(s3_input_prefix) and
                        # Ensure to exclude folders which contains '/'
                        "/" not in path[prefix_length:] and
                        # Exclude empty string paths (e.g., if 's3_input_prefix' is the entire path)
                        path[prefix_length:] != ""
                    ]
                )
            return file_set
        else:
            # Return an empty set if there are no contents
            return set()
    except Exception as e:
        # Handle exceptions (e.g., print an error message or raise a specific exception)
        print(f"Error: {e}")


def get_directory_list_s3(
    s3_client: boto3.client, s3_bucket: str, s3_input_prefix: str
) -> set:
    """Extract all folders inside the specified S3 path.

    :param s3_client: AWS S3 client instance.
    :param s3_bucket: S3 bucket name.
    :param s3_input_prefix: Prefix of the S3 path.
    :return: A set of folder names in the given S3 path.
    """
    try:
        # Ensure the input prefix has a trailing slash for consistency
        s3_input_prefix = s3_input_prefix.rstrip("/") + "/"

        # Retrieve S3 objects with the specified prefix and delimiter
        s3_objects = s3_client.list_objects_v2(
            Bucket=s3_bucket, Prefix=s3_input_prefix, Delimiter="/"
        )

        # Extract common prefixes (directories) from the response
        common_prefixes = s3_objects.get("CommonPrefixes", [])

        if common_prefixes:
            # Generate a set of unique parent folder paths by extracting the part after s3_input_prefix
            # Using '[1].strip('/')' to exclude hierarchical sub-folders
            file_set = set(
                [
                    entry["Prefix"].split(s3_input_prefix)[1].strip("/")
                    for entry in common_prefixes
                    if s3_input_prefix in entry["Prefix"]
                ]
            )
            return file_set
        else:
            # Return an empty set if there are no contents
            return set()
    except Exception as e:
        # Handle exceptions (e.g., print an error message or raise a specific exception)
        print(f"Error: {e}")


def read_file_from_s3(
    s3_client: boto3.client, file_key: str, s3_bucket: str
) -> Union[pd.DataFrame, dict]:
    """
    Read a file from an Amazon S3 bucket using the provided file key, bucket name, and S3 client instance.

    :param s3_client: An instance of the Boto3 S3 client used to interact with the AWS S3 service.
    :param file_key: The unique identifier or key for the file stored in the S3 bucket.
    :param s3_bucket: The name of the S3 bucket from which the file needs to be read.

    :return: DataFrame containing the file data if successful (for CSV),
                                        or a dictionary (for JSON).

    :raises ValueError: If the file format is unsupported or if no objects are found in the specified folder.
    :raises Exception: For any other unexpected errors.
    """
    try:
        if file_key:
            ALLOWED_EXTENSIONS = {"csv", "json"}
            # Extracting file extension from file_key
            file_extension = file_key.split(".")[-1]
            if file_extension not in ALLOWED_EXTENSIONS:
                raise ValueError(f"Unsupported file format found: {file_extension}")
            response = s3_client.get_object(Bucket=s3_bucket, Key=file_key)
            file_data = response["Body"].read()
            if file_extension.lower() == "csv":
                return pd.read_csv(
                    BytesIO(file_data), na_filter=False, encoding="utf-8", dtype=str
                )
            elif file_extension.lower() == "json":
                file_data_str = file_data.decode("utf-8")
                json_data = json.loads(file_data_str)
                return json_data
        else:
            raise ValueError(
                f"No objects were found in the specified folder for bucket {s3_bucket} with key {file_key}."
            )
    except ValueError as ve:
        raise ValueError(
            f"Error while processing file with key {file_key} from bucket {s3_bucket}: {ve}"
        ) from ve
    except Exception as e:
        raise Exception(
            f"An unexpected error occurred while processing file with key {file_key} from bucket {s3_bucket}: {e}"
        ) from e


def s3_get_uri(
    s3_bucket: str,
    prefix: str,
    file: str = "",
    mode: str = "full",
) -> str:
    """
    Create s3 URI of a s3 object.

    :param s3_bucket: name of S3 bucket
    :param prefix: S3 bucket prefix. It's format should be 'folder_name/sub_folder_name'
    :param file: name of remote file in s3 bucket
    :param mode: type of s3 URI either relative s3 URI or full s3 URI
    :return: full or relative s3 URI
    """
    if mode == "full":
        return "s3://" + s3_bucket + "/" + prefix + "/" + file
    elif mode == "relative":
        return prefix + "/" + file


def s3_download_file(
    s3_client: boto3.client,
    s3_bucket: str,
    file_key: str,
    local_file: str,
):
    """
    Download a s3 object.

    :param s3_client: s3 client object
    :param s3_bucket: name of S3 bucket
    :param file_key: s3 object URI
    :param local_file: path to a directory to store downloaded files
    """
    try:
        s3_client.download_file(Bucket=s3_bucket, Key=file_key, Filename=local_file)
    except ClientError as e:
        raise Exception(f"Error while downloading '{file_key}': {e}")


def s3_upload_single_file(
    s3_client: boto3.client,
    s3_bucket: str,
    s3_prefix: str,
    local_dir: str,
    local_file: str,
):
    """
    Upload single file to S3 bucket based on provided data.

    :param s3_client: s3 client object
    :param s3_bucket: name of S3 bucket
    :param s3_prefix: s3 object URI
    :param local_dir: path to a local directory containing local file to upload
    :param local_file: name of local file to upload
    """
    s3_uri = s3_get_uri(s3_bucket, s3_prefix, local_file, "relative")
    try:
        s3_client.upload_file(os.path.join(local_dir, local_file), s3_bucket, s3_uri)

    except ClientError as e:
        raise Exception(f"Error while uploading '{local_file}': {e}")


def put_file_to_s3(
    s3_client: boto3.client,
    s3_bucket: str,
    file_name: str,
    data_to_upload: str,
) -> Dict:
    """
    Upload file to S3 bucket based on provided data.

    :param s3_client: Client for the S3 bucket.
    :param s3_bucket: Name of the S3 bucket.
    :param file_name: Name of the file to be uploaded.
    :param data_to_upload: Data to be uploaded.

    :return: Dict
    """
    try:
        # Upload the file data to S3
        return s3_client.put_object(
            Bucket=s3_bucket, Key=file_name, Body=data_to_upload.encode("utf-8")
        )

    except Exception as e:
        log_description = (
            f"File '{file_name}' uploaded to S3 bucket '{s3_bucket}' Error : {e}"
        )
        raise Exception(log_description)


def delete_file_from_s3(
    s3_client: boto3.client,
    s3_bucket: str,
    file_name: str,
) -> Dict:
    """
    Delete file from s3 bucket.

    :param s3_client: Client for the S3 bucket.
    :param s3_bucket: Name of the S3 bucket.
    :param file_name: Name of the file to be deleted.

    :return: Dict
    """
    try:
        response = s3_client.delete_object(Bucket=s3_bucket, Key=file_name)
        return response
    except Exception as e:
        log_error = (
            f"Failed to delete file '{file_name}' from S3 bucket '{s3_bucket}': {e}"
        )
        raise Exception(log_error)


def delete_message_from_sqs(
    sqs_client: boto3.client,
    msg: Dict[str, Any],
    queue_url: str,
) -> None:
    """Delete a message from an SQS queue.

    :param sqs_client: An instance of the SQS client.
    :param msg: A dictionary representing the message to be deleted.
    :param queue_url: A url of the queue.
    """
    try:
        sqs_client.delete_message(
            QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"]
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "InvalidIdFormat":
            log_description = (
                f"Error: Invalid ID format. Unable to delete message: {msg}."
            )

        elif error_code == "ReceiptHandleIsInvalid":
            log_description = (
                f"Error: Invalid receipt handle. Unable to delete message: {msg}."
            )

        else:
            log_description = (
                f"Unknown Exception occurred while processing message: {msg}. "
                f"Error: {str(e)}"
            )
        raise Exception(log_description)


def push_to_queue(
    sqs_client: boto3.client,
    message_body: str,
    queue_url: str,
    message_group_id: str,
    message_dup_id: str,
) -> Dict:
    """Add a message to a Queue.

    :param sqs_client: An instance of the SQS client.
    :param message_body: A string representing the message to be added to queue.
    :param queue_url: A url of the queue.
    :param message_group_id: An identifier used to group related messages together within an SQS FIFO queue.
    :param message_dup_id: An identifier used to verify the duplicated messages.
    """
    try:
        log_description = (
            f"Message adding to queue with url {queue_url} and body: {message_body}"
        )
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageGroupId=message_group_id,
            MessageDeduplicationId=message_dup_id,
        )
        return response

    except sqs_client.exceptions.InvalidMessageContents as invalid_message_error:
        log_description = (
            f"Error: Invalid Message Contents - {invalid_message_error}. "
            f"Failed processing message body: {message_body}. Please check message content validity."
        )
        raise Exception(log_description)
    except sqs_client.exceptions.UnsupportedOperation as unsupported_operation_error:
        log_description = (
            f"Error: Unsupported Operation - {unsupported_operation_error}. "
            f"Attempted operation not supported for message body: {message_body}."
        )
        raise Exception(log_description)


def get_messages_from_queue(
    sqs_client: boto3.client,
    queue_url: str,
    max_no_of_messages: int,
    visibility_timeout: int,
    wait_time: int,
    attribute_names: List[str] = None,
) -> List[Dict]:
    """Get messages from a Queue.

    :param sqs_client: An instance of the SQS client.
    :param queue_url: A url of the queue.
    :param max_no_of_messages: Maximum number of messages to retrieve at once.
    :param visibility_timeout: Visibility timeout for retrieved messages (in seconds).
    :param wait_time: Maximum time to wait for messages if the queue is empty (in seconds).
    :param attribute_names: A list of attributes that need to be returned along with each message.

    :return: A list of dictionaries representing the retrieved messages.

    """
    attribute_names = attribute_names if attribute_names else ["All"]

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_no_of_messages,
        VisibilityTimeout=visibility_timeout,
        WaitTimeSeconds=wait_time,
        AttributeNames=attribute_names,
    )
    return response.get("Messages") or []


def change_message_visibility(
    sqs_client: boto3.client,
    queue_url: str,
    msg: Dict[str, Any],
    visibility_timeout: int,
) -> None:
    """Change the visibility timeout of a message.

    :param sqs_client: An instance of the SQS client.
    :param msg: A dictionary representing the message.
    :param queue_url: A url of the queue.
    :param visibility_timeout: The new value for the message’s visibility timeout (in seconds)
    """
    try:
        sqs_client.change_message_visibility(
            QueueUrl=queue_url,
            ReceiptHandle=msg["ReceiptHandle"],
            VisibilityTimeout=visibility_timeout,
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "MessageNotInflight":
            log_description = f"Error: Message not inflight. Unable to change visibility timeout of message: {msg}."

        elif error_code == "ReceiptHandleIsInvalid":
            log_description = f"Error: Invalid receipt handle. Unable to change visibility timeout of message: {msg}."

        else:
            log_description = (
                f"Unknown Exception occurred while changing visibility timeout of message: {msg}. "
                f"Error: {str(e)}"
            )
        raise Exception(log_description)
