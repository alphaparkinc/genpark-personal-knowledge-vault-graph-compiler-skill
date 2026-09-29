import sys, json
from client import PersonalKnowledgeVaultGraphCompiler

def handle_mcp():
    vault = PersonalKnowledgeVaultGraphCompiler()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(vault.run_vault_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-personal-knowledge-vault-graph-compiler-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "index_note", "description": "Index note and extract [[wikilinks]].", "inputSchema": {"type": "object", "properties": {"note_id": {"type": "string"}, "title": {"type": "string"}, "content": {"type": "string"}}}},
                    {"name": "query_backlinks", "description": "Query backlinks for a note.", "inputSchema": {"type": "object", "properties": {"note_id_or_title": {"type": "string"}}}},
                    {"name": "compute_vault_analytics", "description": "Compute vault graph analytics and centrality.", "inputSchema": {"type": "object"}},
                    {"name": "run_vault_benchmark", "description": "Run knowledge vault graph benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "index_note":
                    res = vault.index_note(args.get("note_id", "n"), args.get("title", ""), args.get("content", ""))
                elif tname == "query_backlinks":
                    res = vault.query_backlinks(args.get("note_id_or_title", ""))
                elif tname == "compute_vault_analytics":
                    res = vault.compute_vault_analytics()
                else:
                    res = vault.run_vault_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
