#!/usr/bin/env python3
"""Regenerate rhythm box REFRESHED images - override old ones."""
import subprocess
import os
import time

GPT_IMAGE = r"E:/YuNotebooks/01_Development/source/mygithub/ygc-scripts/bin/gpt-image.py"
OUT_DIR = r"E:/YuNotebooks/01_Development/source/games/summon-rhythm-box/images"

# Original 11 characters that need regeneration (small 6KB old images)
CHARACTERS = [
    ("raddy", "Raddy, a red round cheerful blob creature with big expressive eyes, simple cute cartoon, full body, rounded shape"),
    ("garnold", "Garnold, a yellow square robotic creature with an antenna on head, cute cartoon robot, blocky but adorable"),
    ("black", "Black, a dark shadow blob creature with glowing white eyes, spooky but cute cartoon ghost-like creature"),
    ("gray", "Gray, a gray stone-like round creature with cracks on surface, cute cartoon rock monster"),
    ("funbot", "Fun Bot, a cute robot with a screen face showing a happy smile emoji, adorable cartoon robot character"),
    ("sky", "Sky, a light blue fluffy cloud creature with cute eyes, adorable cartoon cloud character"),
    ("oren", "Oren, a round orange creature with cat ears, cute cartoon citrus cat character"),
    ("mrsun", "Mr Sun, a bright yellow sun character wearing cool sunglasses with a smile, cartoon sun mascot"),
    ("mrtree", "Mr Tree, a brown tree trunk character with green leafy top, cute cartoon tree creature"),
    ("jevin", "Jevin, a purple jelly-like wobbly blob creature, cute cartoon purple slime character"),
    ("pinki", "Pinki, a pink heart-shaped cute creature with a ribbon bow, adorable cartoon love character"),
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
        # Delete old file to force regeneration
        if os.path.exists(filepath):
            old_size = os.path.getsize(filepath)
            if old_size < 8000:
                print(f"[{i+1}/{total}] {role_id}: old={old_size}B -> regenerating...")
                os.remove(filepath)
            else:
                print(f"[{i+1}/{total}] SKIP {role_id}.png ({old_size}B)")
                continue
        
        prompt = f"Cute chibi cartoon character design: {desc}, simple flat colors, rounded shapes, adorable kawaii style, full body centered, clean transparent background, game icon sprite, 2D vector art, high quality"
        
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
                    print("OK")
            else:
                err = result.stderr.strip()[:150]
                print(f"FAIL: {err}")
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
        except Exception as e:
            print(f"ERROR: {e}")
        
        time.sleep(2)


if __name__ == "__main__":
    print(f"=== Regenerating {len(CHARACTERS)} rhythm box REFRESHED images ===")
    generate()
    print("=== DONE ===")
