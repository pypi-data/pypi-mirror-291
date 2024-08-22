import boto3
import pandas as pd
import io
import re


def read_pickle(s3_uri):
    """
    Reads a pickle file from S3 and returns it as a pandas DataFrame.
    :param s3_uri: S3 URI of the pickle file, e.g. 's3://bucket-name/path/to/file.pkl'
    :return: Pandas DataFrame.
    """
    s3_client = boto3.client("s3")

    bucket_name, key = _parse_s3_uri(s3_uri)
    if not bucket_name or not key:
        print("Invalid S3 URI.")
        return None

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        pickle_data = response["Body"].read()
        df = pd.read_pickle(io.BytesIO(pickle_data))
        return df
    except Exception as e:
        print(f"Error reading pickle file from S3: {e}")
        return None


def write_pickle(df, s3_uri):
    """
    Writes a pandas DataFrame to a pickle file in S3.

    :param df: Pandas DataFrame to write.
    :param aws_access_key_id: AWS access key ID.
    :param aws_secret_access_key: AWS secret access key.
    :param region_name: AWS region name.
    :param s3_uri: S3 URI of the target pickle file, e.g. 's3://bucket-name/path/to/file.pkl'
    """
    s3_client = boto3.client("s3")

    bucket_name, key = _parse_s3_uri(s3_uri)
    if not bucket_name or not key:
        print("Invalid S3 URI.")
        return

    try:
        pickle_buffer = io.BytesIO()
        df.to_pickle(pickle_buffer)
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=pickle_buffer.getvalue())
        print(f"DataFrame successfully written to {s3_uri}")
    except Exception as e:
        print(f"Error writing pickle file to S3: {e}")


def _parse_s3_uri(s3_uri):
    """
    Parses an S3 URI into bucket name and key.

    :param s3_uri: S3 URI of the pickle file, e.g. 's3://bucket-name/path/to/file.pkl'
    :return: tuple of (bucket_name, key).
    """
    match = re.match(r"s3://([^/]+)/(.+)", s3_uri)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None
