"""Generate Sprunki character sprites as simple PNG images."""
from PIL import Image, ImageDraw
import os

os.makedirs("images", exist_ok=True)

# Character definitions: name, body_color, size
CHARS = [
    ("raddy",     (229, 57, 53),   (183, 28, 28)),      # Red - Raddy
    ("garnold",   (249, 168, 37),  (199, 145, 0)),       # Gold - Garnold
    ("black",     (30, 30, 30),    (0, 0, 0)),           # Black
    ("gray",      (160, 160, 176), (112, 112, 128)),     # Gray
    ("funbot",    (176, 190, 197), (120, 144, 156)),     # Silver - Fun Bot
    ("sky",       (79, 195, 247),  (2, 136, 209)),       # Sky Blue
    ("oren",      (255, 152, 0),   (230, 81, 0)),        # Orange - Oren
    ("mrsun",     (255, 193, 7),   (245, 127, 23)),      # Gold - Mr Sun
    ("mrtree",    (121, 85, 72),   (78, 52, 46)),        # Brown - Mr Tree
    ("jevin",     (30, 58, 138),   (15, 29, 92)),        # Blue - Jevin
    ("pinki",     (244, 143, 177), (194, 24, 91)),       # Pink - Pinki
    ("doghead",   (139, 90, 43),   (101, 67, 33)),       # Dog head
]

def draw_sprunki_body(draw, cx, cy, r, body_color, dark_color):
    """Draw a Sprunki-style rounded body"""
    bw, bh = r * 2.4, r * 3.0
    x0, y0 = cx - bw/2, cy - bh/2
    
    # Rounded rect body
    br = r * 0.7
    draw.rounded_rectangle([x0, y0, x0+bw, y0+bh], radius=br, fill=body_color, outline=dark_color, width=3)
    
    # Arms
    arm_r = r * 0.36
    for side in [-1, 1]:
        ax = cx + side * (bw/2 + arm_r * 0.3)
        ay = cy - bh * 0.3
        draw.ellipse([ax-arm_r, ay-arm_r, ax+arm_r, ay+arm_r], fill=body_color, outline=dark_color, width=2)
    
    # Face area
    face_y = cy - bh * 0.22
    eye_sp = bw * 0.16
    eye_r = r * 0.22
    
    # Eyes white
    for side in [-1, 1]:
        ex = cx + side * eye_sp
        draw.ellipse([ex-eye_r, face_y-eye_r, ex+eye_r, face_y+eye_r], fill="white", outline=dark_color, width=1)
        # Pupil
        pr = eye_r * 0.55
        draw.ellipse([ex-pr, face_y-pr, ex+pr, face_y+pr], fill=dark_color)
    
    # Simple smile
    mouth_y = face_y + r * 0.5
    draw.arc([cx-r*0.2, mouth_y-r*0.15, cx+r*0.2, mouth_y+r*0.15], 20, 160, fill=dark_color, width=2)

for name, body_color, dark_color in CHARS:
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if name == "doghead":
        # Dog head - simple dog face
        cx, cy = size/2, size/2
        r = 55
        # Head circle
        draw.ellipse([cx-r, cy-r*0.8, cx+r, cy+r*0.8], fill=body_color, outline=dark_color, width=3)
        # Ears
        for ex in [cx-r*0.7, cx+r*0.7]:
            draw.ellipse([ex-r*0.35, cy-r*1.2, ex+r*0.35, cy-r*0.3], fill=body_color, outline=dark_color, width=2)
        # Eyes
        for ex in [cx-r*0.3, cx+r*0.3]:
            draw.ellipse([ex-r*0.13, cy-r*0.1-r*0.13, ex+r*0.13, cy-r*0.1+r*0.13], fill=dark_color)
            draw.ellipse([ex-r*0.04, cy-r*0.1-r*0.06, ex+r*0.04, cy-r*0.1+r*0.02], fill="white")
        # Nose
        draw.ellipse([cx-r*0.08, cy+r*0.05, cx+r*0.08, cy+r*0.2], fill=dark_color)
        # Mouth
        draw.arc([cx-r*0.2, cy+r*0.05, cx, cy+r*0.35], 180, 360, fill=dark_color, width=2)
        draw.arc([cx, cy+r*0.05, cx+r*0.2, cy+r*0.35], 180, 360, fill=dark_color, width=2)
        # Cage bars
        for bx in [cx-r*0.7, cx-r*0.35, cx, cx+r*0.35, cx+r*0.7]:
            draw.line([bx, cy-r*1.2, bx, cy+r*0.5], fill=(80,80,80), width=2)
    else:
        draw_sprunki_body(draw, size/2, size/2, 42, body_color, dark_color)
    
    img.save(f"images/{name}.png")
    print(f"  Created images/{name}.png ({size}x{size})")

print("Done! Generated 12 character sprites.")
