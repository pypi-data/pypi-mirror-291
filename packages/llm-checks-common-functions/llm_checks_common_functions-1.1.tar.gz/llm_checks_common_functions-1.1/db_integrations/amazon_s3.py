import boto3
import pandas as pd
from io import BytesIO

class S3DataHandler:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def download_excel_as_df(self, bucket_name, s3_key):
        """
        Download an Excel file from an S3 bucket and return it as a DataFrame.

        :param bucket_name: The name of the S3 bucket.
        :param s3_key: The key (path) of the Excel file in the S3 bucket.
        :return: A pandas DataFrame.
        """
        response = self.s3.get_object(Bucket=bucket_name, Key=s3_key)
        content = response['Body'].read()
        return pd.read_excel(BytesIO(content))

    def upload_df_as_excel(self, df, bucket_name, s3_key):
        """
        Upload a DataFrame as an Excel file to an S3 bucket.

        :param df: The pandas DataFrame to upload.
        :param bucket_name: The name of the S3 bucket.
        :param s3_key: The key (path) where the Excel file will be stored in the S3 bucket.
        """
        with BytesIO() as buffer:
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            self.s3.upload_fileobj(buffer, bucket_name, s3_key)

# Example usage:
if __name__ == "__main__":
    aws_access_key_id = "AKIA4Z4SEB26J5B2GZEN"
    aws_secret_access_key = "wC8+n3HtYD0AZfE9YiSOVjsHe1YjF2f1kBETrPLI"
    region_name = "us-west-2"

    handler = S3DataHandler(aws_access_key_id, aws_secret_access_key, region_name)

    # Download Excel as DataFrame
    bucket_name = "door-dash"
    s3_key_download = 'dd-templates/Bacon.xlsx'
    df = handler.download_excel_as_df(bucket_name, s3_key_download)
    print(df)

    # # Upload DataFrame as Excel
    # s3_key_upload = 'path/to/upload/excel/file.xlsx'
    # handler.upload_df_as_excel(df, bucket_name, s3_key_upload)
