#!/usr/bin/env python
"""Push all tracked files to GitHub via API (for when git protocol is blocked)."""
import os, json, base64, urllib.request, sys

TOKEN = sys.argv[1]
REPO = "qian-gugugaga/-Character_Skill_Producer"
API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json",
}

def api(method, path, data=None):
    url = f"{API}/repos/{REPO}/git{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, body, HEADERS, method=method)
    return json.loads(urllib.request.urlopen(req).read())

# Step 1: Create blobs
blobs = {}
root = "C:/Users/86182/Desktop/csp"
files = [
    ".gitignore", "PRD.md", "README.md", "SKILL.md",
    "examples/takamatsu-tomori/SKILL.md",
    "examples/takamatsu-tomori/references/research/01-setting.md",
    "examples/takamatsu-tomori/references/research/02-personality.md",
    "examples/takamatsu-tomori/references/research/03-expression.md",
    "examples/takamatsu-tomori/references/research/04-relationships.md",
    "examples/takamatsu-tomori/references/research/05-key-scenes.md",
    "references/distillation-framework.md",
    "references/skill-template.md",
    "scripts/merge_research.py",
    "scripts/quality_check.py",
]

for f in files:
    path = os.path.join(root, f)
    content = open(path, "rb").read()
    result = api("POST", "/blobs", {"content": base64.b64encode(content).decode(), "encoding": "base64"})
    blobs[f] = result["sha"]
    print(f"  blob: {f} → {result['sha'][:7]}")

# Step 2: Create tree
tree_items = []
for f, sha in blobs.items():
    tree_items.append({"path": f, "mode": "100644", "type": "blob", "sha": sha})

tree = api("POST", "/trees", {"tree": tree_items})
tree_sha = tree["sha"]
print(f"  tree: {tree_sha[:7]}")

# Step 3: Get current HEAD as parent
try:
    head = api("GET", "/refs/heads/main")
    parent_sha = head["object"]["sha"]
    print(f"  parent: {parent_sha[:7]}")
except urllib.error.HTTPError:
    parent_sha = None
    print("  no parent (empty repo)")

# Step 4: Create commit
commit_msg = "CSP v1.0 — Character Skill Producer\n\nWeb-search-first behavioral distillation for anime/game character role-playing skills.\nIncludes meta-skill, PRD, distillation framework, skill template, quality scripts,\nand a complete example (Takamatsu Tomori from BanG Dream! It's MyGO!!!!!)."
commit_data = {
    "message": commit_msg,
    "tree": tree_sha,
}
if parent_sha:
    commit_data["parents"] = [parent_sha]

commit = api("POST", "/commits", commit_data)
commit_sha = commit["sha"]
print(f"  commit: {commit_sha[:7]}")

# Step 5: Update ref
api("PATCH", "/refs/heads/main", {"sha": commit_sha, "force": False})
print(f"\nDone! https://github.com/{REPO}")
