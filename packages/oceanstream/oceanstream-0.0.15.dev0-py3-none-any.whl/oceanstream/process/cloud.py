import logging
from oceanstream.process.azure.blob_storage import get_azfs


def get_chunk_store(storage_config, path):

    azfs = get_azfs(storage_config)

    container_name = storage_config['container_name']

    if not azfs.exists(container_name):
        try:
            azfs.mkdir(container_name)
        except Exception as e:
            logging.error(f"Error creating container {container_name}: {e}")
            raise

    if azfs:
        return azfs.get_mapper(f"{container_name}/{path}")

    raise ValueError(f"Unsupported storage type: {storage_config['storage_type']}")