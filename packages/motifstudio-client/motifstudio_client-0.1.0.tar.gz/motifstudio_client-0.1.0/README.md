# MotifStudio: Python SDK

[MotifStudio](https://motifstudio.bossdb.org) is a platform for analyzing subnetwork motifs in connectome graphs. This Python SDK allows users to interact with the MotifStudio API to perform various operations such as querying graphs, retrieving motifs, and more.

## Installation

`uv`.

In order to use the MotifStudio Python SDK, you need to install the `motifstudio` package. You can do this using pip or `uv`:

```bash
# SLOW:
# pip install motifstudio-client

# Add motifstudio-client to a project FAST:
uv add motifstudio-client
```

## Usage

To use the MotifStudio Python SDK, you need to create an instance of the `MotifStudioClient` class and provide the API endpoint. You can then use this instance to interact with the API. (The SDK defaults to the public API endpoint but if you are using a private instance, you can specify the URL.)

```python
m = MotifStudioClient("https://api.motifstudio.bossdb.org")
```

To get a list of available "host" graphs, you can use the `hosts` object, which behaves like a dictionary:

```python
g.hosts.keys()  # List all available host graphs
```

You can perform basic operations such as querying the number of vertices or edges in the graph:

```python
m.query("Takemura2013_Medulla").vertices_count()
m.query("Takemura2013_Medulla").edges_count()
```

Perform a motif search on a specific graph:

```python
my_triangle_motif = """
A->B
B->C
C->A
"""

m.query("Takemura2013_Medulla").motifs(my_triangle_motif)  # Example motif query
```

You can also download a graph into a local [NetworkX](https://networkx.org/) object for local analysis:

```python
g = m.hosts.get_graph("Takemura2013_Medulla")
```

---

<p align='center'><small>Made with 💙 at <a href='http://www.jhuapl.edu/'><img alt='JHU APL' align='center' src='https://user-images.githubusercontent.com/693511/62956859-a967ca00-bdc1-11e9-998e-3888e8a24e86.png' height='42px'></a></small></p>
