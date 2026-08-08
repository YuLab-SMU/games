"""Regenerate brighter scene background images."""
from PIL import Image, ImageDraw
import random, math, os

os.makedirs("images", exist_ok=True)
W, H = 1600, 1200

def make_space():
    img = Image.new("RGB", (W, H), (15, 12, 50))
    draw = ImageDraw.Draw(img)
    rng = random.Random(42)
    
    for y in range(H):
        t = y / H
        r = int(15 + t * 15)
        g = int(12 + t * 18)
        b = int(50 + t * 15)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    for _ in range(6):
        cx, cy = rng.randint(100, W-100), rng.randint(100, H-100)
        color = rng.choice([(80,70,150), (100,50,100), (50,80,140), (80,40,90)])
        for _ in range(25):
            x, y = cx + rng.randint(-200, 200), cy + rng.randint(-150, 150)
            r = rng.randint(60, 180)
            overlay = Image.new("RGBA", (W, H), (0,0,0,0))
            od = ImageDraw.Draw(overlay)
            od.ellipse([x-r, y-r, x+r, y+r], fill=(*color, rng.randint(8, 25)))
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
            draw = ImageDraw.Draw(img)
    
    for _ in range(600):
        x, y = rng.randint(0, W), rng.randint(0, H)
        r = rng.randint(1, 3)
        brite = rng.randint(150, 255)
        c = (brite, brite, brite)
        if rng.random() < 0.12: c = rng.choice([(200,220,255), (255,240,200), (255,200,220)])
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
        if r >= 2:
            draw.line([(x-r*2, y), (x+r*2, y)], fill=c, width=1)
            draw.line([(x, y-r*2), (x, y+r*2)], fill=c, width=1)
    
    px, py, pr = 280, 900, 80
    for a in range(360):
        shade = int(180 + 60 * abs(math.cos(math.radians(a))))
        draw.arc([px-pr, py-pr, px+pr, py+pr], a, a+1, fill=(shade, int(shade*0.85), int(shade*0.65)), width=2)
    for _ in range(40):
        a, d = rng.random()*math.pi*2, rng.randint(pr+10, pr+40)
        draw.point((px + math.cos(a)*d, py + math.sin(a)*d*0.25), fill=(220,220,240))
    
    mx, my = 1300, 300
    draw.ellipse([mx-35, my-35, mx+35, my+35], fill=(220, 220, 230))
    draw.ellipse([mx-10, my-15, mx+5, my+5], fill=(190, 190, 200))
    draw.ellipse([mx+8, my-5, mx+18, my+8], fill=(190, 190, 200))
    
    img.save("images/bg-space.png")
    print("  Space ✓")

