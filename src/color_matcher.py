import json
import numpy as np
from sklearn.neighbors import KDTree
from skimage import color  # perceptual color conversions

class ColorMatcher:
    def __init__(self, json_path="data/block_colors.json", mapping_path="data/texture_to_block.json"):
        # Load block color JSON
        with open(json_path, "r") as f:
            data = json.load(f)

        valid_data = {k: v for k, v in data.items() if isinstance(v, (list, tuple)) and len(v) == 3}
        self.block_names = list(valid_data.keys())
        rgb_colors = np.array(list(valid_data.values()), dtype=np.float32) / 255.0

        # Lab conversion
        self.lab_colors = color.rgb2lab(rgb_colors.reshape(1, -1, 3)).reshape(-1, 3)

        # KDTree
        self.tree = KDTree(self.lab_colors)

        # Load texture → placeable block mapping
        try:
            with open(mapping_path, "r") as f:
                self.texture_to_block = json.load(f)
        except FileNotFoundError:
            self.texture_to_block = {}  # fallback to identity mapping

    def find_nearest_block(self, rgb):
        rgb = np.array(rgb, dtype=np.float32) / 255.0
        lab = color.rgb2lab([[rgb]])[0, 0]

        weights = np.array([1.2, 1.0, 1.0])
        weighted_lab = self.lab_colors * weights
        weighted_pixel = lab * weights

        dist, index = self.tree.query([weighted_pixel], k=1)
        block_name = self.block_names[index[0][0]]

        # Map to a valid placeable block if a mapping exists
        block_name = self.texture_to_block.get(block_name, block_name)

        return block_name, float(dist[0][0])
