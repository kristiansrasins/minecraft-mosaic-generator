from PIL import Image
import numpy as np
from color_matcher import ColorMatcher
import argparse
import os
from skimage import color

def snap_to_multiple_of_16(value):
    return max(16, (value // 16) * 16)

def generate_minecraft_mosaic(input_image_path, output_image_path,
                              commands_file=None, start_x=0, start_y=0, start_z=0,
                              width=128, height=None):
    """
    Generate a Minecraft-style mosaic PNG and optional /setblock commands.
    Mosaic is placed flat on the ground (X-Z plane).
    """
    matcher = ColorMatcher()

    # --- Precompute RGB palette from Lab (gamut-safe) ---
    lab_colors = matcher.lab_colors.copy()
    lab_colors[:, 0] = np.clip(lab_colors[:, 0], 0, 100)   # L*
    lab_colors[:, 1] = np.clip(lab_colors[:, 1], -80, 80)  # a*
    lab_colors[:, 2] = np.clip(lab_colors[:, 2], -80, 80)  # b*

    # Convert Lab → RGB
    rgb_colors = color.lab2rgb(lab_colors.reshape(-1,1,3))
    # Gamut compression
    max_val = rgb_colors.max()
    if max_val > 1.0:
        rgb_colors /= max_val
    rgb_colors = np.clip(rgb_colors * 255, 0, 255).astype(np.uint8)

    # --- Load input image ---
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

            # --- Set mosaic pixel color for preview ---
            if block_name in matcher.block_names:
                idx = matcher.block_names.index(block_name)
                mosaic_array[y, x] = rgb_colors[idx, 0]
            else:
                mosaic_array[y, x] = np.array([255, 255, 255], dtype=np.uint8)

            # --- Add Minecraft setblock command ---
            if commands_file:
                mx = start_x + x
                my = start_y  # fixed Y, flat on ground
                mz = start_z + (height - 1 - y)  # image top → negative Z
                commands.append(f"setblock {mx} {my} {mz} minecraft:{block_name}")

    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    if commands_file:
        os.makedirs(os.path.dirname(commands_file), exist_ok=True)

    # Save mosaic PNG
    mosaic_img = Image.fromarray(mosaic_array.astype(np.uint8))
    mosaic_img.save(output_image_path)
    print(f"✅ Mosaic PNG saved to {output_image_path} ({width}×{height})")

    # Save /setblock commands
    if commands_file:
        with open(commands_file, "w") as f:
            f.write("\n".join(commands))
        print(f"✅ {len(commands)} /setblock commands saved to {commands_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Minecraft mosaic PNG and optional setblock commands")
    parser.add_argument("input_image", help="Path to input image")
    parser.add_argument("output_image", help="Path to save mosaic PNG")
    parser.add_argument("--commands", help="Optional path to save .mcfunction commands")
    parser.add_argument("--x", type=int, default=-200, help="Starting X coordinate")
    parser.add_argument("--y", type=int, default=-60, help="Starting Y coordinate")
    parser.add_argument("--z", type=int, default=-100, help="Starting Z coordinate")
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
