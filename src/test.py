import json

with open("data/block_colors.json") as f:
    data = json.load(f)

for k, v in data.items():
    if not isinstance(v, list) or len(v) != 3:
        print(f"❌ Skipping invalid entry {k}: {v}")
