# Changelog

All notable changes to the Poe o3 MCP Server will be documented in this file.

## [1.1.0] - 2025-04-23

### Added
- Model selection via flags feature
  - Add `--ModelName` flags anywhere in your prompt to use a specific model
  - Example: `--Claude-3.5-Sonnet Tell me about quantum computing`
  - Default model remains "o3" when no flag is specified
- Test script for model flag parsing (`test_model_flag.py`)
- Improved documentation with model selection examples

### Changed
- Updated README with model selection feature documentation
- Improved error messages to be more specific about which model is being used

## [1.0.0] - 2025-04-23

### Added
- Initial release of Poe o3 MCP Server
- Basic MCP server implementation using FastMCP
- Integration with Poe's API to access the o3 model
- Asynchronous request handling
- Error handling and logging
- Example script for demonstrating usage