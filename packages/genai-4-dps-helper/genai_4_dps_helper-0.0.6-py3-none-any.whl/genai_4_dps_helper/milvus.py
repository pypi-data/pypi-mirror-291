import os
from typing import List

from ibm_watsonx_ai import APIClient
from pandas import DataFrame
from pymilvus import connections


def get_milvus_connection(
    client: APIClient, connections: connections, server_pem_path="/tmp/presto.crt"
):
    """Connects to a Milvus Datbase speified in the connections property of 'client'. It expects the connection to be SSL and the cerficate is available in the connection metadata.

    Args:
        client (APIClient): A connected APIClient to watsonx.ai.
        connections (connections): The pymilvus connections object to open a connection with.
        server_pem_path (str, optional): Path to store the PEM file in. Defaults to "/tmp/presto.crt".
    """
    client_connections: DataFrame = client.connections.list()
    milvus_connection_id = client_connections.loc[
        client_connections["NAME"] == "MilvusConnection", "ID"
    ].values[0]
    milvus_credentials = (
        client.connections.get_details(milvus_connection_id)
        .get("entity")
        .get("properties")
    )
    if os.path.isfile(server_pem_path):
        os.remove(server_pem_path)
    with open(server_pem_path, "a") as fp:
        fp.write(milvus_credentials["ssl_certificate"])

    print(milvus_credentials)
    print(server_pem_path)

    connections.connect(
        host=milvus_credentials["host"],
        port=milvus_credentials["port"],
        user=milvus_credentials["username"],
        password=milvus_credentials["password"],
        server_pem_path=server_pem_path,
        server_name="watsonxdata",
        secure=True,
    )


def print_milvus_search_results(search_results: List):
    """Prints the results of Milvus searches in a readable fashion

    Args:
        search_results (List): A List [] object returned from a mlivus collection search method
    """
    for hits in search_results:
        print(hits.ids)
        print(hits.distances)
        for entity in hits:
            entity_str = f"{entity.name}: {entity.ingredients}"
            print(entity_str)
