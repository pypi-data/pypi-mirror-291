"""
Motif Studio (https://github.com/aplbrain/motifstudio) is a graph analysis and
storage tool for motif discovery in connectome networks.

This package provides an interface to the Motif Studio API.

"""

import httpx
from typing import Literal
import pydantic
import networkx as nx

__version__ = "0.1.0"


_MotifAggregationTypes = Literal[
    "host.vertex", "motif.vertex", "motif.vertex.attribute", "sample"
]


class HostListing(pydantic.BaseModel):
    name: str
    id: str


class _HostLookup(dict):
    """
    A listing of host graphs on the Motif Studio server.

    Behaves like a dict.

    """

    _cached_graphs: dict[str, HostListing] = {}

    def __init__(self, motif_studio: "MotifStudio"):
        self._api = motif_studio
        self._cached_graphs = {
            item["id"]: item
            for item in self._api._get("providers/hostlist").get("hosts", [])
        }

    def __getitem__(self, key):
        return self._cached_graphs[key]

    def __iter__(self):
        return iter(self._cached_graphs)

    def __len__(self):
        return len(self._cached_graphs)

    def keys(self):
        return self._cached_graphs.keys()

    def items(self):
        return self._cached_graphs.items()

    def values(self):
        return self._cached_graphs.values()

    def get_graph(self, key: str) -> nx.Graph:
        """
        Retrieves the graph associated with this host listing.

        Returns:
            Graph: The graph associated with this host listing.

        """
        raw_xml = self._api._post(
            "queries/graph/download", {"host_id": key, "format": "graphml"}, raw=True
        )
        if "graphml" not in raw_xml.decode("utf-8"):
            raise ValueError("Invalid GraphML response")
        return nx.parse_graphml(raw_xml)


class _HostQueries:

    def __init__(self, host_id: str, motif_studio: "MotifStudio"):
        self.host_id = host_id
        self._api = motif_studio

    def vertices_count(self):
        """
        Returns the number of vertices in the graph associated with this host.

        Returns:
            int: The number of vertices in the graph.

        """
        return self._api._post("queries/vertices/count", {"host_id": self.host_id})[
            "vertex_count"
        ]

    def edges_count(self):
        """
        Returns the number of edges in the graph associated with this host.

        Returns:
            int: The number of edges in the graph.

        """
        return self._api._post("queries/edges/count", {"host_id": self.host_id})[
            "edge_count"
        ]

    def vertices_attributes(self):
        """
        Returns the attributes of the vertices in the graph associated with this host.

        Returns:
            dict: A dictionary of vertex attributes.

        """
        return self._api._post("queries/vertices/attributes", {"host_id": self.host_id})

    def motifs_count(self, motif: str):
        """
        Returns the number of motifs in the graph associated with this host.

        Returns:
            int: The number of motifs in the graph.

        """
        return self._api._post(
            "queries/motifs/count", {"host_id": self.host_id, "query": motif}
        )["motif_count"]

    def motifs(
        self, motif: str, aggregation: None | _MotifAggregationTypes = None
    ) -> tuple[list, list, dict]:
        """
        Returns the motifs in the graph associated with this host.

        Returns:
            list: A list of motif mappings, per the aggregation type.
            list: Motif entities.
            dict: Pointers to host volumetric data, if any.

        """
        aggregation_opts = (
            {} if aggregation is None else {"aggregation_type": aggregation}
        )
        res = self._api._post(
            "queries/motifs",
            {"host_id": self.host_id, "query": motif, **aggregation_opts},
        )
        return (
            res["motif_results"],
            res["motif_entities"],
            res.get("host_volumetric_data", {}),
        )


class _QueryProvider:

    def __init__(self, motif_studio: "MotifStudio"):
        self._api = motif_studio

    def __call__(self, host_id: str):
        return _HostQueries(host_id, self._api)


class MotifStudio:
    """
    The MotifStudio class provides an interface to the Motif Studio API.
    """

    def __init__(self, base_url: str = "https://api.motifstudio.bossdb.org"):
        """
        Initializes the MotifStudio class with the given base URL.

        Note that the default base URL points to the Motif Studio API, NOT the
        Motif Studio web application (https://motifstudio.bossdb.org).

        Args:
            base_url (str): The base URL for the Motif Studio API.

        """
        self.base_url = base_url
        self.hosts = _HostLookup(self)
        self.query = _QueryProvider(self)

    def _get(self, endpoint: str):
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to.

        Returns:
            dict: The JSON response from the API.

        Raises:
            httpx.HTTPStatusError: If the request returned an error status code.

        """
        response = httpx.get(f"{self.base_url}/{endpoint}")
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: dict, raw: bool = False):
        """
        Sends a POST request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to.
            data (dict): The data to send in the request body.

        Returns:
            dict: The JSON response from the API.

        Raises:
            httpx.HTTPStatusError: If the request returned an error status code.

        """
        response = httpx.post(
            f"{self.base_url}/{endpoint}",
            json=data,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json() if not raw else response.content
