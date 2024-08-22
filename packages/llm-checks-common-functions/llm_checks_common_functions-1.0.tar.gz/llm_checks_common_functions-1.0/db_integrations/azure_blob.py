from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO
from datetime import datetime

class AzureBlobStorage:
    def __init__(self, connection_string, container_name):
        """Initialize the Azure Blob Storage client."""
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        

    def ensure_container_exists(self):
        """Ensure the container exists, and create it if it does not."""
        try:
            if not self.container_client.exists():
                self.container_client.create_container()
                print(f"Container '{self.container_client.container_name}' created.")
        except Exception as e:
            print(f"Failed to create container: {e}")

    def upload_blob(self, blob_name, df):
        """Upload a DataFrame as an Excel blob to the container."""
        try:
            self.ensure_container_exists()
            current_date = datetime.now().strftime("%d-%m-%Y")
            blob_path = f"{current_date}/{blob_name}"
            
            # Convert DataFrame to Excel
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            excel_buffer.seek(0)
            
            # Upload the Excel file to Azure Blob Storage
            blob_client = self.container_client.get_blob_client(blob=blob_path)
            blob_client.upload_blob(excel_buffer, overwrite=True)
            print(f"DataFrame uploaded to {blob_path} in container {self.container_client.container_name}.")
        except Exception as e:
            print(f"Failed to upload DataFrame to Blob Storage: {e}")

    def download_blob(self, blob_name):
        """Download an Excel blob from the container and return it as a DataFrame."""
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            
            # Check if blob exists
            if not blob_client.exists():
                print(f"Blob '{blob_name}' does not exist in container '{self.container_client.container_name}'.")
                return None
            
            # Download the blob
            blob_data = blob_client.download_blob()
            blob_content = blob_data.readall()
            
            # Load the Excel file into a DataFrame
            excel_data = BytesIO(blob_content)
            df = pd.read_excel(excel_data)
            
            return df
        except Exception as e:
            print(f"Failed to download or read the blob: {e}")
            return None

    def delete_blob(self, blob_name):
        """Delete a blob from the container."""
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.delete_blob()
            print("Blob deleted successfully.")
        except Exception as e:
            print(f"Failed to delete blob: {e}")

if __name__=="main":
    storage = AzureBlobStorage("your_connection_string", "your_container_name")
    storage.upload_blob("your_blob_name.xlsx", your_dataframe)
    df = storage.download_blob("your_blob_name.xlsx")
    storage.delete_blob("your_blob_name.xlsx")
