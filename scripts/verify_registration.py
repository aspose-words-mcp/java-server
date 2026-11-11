"""Check Words/Java registration, retrieval profile, both worker contracts and the scoped MCP route."""
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "config/product-platform-plugins.json"
os.environ["ADCS_PRODUCT_PLUGIN_CATALOG"] = str(path)
os.environ["ADCS_RETRIEVAL_PLUGIN_CATALOG"] = str(path)
os.environ["ADCS_ENV"] = "dev"
sys.path.insert(0, str(ROOT / "engine/src"))
from adcs.plugins.catalog import PluginCatalog
from adcs.plugins.contracts import ExtractionResponse
from adcs.retrieval.profiles import load_profiles

catalog = PluginCatalog(path)
assert set(catalog.plugins) == {"aspose.words.java"}
assert not catalog.compositions
manifest = catalog.extractor("aspose.words.java")
assert manifest.retrieval_profile is not None
# Java preferred symbols need the engine's com.<product>. prefix support.
assert set(load_profiles(str(path))) == {("aspose.words", "java")}
fixtures = ROOT / "plugins/words-java/tests/fixtures"
for kind, fixture, relative in [
    ("docs", "docs.md", "en/java/_index.md"),
    ("apiref", "watermark-real.md", "english/java/com.aspose.words/watermark/_index.md"),
]:
    source = manifest.sources[kind]
    request = {
        "contract": manifest.contract, "plugin_id": manifest.plugin_id,
        "product_id": manifest.product_id, "language": manifest.language,
        "operation": "extract", "source_kind": kind, "repo_id": source.repo_id,
        "product_family": "aspose", "source_path": source.path + "/" + relative,
        "relative_repo_path": relative, "source_prefix": source.prefix,
        "layout_detection": source.layout, "source_revision": "deployment-fixture",
        "canonical_base_url": source.canonical_base_url,
        "raw_markdown": (fixtures / fixture).read_text(encoding="utf-8"),
    }
    result = subprocess.run(catalog.command(manifest.plugin_id, python=sys.executable),
                            input=json.dumps(request), text=True, capture_output=True, check=True)
    response = ExtractionResponse.model_validate_json(result.stdout)
    assert response.plugin_id == manifest.plugin_id
    assert response.result.chunk_records
    if kind == "apiref":
        assert response.result.symbols[0].member_fqn == "com.aspose.words.Watermark"

from fastapi import FastAPI
from fastapi.testclient import TestClient
from adcs.api.mcp_gateway import router
from adcs.mcp.tool_gateway import MCPToolGateway
app = FastAPI()
app.include_router(router)
app.state.apiref_symbol_service = None
app.state.mcp_tool_gateway = MCPToolGateway(
    public_query_service=Mock(), supported_revisions=("2025-11-25",), primary_revision="2025-11-25",
)
endpoint = "/words/java/mcp/v1/streamable-http"
with TestClient(app) as client:
    initialized = client.post(endpoint, json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    assert initialized.status_code == 200, "engine has no /words/java/mcp route; pin an engine with Java serving"
    assert initialized.json()["result"]["serverInfo"]["name"] == "aspose-words-java-mcp"
    tools = client.post(endpoint, json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    assert tools.status_code == 200
    for tool in tools.json()["result"]["tools"]:
        assert tool["inputSchema"]["properties"]["product_id"]["enum"] == ["aspose.words"]
        assert tool["inputSchema"]["properties"]["language"]["enum"] == ["java"]
print("Words/Java-only registration, retrieval profile, docs/API contracts and MCP endpoint verified")
