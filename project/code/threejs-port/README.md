# Log Spiral Visualization

A 3D logarithmic spiral visualization built with **Three.js** and **Vite**.

This is a JavaScript port of the original Python/Panda3D project.

![Log Spiral](https://via.placeholder.com/800x400/0a0a1a/00f0ff?text=LogSpiral+Visualization)

## Features

- **Interactive 3D logarithmic spiral curve** with adjustable parameters
- **Model loading** - Import your own `.obj` or `.stl` files
- **Animated camera** that follows the spiral path
- **Real-time parameter controls** via lil-gui
- **Modern, dark-themed UI** with accent lighting
- **Keyboard shortcuts** for quick access

## Mathematical Background

The logarithmic spiral (equiangular spiral) is defined by:

```
r = a × e^(k×θ)
```

Where:
- `a` - Initial radius/scale factor
- `k` - Growth rate (spiral tightness)  
- `θ` - Angle in radians

The 3D version adds height using the natural logarithm:
```
z = heightScale² × ln(θ) + lowerBound
```

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later recommended)

### Installation

```bash
# Navigate to the project directory
cd code/threejs-port

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open automatically at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Controls

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `G` | Toggle animation along spiral |
| `C` | Toggle curve visibility |
| `H` | Toggle model visibility |
| `R` | Reset all parameters |

### Mouse Controls

- **Left drag** - Rotate camera
- **Right drag** - Pan camera
- **Scroll** - Zoom in/out

### GUI Parameters

#### Spiral Parameters
- **a coefficient** - Controls initial spiral radius (-3 to 3)
- **k coefficient** - Controls growth rate (0.01 to 1)
- **Radius Scale** - Overall radial scaling
- **Height Scale** - Vertical scaling
- **Lift** - Minimum height offset
- **Truncate** - How much of the inner spiral to skip

#### Viewing
- **Distance** - Camera distance from center (when not animating)
- **Angle** - Camera orbit angle (when not animating)
- **Animation Speed** - How fast the camera moves along the spiral
- **Model Scale** - Scale of the loaded 3D model

## Loading Custom Models

1. Click **"📁 Load Model"** in the GUI
2. Select an `.obj` or `.stl` file from your computer
3. Adjust scale as needed with the **Model Scale** slider

Sample models are available in `../models/`:
- `bunny.obj` - Stanford bunny
- `snowman.obj` - Snowman model
- `chicken.obj` - Chicken model
- `diamond.obj` - Diamond shape

## Project Structure

```
threejs-port/
├── index.html          # Entry HTML
├── package.json        # Dependencies & scripts
├── vite.config.js      # Vite configuration
├── public/
│   └── models/         # Place 3D models here
└── src/
    ├── main.js         # Main application
    ├── LogSpiral.js    # Spiral curve generator
    └── style.css       # Styling
```

## Tech Stack

- [Three.js](https://threejs.org/) - 3D graphics library
- [lil-gui](https://lil-gui.georgealways.com/) - Lightweight GUI controls
- [Vite](https://vitejs.dev/) - Fast build tool

## License

MIT

---

*Ported from the original Panda3D/Python implementation*

