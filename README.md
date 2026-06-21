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

## Available Tools

This FastMCP bridge provides the following tools for interacting with your LightRAG server:

### Health & Status

| Tool | Description |
|------|-------------|
| `health()` | Check whether the LightRAG server is alive and responsive |

### Query Operations

| Tool | Description |
|------|-------------|
| `query(question, include_references, include_chunk_content)` | Run a LightRAG query and return the final response payload |
| `query_stream(question, include_references, include_chunk_content)` | Run a streamed LightRAG query and concatenate the streamed text |

### Document Insertion

| Tool | Description |
|------|-------------|
| `insert_text(text, file_source, title, metadata)` | Insert raw text into LightRAG knowledge base |
| `insert_texts(texts)` | Insert multiple text payloads into LightRAG in batch |

### Document Management

| Tool | Description |
|------|-------------|
| `scan_documents()` | Trigger a document scan to process uploaded files |
| `document_status_counts()` | Get counts of documents by processing status |
| `list_documents(page, page_size, status)` | List paginated documents with optional status filtering |
| `delete_document(doc_id)` | Delete a document by its ID |

### Pipeline & Tracking

| Tool | Description |
|------|-------------|
| `pipeline_state()` | Get the current ingestion pipeline state and progress |
| `get_track_status(track_id)` | Get detailed ingestion status for a specific track ID |

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
