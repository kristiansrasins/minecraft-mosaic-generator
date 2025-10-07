import os
import json

# -----------------------------
BLOCKS_DIR = "data/blocks"
OUTPUT_JSON = "data/texture_to_block.json"

# Suffixes to strip for guessing block names
SUFFIXES_TO_STRIP = ["_top", "_bottom", "_side", "_overlay"]

# Optional: manual overrides for known edge cases
MANUAL_OVERRIDES = {
    "dried_ghast_hydration_3": "air",
    "acacia_door_bottom": "acacia_door",
    "acacia_door_top": "acacia_door",
    "white_stained_glass_pane_top": "white_stained_glass_pane",
    # Add more overrides here as needed
}

# -----------------------------
def guess_block_name(texture_name):
    # Apply manual override first
    if texture_name in MANUAL_OVERRIDES:
        return MANUAL_OVERRIDES[texture_name]

    # Strip known suffixes
    for suffix in SUFFIXES_TO_STRIP:
        if texture_name.endswith(suffix):
            return texture_name[: -len(suffix)]

    # Default: use texture name as block name
    return texture_name

# -----------------------------
def generate_texture_to_block_map(blocks_dir=BLOCKS_DIR):
    mapping = {}
    for filename in os.listdir(blocks_dir):
        if not filename.endswith(".png"):
            continue

        texture_name = os.path.splitext(filename)[0]
        block_name = guess_block_name(texture_name)
        mapping[texture_name] = block_name

    return mapping

# -----------------------------
if __name__ == "__main__":
    mapping = generate_texture_to_block_map()
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(mapping, f, indent=4)
    print(f"✅ Generated texture-to-block mapping → {OUTPUT_JSON}")
