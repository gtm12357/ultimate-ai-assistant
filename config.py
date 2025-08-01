# config.py

import os
from dotenv import load_dotenv

def get_mcp_config():
    """
    Loads API keys from the .env file and returns the complete,
    correct MCP configuration dictionary. This is the single source of truth.
    """
    load_dotenv()

    # Load all necessary API keys from the environment
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    BROWSERBASE_API_KEY = os.getenv("BROWSERBASE_API_KEY")
    BROWSERBASE_PROJECT_ID = os.getenv("BROWSERBASE_PROJECT_ID")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
    RAGIE_API_KEY = os.getenv("RAGIE_API_KEY")

    # Define the full, correct configuration
    config = {
      "mcpServers": {
          "browserbase": {
            "command": "node",
            "args": [
                "F:/ai-engineering-projects/MCPs/mcp-server-browserbase/cli.js",
                "--modelName", "openai/gpt-4o",
                "--modelApiKey", OPENAI_API_KEY
            ],
            "env": {
                "BROWSERBASE_API_KEY": BROWSERBASE_API_KEY,
                "BROWSERBASE_PROJECT_ID": BROWSERBASE_PROJECT_ID
            }
        },
        "mcp-server-firecrawl": {
            "command": "npx",
            "args": ["-y", "firecrawl-mcp"],
            "env": {
              "FIRECRAWL_API_KEY": FIRECRAWL_API_KEY
            }
          },
          "graphiti": {
            "transport": "sse",
            "url": "http://localhost:8000/sse"
          },
          "ragie": {
            "command": "npx",
            "args": [
              "-y",
              "@ragieai/mcp-server",
              "--partition",
              "your-real-ragie-partition-id" # <-- IMPORTANT: Use your real partition ID
            ],
            "env": {
              "RAGIE_API_KEY": RAGIE_API_KEY
            }
        },
        "mcp-git-ingest": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/adhikasp/mcp-git-ingest", "mcp-git-ingest"]
          },
        "desktop-commander": {
          "command": "npx",
          "args": [
            "-y",
            "@wonderwhy-er/desktop-commander"
          ]
        }
      }
    }
    return config