from client import PersonalKnowledgeVaultGraphCompiler
import json

vault = PersonalKnowledgeVaultGraphCompiler()
print("=== PERSONAL KNOWLEDGE VAULT GRAPH BENCHMARK ===")
res = vault.run_vault_benchmark()
print(json.dumps(res, indent=2))
