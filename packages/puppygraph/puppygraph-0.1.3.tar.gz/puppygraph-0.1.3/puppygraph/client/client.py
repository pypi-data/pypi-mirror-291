"""PuppyGraph client module."""

import logging
import signal
import time
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union

import requests
from gremlin_python.driver import client as GremlinClient
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.driver.serializer import GraphBinarySerializersV1
from neo4j import Driver as CypherDriver
from neo4j import GraphDatabase, Query, Result
from neo4j.exceptions import AuthError, CypherSyntaxError, ServiceUnavailable

from puppygraph.common.conversion_utils import convert_mapping_config_to_host_json
from puppygraph.data.host.host_config import PuppyGraphHostConfig
from puppygraph.data.mapping.graph_mapping_config import PuppyGraphMappingConfig

logger = logging.getLogger(__name__)
logger.addHandler(
    logging.NullHandler()
)  # Prevent "No handlers could be found" warnings


class PuppyGraphClient:
    """PuppyGraph client."""

    def __init__(self, config: PuppyGraphHostConfig):
        """Initializes a PuppyGraph client."""
        self._config = config
        self._cypher_query_driver = GraphDatabase.driver(
            f"bolt://{config.ip}:{config.cypher_port}/"
        )
        self._gremlin_query_client = GremlinClient.Client(
            f"ws://{config.ip}:{config.gremlin_port}/gremlin",
            traversal_source="g",
            username=config.username,
            password=config.password,
            message_serializer=GraphBinarySerializersV1(),
        )

    def set_schema(
        self, mapping_config: Union[PuppyGraphMappingConfig, Dict]
    ) -> PuppyGraphMappingConfig:
        """Sets the graph mapping config in PuppyGraph server.

        Args:
            mapping_config: The graph mapping config to set, can be json or dataclass.

        Returns:
            The puppygraph graph mapping config that was set.
        """
        return _set_schema(host_config=self._config, mapping_config=mapping_config)

    def cypher_query(
        self, query: str, params: Optional[Dict[str, Any]] = None, timeout_ms=30000
    ) -> List[Dict[str, Any]]:
        """Executes a Cypher query on the puppy graph.

        Args:
            query: The Cypher query to execute.
            params: The parameters to pass to the Cypher query.
            timeout_ms: The timeout in milliseconds for the query, defaults to 30000.

        Returns:
            The result of the Cypher query in a list of dictionaries.
        """
        return _run_cypher_query(
            cypher_driver=self._cypher_query_driver,
            query=query,
            params=params,
            timeout_ms=timeout_ms,
        )

    def gremlin_query(self, query: str, timeout_ms=30000) -> List[Dict[str, Any]]:
        """Executes a Gremlin query on the puppy graph.

        Args:
            query: The Gremlin query to execute.
            timeout_ms: The timeout in milliseconds for the query, defaults to 30000.

        Returns:
            The result of the Gremlin query in a list of dictionaries.
        """
        return _run_gremlin_query(
            gremlin_client=self._gremlin_query_client,
            query=query,
            timeout_ms=timeout_ms,
        )


@contextmanager
def _timeout(milliseconds: int, error_msg: str):
    def signal_handler(signum, frame):
        raise TimeoutError(error_msg)

    signal.signal(signal.SIGALRM, signal_handler)
    signal.setitimer(signal.ITIMER_REAL, milliseconds / 1e3)
    try:
        yield
    finally:
        signal.alarm(0)


def _set_schema(
    host_config: PuppyGraphHostConfig,
    mapping_config: Union[PuppyGraphMappingConfig, Dict],
) -> PuppyGraphMappingConfig:
    """Sets the graph schema in PuppyGraph server.

    Args:
        host_config: The host configuration of the PuppyGraph server.
        mapping_config: The graph mapping config that defines how the graph is constructed, can be json or dataclass.

    Returns:
        The puppygraph schema that was set.
    """

    schema_json = convert_mapping_config_to_host_json(config=mapping_config)
    logger.info(
        "Setting graph schema in PuppyGraph server...\n=============================\n%s\n=============================\n",
        schema_json,
    )

    response = requests.post(
        f"http://{host_config.ip}:{host_config.http_port}/schema",
        auth=(host_config.username, host_config.password),
        json=schema_json,
        timeout=60,
    )
    response.raise_for_status()
    logger.info("Successfully updated the schema in PuppyGraph!")

    # Check if PuppyGraph is ready to serve
    response = requests.get(
        f"http://{host_config.ip}:{host_config.http_port}/schemajson",
        auth=(host_config.username, host_config.password),
        timeout=60,
    )
    while response.status_code != 200:
        time.sleep(10)
    logger.info("PuppyGraph is ready to serve the new schema!")
    return mapping_config


def _run_cypher_query(
    cypher_driver: CypherDriver,
    query: str,
    params: Optional[Dict[str, Any]] = None,
    timeout_ms: int = 30000,
) -> List[Dict[str, Any]]:
    with (
        cypher_driver.session() as session,
        _timeout(
            milliseconds=timeout_ms,
            error_msg=f"Cypher query `{query}` timeout after {timeout_ms} ms!",
        ),
    ):
        neo4j_query = Query(text=query, timeout=timeout_ms / 1e3)
        try:
            res: Result = session.run(neo4j_query, params)
            json_data: List[Dict[str, Any]] = [record.data() for record in res]
            return json_data
        except CypherSyntaxError as e:
            raise ValueError(f"`{query}` is not valid:\n{e}") from e
        except (AuthError, ServiceUnavailable, TimeoutError) as e:
            raise e


def _run_gremlin_query(
    gremlin_client: GremlinClient,
    query: str,
    timeout_ms: int = 30000,
) -> List[Dict[str, Any]]:
    with _timeout(
        milliseconds=timeout_ms,
        error_msg=f"Gremlin query `{query}` timed out after {timeout_ms} ms!",
    ):
        try:
            result_set = gremlin_client.submit(query)
            results = result_set.all().result()
            return results
        except GremlinServerError as e:
            raise ValueError(f"Gremlin query error: {e}") from e
        except TimeoutError as e:
            raise TimeoutError(f"Timeout occurred: {e}") from e
        except Exception as e:
            raise e