def make_ocean():
    img = Image.new("RGB", (W, H), (15, 40, 75))
    draw = ImageDraw.Draw(img)
    rng = random.Random(99)
    
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(int(15+t*10), int(40+t*35), int(75-t*25)))
    
    for i in range(6):
        rx, alpha = 100 + i * 280, 25 + rng.randint(8, 20)
        for _ in range(12):
            x, y = rx + rng.randint(-40, 40), rng.randint(0, H)
            overlay = Image.new("RGBA", (W, H), (0,0,0,0))
            od = ImageDraw.Draw(overlay)
            od.polygon([(x-20, 0), (x+20, 0), (x+80, y+100), (x-80, y+100)], fill=(120, 200, 255, alpha))
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
            draw = ImageDraw.Draw(img)
    
    for _ in range(150):
        x, y, r = rng.randint(0, W), rng.randint(H//3, H), rng.randint(3, 8)
        draw.ellipse([x-r, y-r*0.3, x+r, y+r*0.3], fill=(60, 120, 170))
    
    for _ in range(80):
        x, y, r = rng.randint(0, W), rng.randint(50, H), rng.randint(3, 12)
        draw.ellipse([x-r, y-r, x+r, y+r], outline=(180, 230, 255), width=1)
        draw.ellipse([x-r*0.4, y-r*0.5, x+r*0.2, y-r*0.1], fill=(230, 245, 255))
    
    for x in range(0, W, 4):
        h = H - 60 + int(math.sin(x*0.02)*20 + math.sin(x*0.05)*10)
        draw.line([(x, h), (x, H)], fill=(30, 75, 50))
    
    for _ in range(15):
        kx, kh = rng.randint(50, W-50), 100 + rng.randint(50, 200)
        for i in range(5):
            x_off = int(math.sin(i*0.8)*15)
            draw.line([(kx+x_off, H-60-i*kh//5), (kx+x_off, H-60-(i+1)*kh//5)], fill=(40, 110, 60), width=4)
    
    img.save("images/bg-ocean.png")
    print("  Ocean ✓")

def make_forest():
    img = Image.new("RGB", (W, H), (25, 55, 30))
    draw = ImageDraw.Draw(img)
    rng = random.Random(77)
    
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(int(25+t*30), int(55+t*40), int(30+t*20)))
    
    for _ in range(30):
        fx, fy, fr = rng.randint(0, W), rng.randint(H-200, H), rng.randint(80, 200)
        overlay = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([fx-fr, fy-fr*0.5, fx+fr, fy+fr*0.5], fill=(200, 220, 190, 10))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
    
    for _ in range(12):
        tx, th, tw = rng.randint(50, W-50), 200+rng.randint(100,400), 30+rng.randint(10,40)
        draw.rectangle([tx-tw//2, H-th//2, tx+tw//2, H], fill=(50, 35, 20))
        for i in range(3):
            fy, fr = H - th//2 - i*60 - 30, tw + rng.randint(20,50) - i*5
            shade = rng.randint(35, 70)
            draw.ellipse([tx-fr, fy-fr*0.7, tx+fr, fy+fr*0.7], fill=(shade, shade+40, shade+15))
    
    for _ in range(100):
        dx, dy, dr = rng.randint(0, W), rng.randint(50, H-300), rng.randint(5, 25)
        draw.ellipse([dx-dr, dy-dr*0.7, dx+dr, dy+dr*0.7], fill=(90, 140, 70))
    
    for _ in range(100):
        fx, fy, fr = rng.randint(0, W), rng.randint(30, H-50), rng.randint(2, 5)
        draw.ellipse([fx-fr, fy-fr, fx+fr, fy+fr], fill=(255, 240, 90))
    
    draw.rectangle([0, H-30, W, H], fill=(30, 50, 25))
    img.save("images/bg-forest.png")
    print("  Forest ✓")

def make_cyber():
    img = Image.new("RGB", (W, H), (15, 12, 35))
    draw = ImageDraw.Draw(img)
    rng = random.Random(33)
    
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(int(15+t*10), int(12+t*8), int(35+t*20)))
    
    for x in range(0, W, 40):
        fy, ty = H - 250, H
        sx = (x - W//2) * (fy / ty) + W//2
        draw.line([(sx, fy), (x, ty)], fill=(0, 200, 240, 20), width=1)
    for y in range(H-250, H, 30):
        draw.line([(0, y), (W, y)], fill=(0, 200, 240, 15), width=1)
    
    for _ in range(5):
        cx, cy, cr = rng.randint(100, W-100), rng.randint(80, H-300), rng.randint(60, 150)
        color = rng.choice([(255,100,100), (0,230,255), (180,90,200), (0,250,130)])
        draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], outline=color, width=2)
        draw.ellipse([cx-cr-3, cy-cr-3, cx+cr+3, cy+cr+3], outline=color, width=1)
    
    for x in range(20, W, 40):
        for y in range(20, H-300, 40):
            draw.point((x, y), fill=(50, 50, 90))
    
    for _ in range(25):
        dx, dy, dh = rng.randint(0, W), rng.randint(0, H), rng.randint(30, 150)
        draw.line([(dx, dy), (dx, min(dy+dh, H))], fill=(0, 230, 255, rng.randint(60, 150)), width=1)
    
    for _ in range(8):
        gx, gy, gw, gh = rng.randint(0, W-100), rng.randint(0, H-20), rng.randint(40, 120), rng.randint(2, 6)
        draw.rectangle([gx, gy, gx+gw, gy+gh], fill=(0, 230, 255, 50))
    
    for y in range(H-5, H):
        draw.line([(0, y), (W, y)], fill=(0, 230, 255, int((y-(H-5))/5*80)), width=1)
    
    img.save("images/bg-cyber.png")
    print("  Cyber ✓")

def make_candy():
    img = Image.new("RGB", (W, H), (50, 25, 60))
    draw = ImageDraw.Draw(img)
    rng = random.Random(55)
    
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(int(50+t*30), int(25+t*15), int(60+t*25)))
    
    for _ in range(12):
        cx, cy, cr = rng.randint(0, W), rng.randint(0, H), rng.randint(80, 200)
        c = rng.choice([(255,220,240,12), (220,235,255,10), (255,245,220,10), (235,200,250,12)])
        overlay = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx-cr, cy-cr*0.7, cx+cr, cy+cr*0.7], fill=c)
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
    
    for _ in range(250):
        sx, sy, sr = rng.randint(0, W), rng.randint(0, H), rng.randint(1, 3)
        sc = rng.choice([(255,255,255), (255,225,130), (255,180,225), (160,235,255)])
        draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=sc)
    
    for i in range(8):
        y1, y2 = i*H//8, (i+1)*H//8
        colors = [(255,180,225,10), (255,220,160,8), (180,220,255,8), (235,180,255,8), (255,200,200,8), (220,255,240,8)]
        draw.rectangle([0, y1, W, y2], fill=colors[i%len(colors)])
    
    for _ in range(8):
        lx, ly, lr = rng.randint(50, W-50), rng.randint(100, H-100), rng.randint(30, 60)
        lc = rng.choice([(255,180,220), (255,225,100), (255,140,140), (110,220,255)])
        draw.line([(lx, ly+lr), (lx, min(ly+lr*3, H-20))], fill=(220,220,220), width=4)
        draw.ellipse([lx-lr, ly-lr, lx+lr, ly+lr], fill=lc)
        draw.ellipse([lx-lr+4, ly-lr+4, lx+lr-4, ly+lr-4], fill=(255,255,255))
        for a in range(0, 360, 30):
            rad = math.radians(a)
            draw.point((lx+math.cos(rad)*lr*0.4, ly+math.sin(rad)*lr*0.4), fill=lc)
    
    img.save("images/bg-candy.png")
    print("  Candy ✓")

print("Generating brighter backgrounds...")
make_space()
make_ocean()
make_forest()
make_cyber()
make_candy()
print("Done!")
