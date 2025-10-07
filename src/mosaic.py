from PIL import Image
import numpy as np
from color_matcher import ColorMatcher
import argparse
import os
import json

def snap_to_multiple_of_16(value):
    return max(16, (value // 16) * 16)

# -----------------------------
# Load texture → block mapping
# -----------------------------
TEXTURE_TO_BLOCK_JSON = "data/texture_to_block.json"
with open(TEXTURE_TO_BLOCK_JSON) as f:
    TEXTURE_TO_BLOCK = json.load(f)

# -----------------------------
def generate_minecraft_mosaic(input_image_path, output_image_path,
                              commands_file=None, start_x=0, start_y=-64, start_z=0,
                              width=128, height=None):
    """
    Generate a Minecraft-style mosaic PNG and optionally /setblock commands.
    Maps texture names to valid Minecraft block IDs using texture_to_block.json.
    """
    matcher = ColorMatcher()
    img = Image.open(input_image_path).convert("RGB")

    # Snap dimensions to multiples of 16
    width = snap_to_multiple_of_16(width)
    if height is None:
        height = snap_to_multiple_of_16(img.height * width // img.width)
    else:
        height = snap_to_multiple_of_16(height)

    img = img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = np.array(img)
    mosaic_array = np.zeros_like(pixels)
    commands = []

    for y in range(height):
        for x in range(width):
            rgb = tuple(pixels[y, x])
            block_name, _ = matcher.find_nearest_block(rgb)

            # Map to valid Minecraft block ID via JSON
            block_name = TEXTURE_TO_BLOCK.get(block_name, "air")

            # Determine pixel color safely
            if block_name in matcher.block_names:
                block_color = matcher.colors[matcher.block_names.index(block_name)]
            else:
                block_color = np.array([255, 255, 255])  # white fallback

            mosaic_array[y, x] = block_color

            # Add /setblock command
            if commands_file:
              mx = start_x + x          # X-axis = image width
              my = -60              # Y-axis = ground level
              mz = start_z + (height - 1 - y)  # Z-axis = image height (invert for top-to-bottom)
              commands.append(f"setblock {mx} {my} {mz} minecraft:{block_name}")


    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    if commands_file:
        dir_path = os.path.dirname(commands_file)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

    # Save PNG
    mosaic_img = Image.fromarray(mosaic_array.astype(np.uint8))
    mosaic_img.save(output_image_path)
    print(f"✅ Mosaic PNG saved to {output_image_path} ({width}×{height})")

    # Save commands
    if commands_file:
        with open(commands_file, "w") as f:
            f.write("\n".join(commands))
        print(f"✅ {len(commands)} /setblock commands saved to {commands_file}")


# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Minecraft mosaic PNG and optional setblock commands")
    parser.add_argument("input_image", help="Path to input image")
    parser.add_argument("output_image", help="Path to save mosaic PNG")
    parser.add_argument("--commands", help="Optional path to save .mcfunction commands")
    parser.add_argument("--x", type=int, default=0, help="Starting X coordinate")
    parser.add_argument("--y", type=int, default=64, help="Starting Y coordinate")
    parser.add_argument("--z", type=int, default=0, help="Starting Z coordinate")
    parser.add_argument("--width", type=int, default=128, help="Width of mosaic in blocks")
    parser.add_argument("--height", type=int, default=None, help="Height of mosaic in blocks")
    args = parser.parse_args()

    generate_minecraft_mosaic(
        args.input_image,
        args.output_image,
        args.commands,
        args.x,
        args.y,
        args.z,
        args.width,
        args.height
    )
