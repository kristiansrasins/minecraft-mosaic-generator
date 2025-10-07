from PIL import Image
import numpy as np
from color_matcher import ColorMatcher
import argparse
import os

def snap_to_multiple_of_16(value):
    return max(16, (value // 16) * 16)

def generate_setblock_commands(input_image_path, output_file, start_x=0, start_y=64, start_z=0,
                               width=128, height=None):
    """
    Generate Minecraft /setblock commands for an image mosaic.

    Args:
        input_image_path: Path to input image
        output_file: Path to save .mcfunction or .txt
        start_x, start_y, start_z: Starting coordinates in Minecraft
        width: Number of blocks horizontally (multiple of 16)
        height: Number of blocks vertically (multiple of 16 or auto)
    """
    matcher = ColorMatcher()

    img = Image.open(input_image_path).convert("RGB")
    width = snap_to_multiple_of_16(width)
    if height is None:
        height = snap_to_multiple_of_16(img.height * width // img.width)
    else:
        height = snap_to_multiple_of_16(height)

    img = img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = np.array(img)

    commands = []

    for y in range(height):
        for x in range(width):
            rgb = tuple(pixels[y, x])
            block_name, _ = matcher.find_nearest_block(rgb)

            # Minecraft y axis is up, so we invert y for image top → Minecraft top
            mx = start_x + x
            my = start_y + (height - 1 - y)
            mz = start_z

            commands.append(f"setblock {mx} {my} {mz} minecraft:{block_name}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save commands to file
    with open(output_file, "w") as f:
        f.write("\n".join(commands))

    print(f"✅ {len(commands)} setblock commands saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Minecraft setblock commands from image")
    parser.add_argument("input_image", help="Input image path")
    parser.add_argument("output_file", help="Output .txt or .mcfunction file")
    parser.add_argument("--x", type=int, default=0, help="Starting X coordinate")
    parser.add_argument("--y", type=int, default=64, help="Starting Y coordinate")
    parser.add_argument("--z", type=int, default=0, help="Starting Z coordinate")
    parser.add_argument("--width", type=int, default=128, help="Width of mosaic in blocks")
    parser.add_argument("--height", type=int, default=None, help="Height of mosaic in blocks")
    args = parser.parse_args()

    generate_setblock_commands(args.input_image, args.output_file, args.x, args.y, args.z,
                               args.width, args.height)
