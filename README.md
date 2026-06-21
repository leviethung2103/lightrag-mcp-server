# LightRAG FastMCP Bridge

This project exposes a FastMCP server that proxies to an existing LightRAG Server API.

## Prerequisites

Before running this FastMCP bridge, you need to have a LightRAG server running. Follow the setup instructions below to install and configure the LightRAG server.

### LightRAG Server Setup

#### Option 1: Quick Install with uv (Recommended)

```bash
# Install LightRAG Server as a tool
uv tool install "lightrag-hku[api]"

# Build front-end artifacts
cd lightrag_webui
bun install --frozen-lockfile
bun run build
cd ..

# Setup environment file
# Download env.example from https://github.com/HKUDS/LightRAG/blob/main/env.example
# or use the interactive setup wizard
cp env.example .env

# Edit .env with your LLM and embedding configurations
# At minimum, configure:
# - OPENAI_API_KEY or your preferred LLM provider
# - EMBEDDING_MODEL (e.g., BAAI/bge-m3)

# Launch the LightRAG server (default: http://localhost:9621)
lightrag-server
```

#### Option 2: Install from Source

```bash
# Clone the LightRAG repository
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG

# Bootstrap the development environment
make dev
source .venv/bin/activate  # Linux/macOS
# Or on Windows: .venv\Scripts\activate

# Setup environment file
make env-base  # Interactive setup wizard
# Or manually: cp env.example .env and edit it

# Launch the LightRAG server
lightrag-server
```

#### Option 3: Docker Compose

```bash
# Clone the LightRAG repository
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG

# Copy and configure environment file
cp env.example .env
# Edit .env with your LLM and embedding configurations

# Start with Docker Compose
docker compose up
```

**Note:** By default, the LightRAG server runs on `http://localhost:9621`. Make sure the server is accessible before running this FastMCP bridge.

For more detailed information about LightRAG configuration and options, visit the [LightRAG repository](https://github.com/HKUDS/LightRAG).

## Environment

- `LIGHTRAG_BASE_URL` - LightRAG API base URL, for example `http://localhost:9621`
- `LIGHTRAG_API_KEY` - optional bearer token used for `/login`-protected routes
- `MCP_TRANSPORT` - `stdio`, `sse`, or `streamable-http` (default: `streamable-http`)
- `MCP_HOST` - bind host for HTTP transports (default: `0.0.0.0`)
- `MCP_PORT` - bind port for HTTP transports (default: `3000`)

## Run

```bash
python -m lightrag_fastmcp_bridge.server
```

## Docker

```bash
docker build -t lightrag-fastmcp .
docker run --rm -p 3000:3000 \
  -e LIGHTRAG_BASE_URL=http://host.docker.internal:9621 \
  lightrag-fastmcp
```

If you want SSE transport instead of streamable HTTP, set `MCP_TRANSPORT=sse`.
