import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
import os

# =======================
# CONFIGURATION
# =======================

variants = [
    ("logo[whiteLtransB]", "white", None),
    ("logo[blackLtransB]", "black", None),
    ("logo[whiteLblackB]", "white", "black"),
    ("logo[blackLwhiteB]", "black", "white"),
]

num_rays = 8
radius = 1.5
arc_width = 0.5
arc_depth = 1
roundness = 0
line_width = 8
dpi = 600
output_size = 6

def create_arc(width, depth, roundness):
    verts = [
        (-width/2, 0),
        (-width/2 + width*roundness, -depth),
        ( width/2 - width*roundness, -depth),
        ( width/2, 0),
    ]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    return Path(verts, codes)

def generate_logo(base_filename, color, background):
    fig, ax = plt.subplots(figsize=(output_size, output_size), dpi=dpi)
    
    if background:
        fig.patch.set_facecolor(background)
        ax.set_facecolor(background)
    
    ax.set_aspect('equal')
    ax.axis('off')

    arc_path = create_arc(arc_width, arc_depth, roundness)

    for i in range(num_rays):
        angle = 2 * np.pi * i / num_rays
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)

        patch = patches.PathPatch(
            arc_path,
            fill=False,
            lw=line_width,
            edgecolor=color,
            capstyle='round'
        )

        transform = (
            Affine2D()
            .rotate(angle + np.pi/2 + np.pi)
            .translate(x, y)
            + ax.transData
        )

        patch.set_transform(transform)
        ax.add_patch(patch)

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)

    plt.savefig(
        f"{base_filename}.png",
        dpi=dpi,
        transparent=(background is None),
        bbox_inches='tight',
        pad_inches=0.1
    )
    
    plt.savefig(
        f"{base_filename}.svg",
        transparent=(background is None),
        bbox_inches='tight',
        pad_inches=0.1
    )
    
    plt.close()
    print(f"✅ Generated: {base_filename} (PNG & SVG)")

# =======================
# RUN GENERATION
# =======================

if __name__ == "__main__":
    os.makedirs("output_logos", exist_ok=True)
    os.chdir("output_logos")
    
    print("🚀 Starting Lumos Identity Generation...")
    
    for name, color, bg in variants:
        generate_logo(name, color, bg)
        
    print("\n✨ All logos saved in 'output_logos' folder.")