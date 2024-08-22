from sqlalchemy import create_engine, text
import pandas as pd

class sqlalchemy:
    def __init__(self, connection_string):
        """Initialize the database connection."""
        self.engine = create_engine(connection_string)

    def extract_data(self, query):
        """Execute the query and return a DataFrame."""
        try:
            df = pd.read_sql_query(query, self.engine)
            print("Data extract successful")
            return df
        except Exception as e:
            print(f'Error extracting data: {e}')
            return None

    def upload_data(self, df, table_name, columns):
        """Upload data from a DataFrame to the specified table."""
        try:
            db_df = df[columns]

            # Convert df to dictionary for insertion
            upsert_data = db_df.to_dict(orient='records')

            # Construct the insert query with ON DUPLICATE KEY UPDATE
            insert_query = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({', '.join([':' + col for col in columns])})
            ON DUPLICATE KEY UPDATE
            {', '.join([f'{col} = VALUES({col})' for col in columns if col != 'HitID'])}
            """

            # Execute the query for all records
            with self.engine.connect() as connection:
                connection.execute(text(insert_query), upsert_data)
                connection.commit()

            print('Data Successfully uploaded to DB')
        except Exception as e:
            print(f'Error uploading data: {e}')

# Example usage
if __name__ == "__main__":
    connection_string = 'mysql+mysqlconnector://mohan.wang@centific.com:8tCCc5c*wgJT@172.18.2.10/scribo_webapps_db'
    query = "SELECT * FROM tasks_hits WHERE taskid IN (1, 2, 3)"  # Example query
    extractor = sqlalchemy(connection_string)
    df = extractor.extract_data(query)
    print(df)
    
    # Prepare DataFrame to upload
    result_df = df.copy()  # Assume result_df is prepared as needed
    columns_to_upload = ['HitID', 'taskID', 'autoqa_data_handled']
    table_name = 'autoqa_tasks_hits'
    extractor.upload_data(result_df, table_name, columns_to_upload)
