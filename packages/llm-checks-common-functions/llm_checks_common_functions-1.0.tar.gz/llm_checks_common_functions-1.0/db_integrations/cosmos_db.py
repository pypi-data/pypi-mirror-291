import uuid
import pandas as pd
from datetime import date
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import json
import os

class CosmosDBHandler:
    def __init__(self, connection_string):
        self.client = CosmosClient.from_connection_string(connection_string)

    def upload_data(self, df, database_name='loop-redteam', container_name='red-team-1', batch_id='batch_001'):
        try:
            if 'id' not in df.columns:
                df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]

            df['batch_id'] = batch_id
            df['date'] = date.today()

            database = self.client.create_database_if_not_exists(id=database_name)
            container = database.create_container_if_not_exists(
                id=container_name,
                partition_key=PartitionKey(path="/HitID"),
                offer_throughput=400
            )

            json_data = df.to_json(orient='records')
            for item in json.loads(json_data):
                container.create_item(body=item)

        except Exception as e:
            print(f"Error uploading data: {e}")

    def download_data(self, database_name, container_name):
        try:
            database = self.client.get_database_client(database_name)
            container = database.get_container_client(container_name)
            query = "SELECT * FROM c"
            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))

            df_out = pd.DataFrame(items)
            return df_out

        except Exception as e:
            print(f"Error downloading data: {e}")

    def update_data(self, df, database_name, container_name):
        try:
            database = self.client.get_database_client(database_name)
            container = database.get_container_client(container_name)

            if container is None:
                raise ValueError(f"Container {container_name} does not exist in database {database_name}")

            df=df[[col for col in df.columns if not col.startswith('_')]]

            existing_items = list(container.query_items(
                query="SELECT * FROM c",
                enable_cross_partition_query=True
            ))

            existing_ids = {item['id'] for item in existing_items}

            for _, row in df.iterrows():
                item = row.to_json()
                item=json.loads(item)
                if 'id' in item and item['id'] in existing_ids:
                    container.upsert_item(body=item)
                else:
                    if 'id' not in item:
                        item['id'] = str(uuid.uuid4())
                    container.create_item(body=item)
            print(f'Data uploaded to container {container_name}')
        except exceptions.CosmosResourceNotFoundError:
            print(f"Container {container_name} does not exist in database {database_name}")
        except Exception as e:
            print(f"Error updating data: {e}")

if __name__=="__main__":
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())
    cosmos_db_connection_string = os.getenv('cosmos_db_connection_string')
    handler = CosmosDBHandler(connection_string=cosmos_db_connection_string)
    df=handler.download_data('loop-redteam','red-team-1')

    handler.update_data(df,'loop-redteam','red-team-1')