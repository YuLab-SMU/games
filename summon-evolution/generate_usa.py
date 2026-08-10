"""Generate American cryptid (美国山海经) character sprites."""
from PIL import Image, ImageDraw
import random, math, os

os.makedirs("images", exist_ok=True)
rng = random.Random(42)

CHARS = [
    ("大脚怪", (139, 90, 43), (101, 67, 33), "bigfoot"),
    ("天蛾人", (40, 40, 50), (20, 20, 30), "mothman"),
    ("泽西恶魔", (80, 30, 30), (50, 10, 10), "jersey"),
    ("卓柏卡布拉", (60, 80, 40), (30, 50, 20), "chupa"),
    ("尼斯湖怪", (30, 100, 80), (15, 60, 45), "nessie"),
    ("弹簧腿杰克", (50, 50, 80), (30, 30, 60), "spring"),
    ("瘦长鬼影", (30, 30, 40), (15, 15, 25), "slender"),
    ("多佛恶魔", (100, 80, 70), (70, 50, 40), "dover"),
    ("温迪戈", (60, 50, 40), (40, 30, 20), "wendigo"),
    ("皮行者", (80, 60, 40), (50, 35, 20), "skinwalker"),
    ("雷鸟", (200, 180, 50), (160, 130, 20), "thunder"),
]

def draw_body(draw, cx, cy, r, body, dark):
    bw, bh = r*2.4, r*3.0
    br = r*0.7
    x0, y0 = cx-bw/2, cy-bh/2
    draw.rounded_rectangle([x0, y0, x0+bw, y0+bh], radius=br, fill=body, outline=dark, width=3)
    # Eyes
    eye_y, eye_sp, eye_r = cy-bh*0.3, bw*0.16, r*0.2
    for s in [-1, 1]:
        ex = cx+s*eye_sp
        draw.ellipse([ex-eye_r, eye_y-eye_r, ex+eye_r, eye_y+eye_r], fill="white", outline=dark, width=1)
        draw.ellipse([ex-eye_r*0.5, eye_y-eye_r*0.5, ex+eye_r*0.5, eye_y+eye_r*0.5], fill=dark)

