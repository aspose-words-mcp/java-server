# Prepare sources and publish content

Run from the deployment repository root after setup. Source URLs, branches, and prefixes are defined by `plugins/words-java/plugin.json`; keep this manifest authoritative when updating component pins.

With the currently pinned plugin:

```sh
mkdir -p engine/sources
git clone --filter=blob:none --sparse --branch master https://github.com/aspose-words-mcp/docs.git engine/sources/documentation
git -C engine/sources/documentation sparse-checkout set en/java
git clone --filter=blob:none --sparse --branch main https://github.com/aspose-words-mcp/reference.git engine/sources/api-reference
git -C engine/sources/api-reference sparse-checkout set english/java
```

Record both source commits and ensure the source working trees are clean before ingestion.

## Prepare external examples

```sh
PYTHONPATH=plugins/words-java/src plugins/words-java/.venv/bin/python \
  -m adcs_words_java.gist_examples \
  --source-root engine/sources/documentation/en/java \
  --cache plugins/words-java/sources/gist-examples.json
```

This network step prepares pinned Gist examples. The cache belongs beside the plugin, while source repositories belong under the `engine/` ingestion workspace. Retain cache provenance with publication records. Extraction uses the cache offline; do not run concurrent cache preparation against the same file.

## Validate

```sh
./scripts/ingest.sh --source-kind docs
./scripts/ingest.sh --source-kind apiref
```

Validation may write operation metadata but does not publish indexed content. `--stage` writes review staging. Configure runtime stores and embeddings before publication.

## Publish explicitly

After reviewing validation results:

```sh
./scripts/ingest.sh --source-kind docs --publish
./scripts/ingest.sh --source-kind apiref --publish
```

Use `--enqueue` with an active worker for durable queued jobs. Read an operation using:

```sh
./scripts/run-engine.sh -m adcs.plugins.cli --workspace "$PWD/engine" --job-status YOUR_OPERATION_ID
```

Restart the API after publication so the retrieval profile and catalog are loaded. Source content, caches, credentials, and generated runtime data must not be committed. Verify documentation citations and Java API symbols through the deployed server after publication.
