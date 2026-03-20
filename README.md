# BioSpace-DBS

BioSpace-DBS is a space-biology knowledge platform that integrates natural language processing, relational databases, and a biomedical knowledge graph to support exploratory analysis of scientific literature. The system processes research abstracts through a multi-stage pipeline, stores structured results in SQLite, builds an entity-relation graph in Neo4j, and exposes everything through an interactive Streamlit dashboard with natural-language querying.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Technology Stack](#3-technology-stack)
4. [Architecture](#4-architecture)
5. [Data Contracts](#5-data-contracts)
6. [Database Schema](#6-database-schema)
7. [Knowledge Graph Schema](#7-knowledge-graph-schema)
8. [Setup and Installation](#8-setup-and-installation)
9. [Environment Configuration](#9-environment-configuration)
10. [Quick Start](#10-quick-start)
11. [Full Regeneration Workflow](#11-full-regeneration-workflow)
12. [Dashboard Capabilities](#12-dashboard-capabilities)
13. [Query Engine](#13-query-engine)
14. [Graph Adapter System](#14-graph-adapter-system)
15. [Validation and Testing](#15-validation-and-testing)
16. [Known Caveats](#16-known-caveats)
17. [License](#17-license)

---

## 1. Project Overview

The platform is built around a corpus of 80 curated space-biology research papers. It supports the following research workflows:

- **Literature exploration** — browse papers with AI-generated summaries and cluster assignments
- **Topic clustering** — group papers into latent thematic clusters using sentence embeddings and KMeans
- **Keyword and insight extraction** — surface cluster-level keywords and knowledge gap signals
- **Biomedical entity recognition** — extract genes, proteins, organisms, conditions, tissues, processes, and other entity types from paper abstracts
- **Relationship extraction** — identify causal, regulatory, and associative relationships between biomedical entities
- **Knowledge graph querying** — traverse entity-relation networks in Neo4j
- **Hybrid querying** — combine graph-discovered entities with SQL-based paper filtering in a single query

---

## 2. Repository Structure

```text
BioSpace-DBS/
├── config/                     Configuration and environment loading
│   ├── config.py               Root path resolution and data directory setup
│   ├── config_m1.py            NER entity types, relation types, regex patterns, synonyms
│   └── neo4j_config.py         Neo4j credentials loader
│
├── pipeline/                   NLP processing modules
│   ├── summarizer.py           Abstract summarization (DistilBART)
│   ├── embedder.py             Sentence embeddings (MiniLM)
│   ├── clusterer.py            KMeans topic clustering
│   ├── keyword_extractor.py    YAKE keyword extraction and cluster summaries
│   ├── insights.py             Knowledge gap detection and cluster insights
│   └── nlp_pipeline.py         Insights generation entry point
│
├── sql/                        Relational database layer
│   ├── models.py               SQLAlchemy ORM schema
│   ├── db_init.py              Database initialization and data loading
│   ├── test_db.py              Validation and record counts
│   └── example_queries.sql     Reference SQL queries
│
├── nosql/                      Graph adapter layer
│   ├── __init__.py             Adapter selector (reads KG_ADAPTER env var)
│   ├── neo4j_adapter.py        Live Neo4j implementation
│   ├── graph_placeholder.py    Demo fallback with hardcoded entities
│   ├── nl_to_cypher.py         Natural language to Cypher query converter
│   └── test_graph_backend.py   Graph connection validation
│
├── ner_pipeline/               Knowledge graph extraction pipeline
│   ├── entity_pipeline.py      NER entity extraction from abstracts
│   ├── relation_pipeline.py    Relation extraction via dependency parsing
│   ├── filter_entities.py      Importance-score filtering
│   ├── graph_builder_neo4j.py  Neo4j import (nodes and relationships)
│   ├── generate_graph_visualization.py  PyVis HTML visualization
│   ├── analyze_entities.py     Entity statistics report
│   ├── analyze_relations.py    Relation statistics report
│   ├── analyze_graph.py        Full graph statistics
│   ├── knowledge_graph_full.html  Pre-rendered interactive graph
│   └── README_M1.md            Knowledge graph pipeline documentation
│
├── dashboard/
│   └── app.py                  Streamlit application entry point
│
├── dashboard_integration/      Data access and query routing
│   ├── data_access.py          SQL and graph retrieval helpers
│   └── query_engine.py         Query classification and dispatch
│
├── data/                       Corpus and generated NLP artifacts
│   ├── papers_clean.csv        Canonical input (80 papers)
│   └── outputs/
│       ├── summaries.csv
│       ├── embeddings.npy
│       ├── embeddings_meta.csv
│       ├── clusters.csv
│       ├── cluster_keywords.csv
│       ├── cluster_summaries.csv
│       └── insights.json
│
├── graph_data/                 Knowledge graph artifacts
│   ├── entities.json           593 extracted entities
│   ├── relations.json          1,303 extracted relations
│   ├── filtered_entities.json  107 high-importance entities
│   ├── filtered_relations.json 758 high-importance relations
│   ├── entity_rankings.json
│   └── relation_patterns.json
│
├── data_prep/                  Raw data sources and preparation notebooks
├── sql/space_bio.db            SQLite database (generated)
└── .env                        Environment secrets (not committed)
```

---

## 3. Technology Stack

### Core Frameworks

| Component | Library / Tool | Version Guidance |
|-----------|---------------|-----------------|
| Dashboard | Streamlit | Latest stable |
| ORM | SQLAlchemy | 2.x |
| Database | SQLite | Built-in |
| Graph Database | Neo4j Aura (cloud) | 5.x compatible |
| Graph Driver | neo4j Python driver | 5.x |

### NLP and ML

| Component | Library / Model |
|-----------|----------------|
| Summarization | `sshleifer/distilbart-cnn-12-6` via Hugging Face Transformers |
| Sentence Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Clustering | scikit-learn KMeans |
| Keyword Extraction | YAKE (Yet Another Keyword Extractor) |
| Biomedical NER | scispacy `en_ner_bc5cdr_md`, `en_ner_bionlp13cg_md` |
| General NLP | spacy `en_core_sci_sm` |
| Data manipulation | pandas, numpy |

### Graph and Visualization

| Component | Library |
|-----------|---------|
| Graph algorithms | networkx |
| Interactive visualization | pyvis |
| String matching | fuzzywuzzy |

### Infrastructure

| Component | Tool |
|-----------|------|
| Environment variables | python-dotenv |
| Embedding storage | numpy `.npy` format |
| Artifact storage | CSV and JSON files |

---

## 4. Architecture

### 4.1 End-to-End Data Flow

```
data/papers_clean.csv  (80 papers)
         |
         v
  NLP Pipeline (pipeline/)
  |-- summarizer.py       -->  data/outputs/summaries.csv
  |-- embedder.py         -->  data/outputs/embeddings.npy + embeddings_meta.csv
  |-- clusterer.py        -->  data/outputs/clusters.csv
  |-- keyword_extractor   -->  data/outputs/cluster_keywords.csv
  |                            data/outputs/cluster_summaries.csv
  `-- insights.py         -->  data/outputs/insights.json
         |
         v
  SQL Layer (sql/)
  |-- db_init.py loads all outputs above
  `-- space_bio.db  (tables: papers, summaries, keywords, clusters, associations)
         |
         v  (parallel path)
  NER Pipeline (ner_pipeline/)
  |-- entity_pipeline.py  -->  graph_data/entities.json         (593 entities)
  |-- relation_pipeline   -->  graph_data/relations.json        (1,303 relations)
  |-- filter_entities.py  -->  graph_data/filtered_entities.json (107 entities)
  |                            graph_data/filtered_relations.json (758 relations)
  |-- graph_builder_neo4j -->  Neo4j Aura (cloud database)
  `-- graph_visualization -->  ner_pipeline/knowledge_graph_full.html
         |
         v
  Dashboard (dashboard/)
  |-- data_access.py      reads SQL + graph
  |-- query_engine.py     routes SQL / GRAPH / HYBRID queries
  `-- app.py              Streamlit UI at http://localhost:8501
```

### 4.2 Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| `pipeline/` | Stateless NLP processing functions; outputs are CSV and numpy files |
| `sql/` | ORM schema and database initialization; loads NLP artifacts into structured tables |
| `ner_pipeline/` | Biomedical entity and relation extraction; pushes to Neo4j; generates visualization |
| `nosql/` | Hot-swappable graph client; controlled by `KG_ADAPTER` environment variable |
| `dashboard_integration/` | Unified data access and query classification layer |
| `dashboard/` | Streamlit UI; consumes `dashboard_integration/` only |
| `config/` | Centralized path resolution and NER configuration |

---

## 5. Data Contracts

### 5.1 Primary Input

`data/papers_clean.csv` is the canonical corpus. Required columns:

| Column | Type | Description |
|--------|------|-------------|
| `paper_id` | string | Unique paper identifier |
| `title` | string | Paper title |
| `abstract` | string | Full abstract text |

Optional columns currently present:

| Column | Type | Description |
|--------|------|-------------|
| `authors` | string | Comma-separated author list |
| `year` | integer | Publication year |
| `journal` | string | Journal name |
| `doi_url` | string | DOI URL |

### 5.2 SQL Build Inputs

`sql/db_init.py` requires the following files to exist before running:

```text
data/papers_clean.csv
data/outputs/summaries.csv
data/outputs/clusters.csv
data/outputs/cluster_keywords.csv
data/outputs/cluster_summaries.csv
```

All of these files are committed to the repository and do not need to be regenerated for a quick-start run.

### 5.3 Graph Build Inputs

`ner_pipeline/graph_builder_neo4j.py` requires:

```text
graph_data/filtered_entities.json
graph_data/filtered_relations.json
```

Both files are committed to the repository.

---

## 6. Database Schema

The SQLite database (`sql/space_bio.db`) is defined via SQLAlchemy ORM in `sql/models.py`.

### Tables

**`papers`**

| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | Auto-increment |
| `external_id` | String | Maps to `paper_id` in CSV |
| `title` | String | Paper title |
| `authors` | String | Author list |
| `year` | Integer | Publication year |
| `journal` | String | Journal name |
| `doi_url` | String | DOI URL |
| `abstract` | Text | Full abstract |

**`summaries`**

| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | |
| `text` | Text | Generated summary |
| `method` | String | Model identifier |
| `paper_id` | Integer FK | References `papers.id` |

**`keywords`**

| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | |
| `text` | String | Keyword phrase |
| `score` | Float | YAKE score (lower = more relevant) |

**`clusters`**

| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | |
| `label` | Integer | Cluster index (0-4) |
| `summary_text` | Text | Cluster-level summary |
| `representative_keyword` | String | Top keyword for this cluster |

### Association Tables

| Table | Purpose |
|-------|---------|
| `paper_keyword` | Many-to-many: papers to keywords |
| `paper_cluster` | Many-to-many: papers to cluster assignments |

---

## 7. Knowledge Graph Schema

### Node Type

All graph nodes use the label `Entity`.

| Property | Type | Description |
|----------|------|-------------|
| `entity_id` | String (unique) | Stable identifier |
| `name` | String | Canonical entity name |
| `type` | String | One of 10 entity types (see below) |
| `importance_score` | Float | Computed relevance score |
| `papers` | List[String] | Paper IDs that mention this entity |
| `relation_count` | Integer | Number of relationships |
| `synonyms` | List[String] | Alternate names |

### Entity Types

`gene`, `protein`, `organism`, `condition`, `tissue`, `process`, `assay`, `disease`, `cell_type`, `chemical`

### Relationship Types

`AFFECTS`, `ASSOCIATED_WITH`, `EXPRESSED_IN`, `REGULATES`, `USED_IN`, `INCREASES`, `DECREASES`, `INDUCES`, `INHIBITS`, `CAUSES`, `MEASURED_IN`, `PART_OF`

Each relationship carries:

| Property | Type | Description |
|----------|------|-------------|
| `relation_type` | String | One of 12 types above |
| `evidence_count` | Integer | Occurrences across corpus |
| `confidence` | Float | Extraction confidence |
| `papers` | List[String] | Supporting paper IDs |

### Graph Statistics (Current Build)

| Metric | Value |
|--------|-------|
| Total extracted entities | 593 |
| Total extracted relations | 1,303 |
| Filtered entities (importance threshold >= 20) | 107 |
| Filtered relations | 758 |

### Importance Score Formula

```
importance = (paper_count * 1.0) + (relation_count * 2.0) + (relation_type_diversity * 1.5)
```

---

## 8. Setup and Installation

### 8.1 Prerequisites

- Python 3.9 or higher
- pip
- Internet access for downloading transformer and scispacy models (only required for full pipeline regeneration)
- Neo4j Aura account (optional; placeholder mode works without it)

### 8.2 Clone and Create Environment

```bash
git clone <repository-url>
cd BioSpace-DBS

python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 8.3 Scispacy Model Installation

Biomedical NER requires scispacy models that must be installed separately from pip:

```bash
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bc5cdr_md-0.5.1.tar.gz
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bionlp13cg_md-0.5.1.tar.gz
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_sm-0.5.1.tar.gz
```

These are only required if regenerating the knowledge graph. They are not needed for the dashboard or SQL workflows.

---

## 9. Environment Configuration

Create a `.env` file in the repository root:

```env
# Neo4j connection (required only when KG_ADAPTER=neo4j)
NEO4J_URI=neo4j+s://<your-instance>.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=<your-password>

# Graph adapter selection
KG_ADAPTER=placeholder
```

### Adapter Modes

| `KG_ADAPTER` value | Behavior |
|--------------------|---------|
| `placeholder` | Dashboard graph tab uses eight hardcoded demo entities. No database connection required. All SQL features fully functional. |
| `neo4j` | Dashboard and query engine connect to Neo4j Aura using the credentials above. Full 107-entity, 758-relationship graph available. |

The adapter is selected at import time in `nosql/__init__.py` and exposed as `GraphClient` throughout the codebase.

---

## 10. Quick Start

All pipeline artifacts and the SQLite database source files are committed to the repository. The minimum steps to run the dashboard are:

```bash
# Step 1: Build the SQLite database from committed CSV artifacts
python sql/db_init.py

# Step 2: Launch the dashboard
streamlit run dashboard/app.py
```

The dashboard will be available at `http://localhost:8501`.

If you want to enable live graph queries, set `KG_ADAPTER=neo4j` in `.env` and provide valid Neo4j credentials before launching.

---

## 11. Full Regeneration Workflow

Use this section to regenerate all artifacts from the source CSV.

### 11.1 NLP Artifacts

The pipeline modules are library-style. Call them in the following order from a runner script or Python session:

```python
from pipeline.summarizer import generate_summaries
from pipeline.embedder import embed_all
from pipeline.clusterer import generate_clusters
from pipeline.keyword_extractor import build_cluster_keywords, generate_cluster_summaries

import pandas as pd

df = pd.read_csv("data/papers_clean.csv")

# 1. Summarize
summaries_df = generate_summaries(df, text_column="abstract")

# 2. Embed
embeddings, meta_df = embed_all(summaries_df, text_column="summary")

# 3. Cluster
clusters_df = generate_clusters("data/outputs/embeddings.npy", "data/outputs/embeddings_meta.csv", n_clusters=5)

# 4. Keywords and cluster summaries
build_cluster_keywords(summaries_df, clusters_df)
generate_cluster_summaries(summaries_df, clusters_df)
```

Then generate insights:

```bash
python pipeline/nlp_pipeline.py
```

This produces `data/outputs/insights.json` from `cluster_keywords.csv` and `cluster_summaries.csv`.

### 11.2 SQL Database

```bash
python sql/db_init.py
python sql/test_db.py
```

Output: `sql/space_bio.db`

The initialization script drops and recreates all tables on each run.

### 11.3 Knowledge Graph Pipeline

Run each script in sequence:

```bash
# Extract entities from paper abstracts
python ner_pipeline/entity_pipeline.py

# Extract relationships between entities
python ner_pipeline/relation_pipeline.py

# Filter by importance score
python ner_pipeline/filter_entities.py

# Generate statistics
python ner_pipeline/analyze_graph.py

# Push to Neo4j (requires KG_ADAPTER=neo4j and valid credentials)
python ner_pipeline/graph_builder_neo4j.py

# Generate interactive HTML visualization
python ner_pipeline/generate_graph_visualization.py
```

Outputs:

| File | Description |
|------|-------------|
| `graph_data/entities.json` | All 593 extracted entities |
| `graph_data/relations.json` | All 1,303 extracted relations |
| `graph_data/filtered_entities.json` | 107 high-importance entities |
| `graph_data/filtered_relations.json` | 758 high-importance relations |
| `graph_data/entity_rankings.json` | Ranked entity list |
| `graph_data/relation_patterns.json` | Relation pattern analysis |
| `ner_pipeline/knowledge_graph_full.html` | Interactive visualization |

---

## 12. Dashboard Capabilities

The Streamlit application (`dashboard/app.py`) provides seven functional tabs:

### Overview

- Total paper count, cluster count, keyword count
- Bar chart of papers by publication year
- Bar chart of papers by cluster assignment

### Papers Explorer

- Paginated list of up to 100 papers
- Per-paper detail view with:
  - Full abstract
  - AI-generated summary (DistilBART)
  - Extracted keywords with YAKE scores
  - Cluster assignment

### Clusters Explorer

- List of all five clusters
- Per-cluster summary text
- List of member papers for each cluster

### Query Console

- Natural language query input
- Automatic routing to SQL, graph, or hybrid execution
- Results displayed as structured DataFrames
- Example queries provided inline

### Insights

- Top keywords per cluster
- Knowledge gap signals detected by heuristic term matching
- Loaded from `data/outputs/insights.json`

### Knowledge Graph

- Embedded interactive PyVis visualization (`ner_pipeline/knowledge_graph_full.html`)
- Node coloring by entity type
- Node sizing by importance score
- Direct link to Neo4j browser (when `KG_ADAPTER=neo4j`)

### Graph Query Playground

- Natural language to Cypher query conversion (`nosql/nl_to_cypher.py`)
- Shows generated Cypher query and explanation
- Supports pattern queries: entity lookup, relationship traversal, path finding

---

## 13. Query Engine

`dashboard_integration/query_engine.py` classifies and dispatches natural language queries.

### Query Classification

| Mode | Trigger Keywords |
|------|----------------|
| `SQL` | year, keyword, cluster, abstract, title, papers, summary, journal, doi, after, before |
| `GRAPH` | entity, relation, connected, linked, graph, node, edge |
| `HYBRID` | "related to", "connected to", "and in cluster" |

If no keywords match, the engine defaults to `SQL`.

### SQL Query Examples

```
papers in cluster 0
papers after 2020
keyword microgravity
```

### Graph Query Examples

```
entities
entities of type gene
```

### Hybrid Query Examples

```
related to spaceflight
what affects bone
connected to microgravity and in cluster 2
```

Hybrid queries first resolve entity names in the graph, retrieve associated paper IDs, then filter those papers through the SQL layer.

### Caching

The query engine applies LRU caching to `_cached_get_related_papers` and `_cached_get_entity_by_name` to reduce repeated graph round-trips within a session.

---

## 14. Graph Adapter System

The `nosql/` package implements a hot-swappable adapter pattern controlled by the `KG_ADAPTER` environment variable.

### Interface

Both adapters implement the same methods:

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_entities` | `(entity_type=None, limit=50)` | List entities, optionally filtered by type |
| `get_entity_by_name` | `(name)` | Case-insensitive entity lookup |
| `get_related_papers` | `(entity_id, limit=20)` | Paper IDs associated with an entity |
| `get_entity_relations` | `(entity_id, relation_type=None)` | All relationships for an entity |
| `close` | `()` | Release database connection |

### Natural Language to Cypher

`nosql/nl_to_cypher.py` supports the following query patterns:

| Pattern | Example Input |
|---------|--------------|
| Effect queries | "what affects bone" |
| Causal queries | "what causes muscle atrophy" |
| Top entity listing | "top entities" |
| Path queries | "path between gene X and tissue Y" |
| Paper queries | "papers about microgravity" |
| General entity lookup | "find spaceflight" |

Each call returns a tuple of `(cypher_query, explanation, parameters)`.

---

## 15. Validation and Testing

Current validation is script-based rather than pytest-based.

### SQL Validation

```bash
python sql/test_db.py
```

Outputs record counts for all tables and displays sample paper-cluster associations and top keywords.

### Graph Validation

```bash
python nosql/test_graph_backend.py
```

Tests the adapter connection and basic retrieval methods.

### NER Pipeline Analysis

```bash
python ner_pipeline/analyze_entities.py
python ner_pipeline/analyze_relations.py
python ner_pipeline/analyze_graph.py
```

These generate statistical summaries of extracted entities and relations.

### Reference SQL

`sql/example_queries.sql` contains annotated SQL examples for direct use in any SQLite client against `sql/space_bio.db`.

---

## 16. Known Caveats

1. **Import path inconsistency** — `ner_pipeline/entity_pipeline.py` imports `config_m1` without the `config.` package prefix (`from config_m1 import ...`). Depending on the working directory, this may require adding `config/` to `sys.path` or correcting the import statement to `from config.config_m1 import ...`.

2. **No pipeline CLI entry points** — Modules in `pipeline/` are library-style and do not expose `__main__` blocks. To regenerate NLP artifacts, call the functions from a runner script as described in section 11.1.

3. **Graph fallback behavior** — Without valid Neo4j credentials or with `KG_ADAPTER=placeholder`, graph tabs in the dashboard return demo entities only. Relation and paper lookups return empty results in placeholder mode.

4. **Test architecture** — Tests are standalone scripts. There is no pytest suite. Continuous integration is not currently configured.

5. **Legacy import reference** — `nosql/test_graph_backend.py` references `graph_backend`, which is a legacy module name. The current adapter design uses `nosql/neo4j_adapter.py` and `nosql/graph_placeholder.py` selected via `nosql/__init__.py`.

6. **Pre-computed artifacts** — Committed output files enable quick-start demos, but full reproducibility requires model availability, scispacy installation, and a live Neo4j instance for the graph build step.

---

## 17. License

No explicit license file is currently present at the repository root. Add a `LICENSE` file before external distribution or publication.
