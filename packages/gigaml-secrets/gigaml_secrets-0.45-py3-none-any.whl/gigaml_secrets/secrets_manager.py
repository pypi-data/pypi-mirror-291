import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class SecretsManager:
    def __init__(self):
        self.client = boto3.client('secretsmanager')

    def get_secret(self, secret_name):
        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
            return get_secret_value_response['SecretString']
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
            return None
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None