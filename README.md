# Process Atlas (public release)

An explorable, anonymised release of the JPRX knowledge graph: 140
digital-fabrication enablers, 217 Japanese robotic-construction
processes, 50 deep-coded polar cases, 100 literature-cited
dependencies between enablers and 8447 co-occurrence pairs derived
from the cases.

Open `index.html` through a web server (`python -m http.server -d . 8080`, then
http://localhost:8080). Opening the file directly will not work: the page loads
its data with `fetch`, which browsers block on `file://`.

## What is here

| path | content |
|---|---|
| `index.html` | the Process Atlas viewer, running without a backend |
| `data/jprx_kg_public.ttl` | the graph itself, RDF/Turtle, the citable artefact |
| `data/graph.json` | the graph as the viewer consumes it |
| `data/node-info.json` | per-node record behind the Linked Info panel |
| `data/queries/` | the example questions with their answers and sources |

## Anonymisation, and its limits

Company and robot identities are removed, not obscured: firm names (EN and JP),
robot names, free-text robot descriptions, websites and source URLs are absent
from the released graph. Firms appear as stable pseudonyms (`Firm_NNN`) so that
co-development structure stays analysable. The mapping from pseudonym to firm
is held privately by the authors and is not part of any release.

Two honest limits. First, the categorical attributes are released unchanged, and
a combination of technology-readiness level, task, building system, deployment
mode and material is often distinctive: a reader with domain knowledge may
recognise individual well-known processes.
Second, the dependency layer keeps its academic citations, so author surnames
that coincide with firm names (for instance Yamazaki & Maeda 1998) do appear;
these are bibliographic references, not firm identifications.

## Answering questions

The retrieval and generation pipeline runs against the graph; this page is
statically hosted, so each example answer is served exactly as the pipeline
produced it, together with its sources. A hosted interface for free-form
queries is in preparation. To ask your own questions today, run the instrument
from the released code against this graph.

## Funding

Supported in part by the Swiss National Science Foundation (SNSF) Scientific
Exchanges grant IZSEZ0_242606.

## Reuse

Data: Creative Commons Attribution 4.0 International (CC BY 4.0).
Viewer code: MIT. See `LICENSE`.

Please cite the dataset (see `CITATION.cff`) alongside the paper it supports.
