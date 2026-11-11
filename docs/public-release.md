# Maintaining the public deployment

This repository uses public engine and plugin submodules with explicitly pinned commits.

## Update components

1. Fetch the desired revisions in `engine/` and `plugins/words-java/` and check out the commits you intend to release.
2. Run `./scripts/setup.sh`, fixture registration, and the plugin regression suite.
3. Review and commit both gitlink changes with any required deployment updates. Do not initialize nested historical source submodules recursively.

The engine pin must include Java serving (`com.<product>.` retrieval-profile symbols and the `/words/java/mcp` route).

GitHub Actions checks shell syntax and configuration, then installs the pinned engine and verifies registration and plugin tests. It does not deploy services or publish indexed content.

## Published companions

- [Context engine](https://github.com/aspose-core-mcp/context-engine)
- [Words/Java plugin](https://github.com/aspose-words-mcp/java-plugin)

The project uses the MIT license in the repository root. Preserve component licenses and third-party notices when distributing the deployment.
