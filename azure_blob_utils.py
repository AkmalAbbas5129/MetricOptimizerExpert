from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pandas as pd
import io


# Function to get blob service client
def get_blob_service_client(connection_string):
    return BlobServiceClient.from_connection_string(connection_string)


# Function to append data to a CSV in the blob
def append_to_csv(blob_service_client, container_name, blob_name, new_data):
    # Get a reference to the container
    container_client = blob_service_client.get_container_client(container_name)

    # Download the existing blob (if it exists)
    blob_client = container_client.get_blob_client(blob_name)
    try:
        existing_blob = blob_client.download_blob().readall()
        existing_data = pd.read_csv(io.StringIO(existing_blob.decode('utf-8')))
    except:
        existing_data = pd.DataFrame()

    # Append the new data to the existing data
    # updated_data = existing_data.append(new_data, ignore_index=True)
    # updated_data = existing_data.concat(new_data, ignore_index=True)
    updated_data = pd.concat([existing_data,new_data],ignore_index=True)
    # Upload the updated data back to the blob
    output = io.StringIO()
    updated_data.to_csv(output, index=False)
    blob_client.upload_blob(output.getvalue(), overwrite=True)
