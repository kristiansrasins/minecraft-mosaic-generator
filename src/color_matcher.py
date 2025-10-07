import json
import numpy as np
from sklearn.neighbors import KDTree

class ColorMatcher:
    def __init__(self, json_path="data/block_colors.json"):
        # Load block color JSON
        with open(json_path, "r") as f:
            data = json.load(f)

        # Keep only valid RGB entries
        filtered = {k: v for k, v in data.items() if isinstance(v, list) and len(v) == 3}

        self.block_names = list(filtered.keys())
        self.colors = np.array(list(filtered.values()), dtype=np.uint8)  # shape: (N, 3)

        # Build KDTree for fast nearest-neighbor lookup
        self.tree = KDTree(self.colors)

    def find_nearest_block(self, rgb):
        """
        Given an RGB tuple, return the nearest Minecraft block name.
        """
        dist, index = self.tree.query([rgb], k=1)
        return self.block_names[index[0][0]], dist[0][0]


if __name__ == "__main__":
    matcher = ColorMatcher()
    test_rgb = (3, 252, 3)
    block, distance = matcher.find_nearest_block(test_rgb)
    print(f"Closest block to {test_rgb} → {block} (distance={distance:.2f})")
