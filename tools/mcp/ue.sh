#!/usr/bin/env bash
# Cliente mínimo del MCP oficial de Unreal (HTTP local). Uso:
#   ue.sh list_toolsets
#   ue.sh describe_toolset '{"toolset":"..."}'
#   ue.sh call_tool '{"toolset":"...","tool":"...","arguments":{...}}'
#   ue.sh raw <method> '<params json>'
set -euo pipefail
U=${UE_MCP_URL:-http://127.0.0.1:8000/mcp}
S=${XDG_RUNTIME_DIR:-/tmp}/ue-mcp-session
H=(-H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream')
init() {
  curl -s -D - -o /dev/null "${H[@]}" "$U" -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"ue.sh","version":"1"}}}' \
    | tr -d '\r' | awk -F': ' 'tolower($1)=="mcp-session-id"{print $2}' > "$S"
  curl -s -o /dev/null "${H[@]}" -H "Mcp-Session-Id: $(cat "$S")" "$U" -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
}
[ -s "$S" ] || init
rpc() { curl -s "${H[@]}" -H "Mcp-Session-Id: $(cat "$S")" "$U" -d "$1"; }
if [ "$1" = raw ]; then body="{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"$2\",\"params\":${3:-{\}}}"
else body="{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":${2:-{\}}}}"; fi
out=$(rpc "$body")
if echo "$out" | grep -qi 'session'; then init; out=$(rpc "$body"); fi
echo "$out"
