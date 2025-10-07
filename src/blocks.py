from PIL import Image
import numpy as np
import os
import json

def get_average_color(image_path):
    """Compute the average (R, G, B) color of an image, safely handling transparency."""
    img = Image.open(image_path).convert("RGBA")
    np_img = np.array(img)

    # Keep only pixels that have at least some opacity
    if np_img.shape[2] == 4:
        mask = np_img[:, :, 3] > 10  # allow semi-transparent pixels too
        if not np.any(mask):
            print(f"⚠️ Skipping {os.path.basename(image_path)} — no visible pixels.")
            return None
        np_img = np_img[mask][:, :3]
    else:
        np_img = np_img[:, :, :3].reshape(-1, 3)

    avg = np.mean(np_img, axis=0)
    if np.isnan(avg).any():
        print(f"⚠️ Skipping {os.path.basename(image_path)} — invalid average color.")
        return None

    return tuple(map(int, avg))



def generate_block_color_json(blocks_dir="data/blocks", output_file="data/block_colors.json"):
    """Generate a JSON file mapping block names to average RGB values."""
    color_data = {}

    for filename in os.listdir(blocks_dir):
        if not filename.endswith(".png"):
            continue

        block_name = os.path.splitext(filename)[0]  # e.g., stone.png → stone
        image_path = os.path.join(blocks_dir, filename)
        avg_color = get_average_color(image_path)
        color_data[block_name] = avg_color
        print(f"Processed {block_name}: {avg_color}")

    with open(output_file, "w") as f:
        json.dump(color_data, f, indent=4)

    print(f"\n✅ Saved {len(color_data)} block colors → {output_file}")


if __name__ == "__main__":
    generate_block_color_json()
