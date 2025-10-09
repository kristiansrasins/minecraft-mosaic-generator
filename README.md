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
```

## Usage
1. Add picture to examples folder
2. Change default x/y/z cords at end of mosaic.py file
3. Run mosaic.py with picture path and needed width and height parameters 
```bash
python src/mosaic.py data/examples/picutre.png data/examples/mosaic.png --commands data/examples/mosaic.mcfunction --width 200 --height 200
```
4. Create a minecraft datapack and create a function with the mosaic.function file (you can follow an existing tutorial for this)
5. Run the function ingame.