#!/usr/bin/env python3
"""Generate rhythm box REFRESHED images for all 20 Sprunki characters via gpt-image."""
import subprocess
import os
import time

GPT_IMAGE = r"E:/YuNotebooks/01_Development/source/mygithub/ygc-scripts/bin/gpt-image.py"
OUT_DIR = r"E:/YuNotebooks/01_Development/source/games/summon-rhythm-box/images"

# All 20 Sprunki characters
CHARACTERS = [
    ("raddy", "Raddy, a red round blob character with big eyes, simple cartoon creature, red body"),
    ("garnold", "Garnold, a yellow square robotic character with antenna, cartoon robot design, blocky shape"),
    ("black", "Black, a dark shadow blob character with glowing white eyes, simple spooky cartoon design"),
    ("gray", "Gray, a gray round stone-like character with cracks, cartoon rock creature"),
    ("funbot", "Fun Bot, a cute robot character with a screen face showing a smile, cartoon robot design"),
    ("sky", "Sky, a light blue cloud-like character, fluffy cartoon cloud creature with eyes"),
    ("oren", "Oren, an orange ball character with cat ears, cartoon orange creature"),
    ("mrsun", "Mr Sun, a yellow sun character with sunglasses and a cool smile, cartoon sun design"),
    ("mrtree", "Mr Tree, a brown tree trunk character with green leaves on top, cartoon tree creature"),
    ("jevin", "Jevin, a purple jelly-like character, wobbly cartoon purple blob with eyes"),
    ("pinki", "Pinki, a pink heart-shaped character, cute cartoon pink creature with bow"),
    ("lime", "Lime, a green lime fruit character with a leaf hat, cartoon citrus creature"),
    ("vineria", "Vineria, a vine plant character with green tendrils, cartoon plant creature"),
    ("clukr", "Clukr, a silver metallic character with a cymbal hat, cartoon robot musician"),
    ("brud", "Brud, a brown character with bucket hat and googly eyes, cartoon creature"),
    ("durple", "Durple, a purple dragon-like character, cartoon purple creature with horns"),
    ("simon", "Simon, a yellow character with crown hat, cartoon royal creature"),
    ("tunner", "Tunner, a brown character with fedora hat, cartoon detective creature"),
    ("funcomputer", "Fun Computer, a character with a computer monitor as head, cartoon tech creature"),
    ("wenda", "Wenda, a white female character with cat ears, cute cartoon cat girl"),
]


def run(cmd, timeout=180):
    env = os.environ.copy()
    env["http_proxy"] = "http://127.0.0.1:7897"
    env["https_proxy"] = "http://127.0.0.1:7897"
    env["all_proxy"] = "http://127.0.0.1:7897"
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env, shell=True)
    return result


def generate():
    os.makedirs(OUT_DIR, exist_ok=True)
    total = len(CHARACTERS)
    
    for i, (role_id, desc) in enumerate(CHARACTERS):
        filepath = os.path.join(OUT_DIR, f"{role_id}.png")
        # Check if file exists and has reasonable size (>1KB)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            print(f"[{i+1}/{total}] SKIP {role_id}.png (exists)")
            continue
        
        # Delete small/broken file if exists
        if os.path.exists(filepath):
            os.remove(filepath)
        
        prompt = f"Cute chibi cartoon character: {desc}, simple flat colors, rounded shapes, adorable kawaii style, full body, clean transparent background, game icon sprite, 2D vector art style"
        
        cmd = (
            f'python "{GPT_IMAGE}" '
            f'--prompt "{prompt}" '
            f'--out "{filepath}" '
            f'--size 1024x1024 '
            f'--quality high '
            f'--timeout 300'
        )
        print(f"[{i+1}/{total}] GEN {role_id}.png ...", end=" ", flush=True)
        try:
            result = run(cmd, timeout=300)
            if result.returncode == 0:
                outpath = result.stdout.strip()
                if os.path.exists(outpath):
                    size_kb = os.path.getsize(outpath) / 1024
                    print(f"OK ({size_kb:.0f}KB)")
                else:
                    print(f"OK (path: {outpath})")
            else:
                err = result.stderr.strip()[:150]
                print(f"FAIL: {err}")
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
        except Exception as e:
            print(f"ERROR: {e}")
        
        time.sleep(2)


if __name__ == "__main__":
    print(f"=== Generating {len(CHARACTERS)} rhythm box REFRESHED images ===")
    generate()
    print("=== DONE ===")
