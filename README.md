# Aspose.Words for Java MCP Server

Deploy the Aspose context engine with the Aspose.Words for Java extraction plugin registered, then connect an MCP-compatible AI client to documentation and API tools.

This repository supplies a pinned engine/plugin composition, its catalog, and setup, launch, and ingestion helpers. It does not bundle indexed documentation, provision infrastructure, or supply a hosted endpoint.

[Setup](docs/setup.md) · [Source preparation](docs/ingestion.md) · [Connect a client](docs/clients.md) · [Component maintenance](docs/public-release.md)

## Project family

These repositories work together to provide documentation-backed MCP services for Aspose.Words for Java. The shared engine is maintained under **aspose-core-mcp**; the Words/Java components are maintained under **aspose-words-mcp**.

| Repository | Responsibility |
| --- | --- |
| [context-engine](https://github.com/aspose-core-mcp/context-engine) | Shared documentation ingestion, indexing, retrieval, and MCP infrastructure |
| [java-plugin](https://github.com/aspose-words-mcp/java-plugin) | Aspose.Words for Java documentation/API extraction and retrieval profile |
| [java-server](https://github.com/aspose-words-mcp/java-server) **(this repository)** | Deployment helpers that combine pinned engine and plugin versions |

## Get the server

```sh
git clone https://github.com/aspose-words-mcp/java-server.git
cd java-server
```

The engine and plugin are pinned to reviewed public commits. Setup initializes only these immediate components. Do not clone recursively: the engine retains historical documentation submodules that this deployment does not need.

## Setup and verification

Requires Git and Python 3.12 or newer. Run from this repository root:

```sh
./scripts/setup.sh
```

Setup initializes only `engine` and `plugins/words-java`, installs the engine into `.venv`, creates a separate plugin interpreter, and verifies Words/Java-only registration, the Java retrieval profile, fixture extraction, and the `/words/java/mcp` MCP endpoint. It does not download source corpora or publish content.

## Run the server

Configure runtime stores, credentials, and embeddings as described in [setup](docs/setup.md), then:

```sh
./scripts/run-engine.sh -m uvicorn adcs.api.main:app --host 127.0.0.1 --port 8080
```

For queued ingestion, run the worker in another terminal:

```sh
./scripts/run-engine.sh -m celery -A adcs.worker.celery_app:celery_app worker --loglevel=info
```

Always use the wrapper: it selects this deployment's plugin catalog for both product registration and retrieval profiles and runs from `engine/` so relative runtime paths resolve consistently.

## Populate content and connect

Follow [source preparation and ingestion](docs/ingestion.md), validate extraction, and explicitly publish indexed content. Then configure a client with your deployment's endpoint:

```text
https://YOUR_MCP_HOST/words/java/mcp/v1/streamable-http
```

The example host is a placeholder. See [client setup](docs/clients.md) for the local URL, authentication guidance, and Copilot configuration.

## Scope

Only `aspose.words.java` is registered; the catalog has no compositions. The plugin's retrieval profile applies to `aspose.words`/`java`. The Words/Java route fixes the product and `language="java"`; it is not a Total/.NET member. The inherited engine still defines other product routes; restrict externally exposed paths in your ingress if required. Registration alone neither populates indexes nor grants access to documentation sources.

## Files

| Path | Purpose |
| --- | --- |
| `engine/` | Pinned context-engine submodule |
| `plugins/words-java/` | Pinned Words/Java plugin submodule |
| `config/product-platform-plugins.json` | Deployment registration catalog |
| `scripts/setup.sh` | Initialize components and verify registration |
| `scripts/run-engine.sh` | Launch engine commands with deployment catalogs |
| `scripts/ingest.sh` | Words/Java ingestion with explicit workspace and interpreter |
| `scripts/verify_registration.py` | Fixture-based integration check |

Gitlinks pin exact revisions. Updating an upstream branch does not update this deployment automatically. Review component updates and run registration and plugin tests before changing the pins.

## Validation and licenses

GitHub Actions checks shell syntax and the catalog, then runs registration, MCP route verification, and the plugin regression suite. It does not deploy services or publish content.

Engine and plugin license texts and notices are supplied by their respective pinned repositories. Preserve them when distributing those components. This repository is licensed under [MIT](LICENSE), copyright (c) 2001 - 2026 Aspose Pty Ltd.
