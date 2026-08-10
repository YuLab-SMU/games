#!/usr/bin/env python3
"""Generate brainrot character images (classic + refreshed) via gpt-image."""
import subprocess
import os
import time

GPT_IMAGE = r"E:/YuNotebooks/01_Development/source/mygithub/ygc-scripts/bin/gpt-image.py"
OUT_DIR = r"E:/YuNotebooks/01_Development/source/games/summon-rhythm-box/images/brainrot"

# 11 brainrot characters with descriptions
CHARACTERS = [
    ("sneakerShark", "sneaker shark character, a shark wearing colorful sneakers on fins, cartoon creature design"),
    ("bomberCroc", "bomber crocodile character, a crocodile wearing aviator goggles and carrying a bomb on its back, cartoon creature design"),
    ("treeMonkey", "tree monkey character, a monkey with a small tree growing from its head, cartoon creature design"),
    ("cactusElephant", "cactus elephant character, an elephant with cactus spikes and flowers on its back, cartoon creature design"),
    ("coffeeNinja", "coffee ninja character, a ninja holding a hot coffee cup with steam rising, cartoon creature design"),
    ("ballerinaCup", "ballerina cup character, a teacup wearing a ballet tutu and dancing on tiptoe, cartoon creature design"),
    ("bananaChimp", "banana chimpanzee character, a happy chimp holding a banana, cartoon creature design"),
    ("bomberGoose", "bomber goose character, a goose wearing pilot goggles carrying a small bomb, cartoon creature design"),
    ("fridgeCamel", "fridge camel character, a camel with a mini refrigerator on its hump, cartoon creature design"),
    ("saturnCow", "saturn cow character, a cow with a saturn ring around its body, cartoon creature design"),
    ("teapotMan", "teapot man character, a walking teapot person with arms and legs, cartoon creature design"),
]


def run(cmd, timeout=120):
    """Run command with proxy env, capture output."""
    env = os.environ.copy()
    env["http_proxy"] = "http://127.0.0.1:7897"
    env["https_proxy"] = "http://127.0.0.1:7897"
    env["all_proxy"] = "http://127.0.0.1:7897"
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env, shell=True)
    return result


def generate_classic():
    """Generate classic style (detailed, high-quality) images."""
    out = os.path.join(OUT_DIR, "classic")
    os.makedirs(out, exist_ok=True)
    
    for role_id, desc in CHARACTERS:
        filepath = os.path.join(out, f"{role_id}.png")
        if os.path.exists(filepath):
            print(f"[SKIP] classic/{role_id}.png already exists")
            continue
        
        prompt = f"A high-quality detailed game character sprite of {desc}, full body, digital painting style, vibrant colors, clean silhouette, transparent background, sprite sheet ready"
        
        cmd = (
            f'python "{GPT_IMAGE}" '
            f'--prompt "{prompt}" '
            f'--out "{filepath}" '
            f'--size 1200x1416 '
            f'--quality high '
            f'--timeout 300'
        )
        print(f"[GEN] classic/{role_id}.png ...")
        try:
            result = run(cmd, timeout=300)
            if result.returncode == 0:
                print(f"  -> OK: {result.stdout.strip()}")
            else:
                print(f"  -> FAIL: {result.stderr.strip()[:200]}")
        except subprocess.TimeoutExpired:
            print(f"  -> TIMEOUT")
        except Exception as e:
            print(f"  -> ERROR: {e}")
        
        time.sleep(2)  # rate limit


def generate_refreshed():
    """Generate refreshed style (cute chibi) images."""
    out = os.path.join(OUT_DIR, "refreshed")
    os.makedirs(out, exist_ok=True)
    
    for role_id, desc in CHARACTERS:
        filepath = os.path.join(out, f"{role_id}.png")
        if os.path.exists(filepath):
            print(f"[SKIP] refreshed/{role_id}.png already exists")
            continue
        
        prompt = f"Cute chibi cartoon character of {desc}, simple flat colors, rounded shapes, adorable style, clean white background, game icon style"
        
        cmd = (
            f'python "{GPT_IMAGE}" '
            f'--prompt "{prompt}" '
            f'--out "{filepath}" '
            f'--size 512x512 '
            f'--quality high '
            f'--timeout 300'
        )
        print(f"[GEN] refreshed/{role_id}.png ...")
        try:
            result = run(cmd, timeout=300)
            if result.returncode == 0:
                print(f"  -> OK: {result.stdout.strip()}")
            else:
                print(f"  -> FAIL: {result.stderr.strip()[:200]}")
        except subprocess.TimeoutExpired:
            print(f"  -> TIMEOUT")
        except Exception as e:
            print(f"  -> ERROR: {e}")
        
        time.sleep(2)


if __name__ == "__main__":
    print("=== Generating CLASSIC brainrot images ===")
    generate_classic()
    print("\n=== Generating REFRESHED brainrot images ===")
    generate_refreshed()
    print("\n=== DONE ===")
