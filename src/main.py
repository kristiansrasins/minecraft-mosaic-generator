from PIL import Image
import numpy as np
import argparse

def average_color(image_path):
    img = Image.open(image_path).convert('RGB')
    np_img = np.array(img)
    avg = np.mean(np_img.reshape(-1, 3), axis=0)
    return tuple(avg.astype(int))

def main():
    parser = argparse.ArgumentParser(description="Minecraft Image Mapper")
    parser.add_argument("image", help="Input image file")
    args = parser.parse_args()

    avg = average_color(args.image)
    print(f"Average color of {args.image}: {avg}")

if __name__ == "__main__":
    main()
