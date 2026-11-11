# Setup and runtime configuration

## Install components

The component URLs and commit pins are configured. Run `./scripts/setup.sh` from the repository root. Set `PYTHON=/path/to/python3.12` if the default interpreter is not on PATH.

Setup creates `.venv` for the engine and `plugins/words-java/.venv` for the standard-library-only plugin. It initializes the two immediate submodules only. Do not add `--recursive`.

The pinned engine must include Java serving: retrieval profiles that accept `com.<product>.` symbols and the `/words/java/mcp/v1/streamable-http` route. `verify_registration.py` fails if either is missing.

## Configure the runtime

Follow the pinned engine's deployment instructions for PostgreSQL, Valkey, RabbitMQ, Qdrant, OpenSearch, authentication, and embedding-provider settings. For local development, copy `engine/.env.example` to `engine/.env.local` and review its settings. The run wrapper changes directory to `engine/`, where configuration and runtime paths are resolved.

The engine's `make infra-up` starts its development backing services. Review its Compose environment and ports first. For a VM or Kubernetes deployment, follow the engine's corresponding guide and adapt mounts to this repository's component layout.

Both `ADCS_PRODUCT_PLUGIN_CATALOG` and `ADCS_RETRIEVAL_PLUGIN_CATALOG` are set by `scripts/run-engine.sh` to this repository's catalog. Using the engine directly can bypass that configuration and the retrieval profile.

## Container deployment

The helpers run host Python environments; this repository does not include a product-specific container composition. Provision or mount the deployment catalog, plugin manifest, retrieval profile, plugin interpreter, source repositories, and Gist cache at paths visible inside the relevant containers. Preserve the catalog's relative `../plugins/words-java/plugin.json` relationship or use a deployment-specific catalog with correct container paths. The engine's empty-catalog image does not include this plugin.

## Verify serving

Start the API through the wrapper, check `/healthz`, then verify authenticated MCP initialization and real retrieval results after ingestion. A healthy process or successful fixture check does not prove that a product corpus has been published.

For external clients, configure TLS, authentication, and ingress. Preserve the `/words/java/mcp` path and headers; SSE requires streaming without proxy buffering. The example launch command binds to loopback intentionally.
