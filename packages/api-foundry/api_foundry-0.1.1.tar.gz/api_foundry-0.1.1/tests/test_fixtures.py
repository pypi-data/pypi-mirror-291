import boto3
import os
import pytest
import json

from botocore.exceptions import ClientError

from api_foundry.utils.model_factory import ModelFactory
from api_foundry.utils.logger import logger

log = logger(__name__)


@pytest.fixture
def load_model():
    ModelFactory.load_yaml("resources/chinook_api.yaml")


def create_secret_if_not_exists(name, value):
    log.info("creating secret")
    # Create a Secrets Manager client
    client = boto3.client(
        "secretsmanager", endpoint_url="http://localhost.localstack.cloud:4566"
    )

    try:
        # Check if the secret already exists
        response = client.describe_secret(SecretId=name)
        log.info(f"Secret '{name}' already exists!")
        return response["ARN"]
    except client.exceptions.ResourceNotFoundException:
        # Secret does not exist, proceed with creating it
        try:
            # Create the secret
            response = client.create_secret(Name=name, SecretString=value)
            log.info(f"Secret '{name}' created successfully!")
            return response["ARN"]
        except ClientError as e:
            log.error(f"Failed to create secret '{name}': {e}")
            return None
    except ClientError as e:
        log.error(f"Failed to check for secret '{name}': {e}")
        return None


@pytest.fixture
def db_secrets():
    log.info("set secrets variable")
    os.environ["AWS_ENDPOINT_URL"] = "https://localhost.localstack.cloud:4566"
    os.environ["SECRETS"] = json.dumps({"chinook": "postgres/chinook/localstack"})
    create_secret_if_not_exists(
        "postgres/chinook/localstack",
        json.dumps(
            {
                "engine": "postgres",
                "dbname": "chinook_auto_increment",
                "username": "chinook_user",
                "password": "chinook_password",
                "host": "localhost",
            }
        ),
    )
    create_secret_if_not_exists(
        "oracle/chinook",
        json.dumps(
            {
                "engine": "oracle",
                "dbname": "XEPDB1",
                "username": "system",
                "password": "system",
                "host": "localhost",
            }
        ),
    )
