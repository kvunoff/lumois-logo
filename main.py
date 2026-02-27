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
    ("logo[whiteLtransB]", "white", None, None),
    ("logo[blackLtransB]", "black", None, None),
    ("logo[whiteLblackB]", "white", "black", "full"),
    ("logo[blackLwhiteB]", "black", "white", "full"),
    ("platelogo[whiteLblackB]", "white", "black", "squircle"),
    ("platelogo[blackLwhiteB]", "black", "white", "squircle"),
]

num_rays = 8
radius = 1.5
arc_width = 0.5
arc_depth = 1
roundness = 0
line_width = 8
dpi = 600
output_size = 6

plate_offset = -2.2
plate_size = 4.4
rounding = 0.7

def create_arc(width, depth, roundness):
    verts = [
        (-width/2, 0),
        (-width/2 + width*roundness, -depth),
        ( width/2 - width*roundness, -depth),
        ( width/2, 0),
    ]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    return Path(verts, codes)

def generate_logo(base_filename, color, background, bg_type):
    fig, ax = plt.subplots(figsize=(output_size, output_size), dpi=dpi)
    
    ax.set_aspect('equal')
    ax.axis('off')

    if bg_type == "full":
        fig.patch.set_facecolor(background)
        fig.patch.set_alpha(1.0)
        ax.set_facecolor(background)
        transparent = False
    elif bg_type == "squircle":
        fig.patch.set_alpha(0)
        ax.set_facecolor((0,0,0,0))
        box = patches.FancyBboxPatch(
            (plate_offset, plate_offset), plate_size, plate_size,
            boxstyle=f"round,pad=0,rounding_size={rounding}",
            facecolor=background,
            edgecolor='none',
            zorder=0
        )
        ax.add_patch(box)
        transparent = True
    else:
        fig.patch.set_alpha(0)
        ax.set_facecolor((0,0,0,0))
        transparent = True

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
            capstyle='round',
            zorder=1
        )

        transform = (
            Affine2D()
            .rotate(angle + np.pi/2 + np.pi)
            .translate(x, y)
            + ax.transData
        )

        patch.set_transform(transform)
        ax.add_patch(patch)

    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.7, 2.7)

    for ext in ['png', 'svg']:
        plt.savefig(
            f"{base_filename}.{ext}",
            dpi=dpi,
            transparent=transparent,
            bbox_inches='tight',
            pad_inches=0.1
        )
    
    plt.close()
    print(f"✅ Generated: {base_filename}")

# =======================
# RUN
# =======================

if __name__ == "__main__":
    folder = "output_logos"
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chdir(folder)
    
    print("🎨 Generating Lumos Logo Pack...")
    for name, color, bg, bg_type in variants:
        generate_logo(name, color, bg, bg_type)
    print(f"\n✨ Done! All 6 variants are in '{folder}/'")