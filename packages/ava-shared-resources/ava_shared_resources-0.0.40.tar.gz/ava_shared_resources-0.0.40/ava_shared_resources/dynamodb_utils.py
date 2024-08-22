"""DynamoDB Handler."""

import logging
import time
import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)

# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.Errors.html#Programming.Errors.MessagesAndCodes
# ProvisionedThroughputExceededException is handled by AWS SDK for DynamoDB.
# Server errors with status code 500 are handled by AWS SDK


def get_ttl(days: int):
    """Calculate the Time to Live using given no. of days."""
    return int(time.time()) + (days * 24 * 60 * 60)


def read_items(
    client: boto3.client,
    table_handler: boto3.resource,
    partition_key_attribute: str,
    partition_key_value: str,
    scan_index_forward: bool,
    dynamodb_retries: int,
    dynamodb_retries_delay: int,
) -> list:
    """Read items from DynamoDB Table with retries.

    :param client: AWS dynamodb client instance.
    :param table_handler: The boto3 resource representing the DynamoDB table.
    :param partition_key_attribute: The name of the partition key attribute.
    :param partition_key_value: The value of the partition key attribute to query.
    :param scan_index_forward: If True, the query will be performed in ascending order else in descending order.
    :param dynamodb_retries: Number of retries for reading items from DynamoDB table.
    :param dynamodb_retries_delay: Delay in seconds between retries for reading items from DynamoDB table.

    :return: A list containing all items retrieved from the DynamoDB table, otherwise raise Exception
    """
    retry_attempts = 0
    while retry_attempts < dynamodb_retries:
        try:
            items = _read_items(
                table_handler=table_handler,
                partition_key_attribute=partition_key_attribute,
                partition_key_value=partition_key_value,
                scan_index_forward=scan_index_forward,
            )
            return items

        except client.exceptions.RequestLimitExceeded as rle:
            retry_attempts += 1
            log.error(
                f"Exception during reading items from DynamoDB Table: "
                f"{table_handler.table_name}. RequestLimitExceeded: {rle}"
            )

            if retry_attempts < dynamodb_retries:
                log.info(
                    f"Retrying to read items from DynamoDB Table in "
                    f"{dynamodb_retries_delay} seconds..."
                )
                time.sleep(dynamodb_retries_delay)
            else:
                raise rle

        except ClientError as ce:
            raise Exception(
                f"Exception during reading items from DynamoDB Table: "
                f"{table_handler.table_name}. ClientError: {ce}"
            )
        except Exception as e:
            raise Exception(
                f"Unknown Exception during reading items from DynamoDB Table: {table_handler.table_name}. "
                f"Exception: {e.__class__.__name__} message: {e}"
            )


def _read_items(
    table_handler: boto3.resource,
    partition_key_attribute: str,
    partition_key_value: str,
    scan_index_forward: bool,
):
    """Read items from DynamoDB Table.

    :param table_handler: The boto3 resource representing the DynamoDB table.
    :param partition_key_attribute: The name of the partition key attribute.
    :param partition_key_value: The value of the partition key attribute to query.
    :param scan_index_forward: If True, the query will be performed in ascending order else in descending order.

    :return: A list containing all items retrieved from the DynamoDB table, otherwise raise Exception
    """
    items = list()
    query_count = 1

    start_time = time.time()
    response = table_handler.query(
        KeyConditionExpression=Key(partition_key_attribute).eq(partition_key_value),
        ScanIndexForward=scan_index_forward,
    )
    execution_time = round(time.time() - start_time, 4)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        items.extend(response["Items"])
        log.debug(f"{query_count}st query done. execution time: {execution_time}sec.")

        # Retrieve all items from the paginated result set
        while "LastEvaluatedKey" in response:
            start_time2 = time.time()
            response = table_handler.query(
                KeyConditionExpression=Key(partition_key_attribute).eq(
                    partition_key_value
                ),
                ScanIndexForward=scan_index_forward,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            execution_time = round(time.time() - start_time2, 4)

            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                items.extend(response["Items"])
                query_count = query_count + 1
                log.debug(
                    f"{query_count}th query done. execution time: {execution_time}sec."
                )
            else:
                raise Exception(
                    f"Failed to read items. Received status code: "
                    f"{response['ResponseMetadata']['HTTPStatusCode']}"
                )

    else:
        raise Exception(
            f"Failed to read items. Received status code: "
            f"{response['ResponseMetadata']['HTTPStatusCode']}"
        )

    log.debug(
        f"Total query operations done to retrieve all the {len(items)} items: {query_count}. "
        f"Total execution time: {round(time.time() - start_time, 4)}sec."
    )
    return items


def insert_item(
    client: boto3.client,
    table_handler: boto3.resource,
    item: dict,
    dynamodb_retries: int,
    dynamodb_retries_delay: int,
) -> bool:
    """Insert item into DynamoDB Table with retries.

    :param client: AWS dynamodb client instance.
    :param table_handler: The boto3 resource representing the DynamoDB table.
    :param item: A dictionary representing the item to be inserted into the table.
    :param dynamodb_retries: Number of retries for reading items from DynamoDB table.
    :param dynamodb_retries_delay: Delay in seconds between retries for reading items from DynamoDB table.

    :return: True if the item is successfully inserted, otherwise raise Exception.
    """
    retry_attempts = 0
    while retry_attempts < dynamodb_retries:
        try:
            result = _insert_item(table_handler=table_handler, item=item)
            return result

        except client.exceptions.RequestLimitExceeded as rle:
            retry_attempts += 1
            log.error(
                f"Exception during inserting item into DynamoDB Table: "
                f"{table_handler.table_name}. RequestLimitExceeded: {rle}"
            )

            if retry_attempts < dynamodb_retries:
                log.info(
                    f"Retrying to insert item to DynamoDB Table in "
                    f"{dynamodb_retries_delay} seconds..."
                )
                time.sleep(dynamodb_retries_delay)
            else:
                raise rle

        except ClientError as ce:
            raise Exception(
                f"Exception during inserting item into DynamoDB Table: "
                f"{table_handler.table_name}. ClientError: {ce}"
            )
        except Exception as e:
            raise Exception(
                f"Unknown Exception during inserting item into DynamoDB Table: {table_handler.table_name}. "
                f"Exception: {e.__class__.__name__} message: {e}"
            )


def _insert_item(table_handler: boto3.resource, item: dict) -> bool:
    """Insert item into DynamoDB Table.

    :param table_handler: The boto3 resource representing the DynamoDB table.
    :param item: A dictionary representing the item to be inserted into the table.

    :return: True if the item is successfully inserted, otherwise raise Exception.
    """
    # Convert all the float values to Decimal, as dynamodb does not support float types
    item = json.loads(json.dumps(item), parse_float=Decimal)

    start_time = time.time()
    response = table_handler.put_item(Item=item)
    execution_time = round(time.time() - start_time, 4)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        log.debug(f"Total execution time to insert item: {execution_time}sec. ")
        return True
    else:
        raise Exception(
            f"Failed to insert item. Received status code: "
            f"{response['ResponseMetadata']['HTTPStatusCode']}"
        )
