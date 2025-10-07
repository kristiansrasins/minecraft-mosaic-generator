# minecraft-mosaic-generator
Tool to convert any image in to a minecraft block mosaic.

## Features
- Uses real Minecraft block textures to compute average colors
- Maps input image pixels to nearest block colors
- Generates a mosaic image or exportable Minecraft build file (WIP)

## Setup
```bash
git https://github.com/kristiansrasins/minecraft-mosaic-generator
cd minecraft-image-mapper
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