for name, body, dark, fname in CHARS:
    size = 128
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx, cy = size/2, size/2
    r = 42
    bw, bh = r*2.4, r*3.0
    eye_y = cy - bh*0.3
    eye_sp = bw*0.16
    eye_r = r*0.2
    
    # Base body
    draw_body(draw, cx, cy, r, body, dark)
    
    # Character-specific features
    if fname == "bigfoot":
        # Bushy hair on top
        for i in range(5):
            draw.ellipse([cx-25+i*10, cy-bh/2-r*0.3, cx-5+i*10, cy-bh/2+r*0.1], fill=dark)
        # Big footprint below
        draw.ellipse([cx-15, cy+bh/2-5, cx+15, cy+bh/2+15], fill=dark)
    elif fname == "mothman":
        # Red glowing eyes
        for s in [-1, 1]:
            ex = cx+s*eye_sp
            draw.ellipse([ex-eye_r, eye_y-eye_r, ex+eye_r, eye_y+eye_r], fill=(200,40,40))
        # Wings
        for s in [-1, 1]:
            px0 = min(cx+s*5, cx+s*bw*0.7, cx+s*bw*0.9)
            px1 = max(cx+s*5, cx+s*bw*0.7, cx+s*bw*0.9)
            draw.polygon([(cx+s*5, cy-bh*0.2), (cx+s*bw*0.7, cy-bh*0.5), (cx+s*bw*0.9, cy), (cx+s*5, cy+bh*0.1)], fill=(50,50,60))
    elif fname == "jersey":
        # Horns
        for s in [-1, 1]:
            draw.polygon([(cx+s*10, cy-bh/2), (cx+s*25, cy-bh/2-20), (cx+s*30, cy-bh/2-5)], fill=dark)
        # Small wings
        for s in [-1, 1]:
            x1 = min(cx+s*25, cx+s*55)
            x2 = max(cx+s*25, cx+s*55)
            draw.ellipse([x1, cy-bh*0.3, x2, cy+bh*0.1], fill=(60,20,20), outline=dark, width=2)
    elif fname == "chupa":
        # Spikes on back
        for i in range(4):
            draw.polygon([(cx-15+i*10, cy-bh/2), (cx-10+i*10, cy-bh/2-15), (cx-5+i*10, cy-bh/2)], fill=dark)
        # Red eyes
        for s in [-1, 1]:
            ex = cx+s*eye_sp
            draw.ellipse([ex-eye_r, eye_y-eye_r, ex+eye_r, eye_y+eye_r], fill=(200,40,20))
    elif fname == "nessie":
        # Long neck
        draw.ellipse([cx-10, cy-bh/2-r*0.8, cx+10, cy-bh/2+r*0.1], fill=body, outline=dark, width=2)
        draw.ellipse([cx-8, cy-bh/2-r*1.0, cx+8, cy-bh/2-r*0.3], fill=body, outline=dark, width=2)
        # Flippers
        for s in [-1, 1]:
            fx1 = min(cx+s*25, cx+s*45)
            fx2 = max(cx+s*25, cx+s*45)
            draw.ellipse([fx1, cy+bh*0.1, fx2, cy+bh*0.4], fill=body, outline=dark, width=2)
    elif fname == "spring":
        # Top hat
        draw.rectangle([cx-12, cy-bh/2-15, cx+12, cy-bh/2], fill=(20,20,40))
        draw.rectangle([cx-18, cy-bh/2-3, cx+18, cy-bh/2], fill=(20,20,40))
        # Spring boots
        for s in [-1, 1]:
            draw.ellipse([cx+s*10-8, cy+bh/2-5, cx+s*10+8, cy+bh/2+10], fill=dark)
    elif fname == "slender":
        # Very tall, thin
        draw.rectangle([cx-bw*0.3, cy-bh/2-r*0.5, cx+bw*0.3, cy+bh/2], fill=body, outline=dark, width=2)
        # Suit tie
        draw.rectangle([cx-3, cy-bh*0.15, cx+3, cy-bh*0.05], fill=(50,50,50))
        # No face
    elif fname == "dover":
        # Big head
        draw.ellipse([cx-r*0.9, cy-bh/2-r*0.4, cx+r*0.9, cy-r*0.2], fill=body, outline=dark, width=2)
        # Large glowing eyes
        for s in [-1, 1]:
            ex = cx+s*eye_sp*1.3
            draw.ellipse([ex-eye_r*1.3, eye_y-eye_r*1.3, ex+eye_r*1.3, eye_y+eye_r*1.3], fill=(200,255,100))
    elif fname == "wendigo":
        # Antlers
        for s in [-1, 1]:
            for i in range(3):
                draw.line([(cx+s*8, cy-bh/2), (cx+s*35, cy-bh/2-30-i*8)], fill=dark, width=2)
        # Skull-like pale face
        draw.ellipse([cx-r*0.7, eye_y-r*0.8, cx+r*0.7, eye_y+r*0.5], fill=(220,210,200), outline=dark, width=1)
        # Dark eye sockets
        for s in [-1, 1]:
            draw.ellipse([cx+s*eye_sp-eye_r*0.8, eye_y-eye_r*0.5, cx+s*eye_sp+eye_r*0.8, eye_y+eye_r*0.5], fill=(0,0,0))
    elif fname == "skinwalker":
        # Wolf-like ears
        for s in [-1, 1]:
            draw.polygon([(cx+s*10, cy-bh/2), (cx+s*25, cy-bh/2-20), (cx+s*20, cy-bh/2)], fill=body, outline=dark, width=2)
        # Glowing yellow eyes
        for s in [-1, 1]:
            ex = cx+s*eye_sp
            draw.ellipse([ex-eye_r, eye_y-eye_r, ex+eye_r, eye_y+eye_r], fill=(200,200,30))
    elif fname == "thunder":
        # Feathers / wings spread
        for s in [-1, 1]:
            draw.polygon([(cx+s*5, cy-bh*0.3), (cx+s*bw*0.8, cy-bh*0.6), (cx+s*bw*1.0, cy), (cx+s*5, cy+bh*0.2)], fill=(180,160,60))
        # Beak
        draw.polygon([(cx-5, eye_y+5), (cx+5, eye_y+5), (cx+8, eye_y+15), (cx-2, eye_y+10)], fill=(200,150,30))
    
    img.save(f"images/usa_{CHARS.index((name, body, dark, fname))}.png")
    print(f"  {name} ✓")

print("Done! 11 American cryptid sprites generated.")
