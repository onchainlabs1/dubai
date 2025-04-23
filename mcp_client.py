"""Minimal MCP client (HTTP POST wrapper)."""
import requests

class MCPClient:
    def __init__(self, server_url: str):
        self.base = server_url.rstrip("/")

    def call(self, endpoint: str, payload: dict):
        url = f"{self.base}/{endpoint}"
        try:
            r = requests.post(url, json=payload, timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as exc:
            print("[MCP] error:", exc)
            return {"error": str(exc)}