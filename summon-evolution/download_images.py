"""Download Sprunki character images from web with proper browser headers."""
import requests
import os
import time

os.makedirs("images", exist_ok=True)

# Image URLs collected from sprunki.com character pages (valid tokens)
CHAR_URLS = {
    "raddy": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/53d1095f8ef68d855ffd0b64a9a8e8a4~tplv-h9hire4aei-image.jpeg",
    "garnold": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/679592769367b0404d239d34fb6fd26e~tplv-h9hire4aei-image.jpeg",
    "black": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/8706856814344ba2c6d7eeaf39becd3a~tplv-h9hire4aei-image.jpeg",
    "gray": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/9af6ab1fd6c3b2ad3823e1c3cf991206~tplv-h9hire4aei-image.jpeg",
    "funbot": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/ef9ef4a1107bdf1ab2d2751f841d956d~tplv-h9hire4aei-image.jpeg",
    "sky": "https://p19-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/dded62ea83b587876abf928d0ffd5de0~tplv-h9hire4aei-image.jpeg",
    "oren": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/ee262606e97f72f2fe6a8a3b16aea765~tplv-h9hire4aei-image.jpeg",
    "mrsun": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/4fc767b8055f8f980873a5f488bcb6ea~tplv-h9hire4aei-image.jpeg",
    "mrtree": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/8706856814344ba2c6d7eeaf39becd3a~tplv-h9hire4aei-image.jpeg",
    "jevin": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/bac3d5baa76abe608ae6dae15dcbf011~tplv-h9hire4aei-image.jpeg",
    "pinki": "https://p16-cc-image-search-sign-sg.ibyteimg.com/tos-alisg-i-h9hire4aei-sg/image/8706856814344ba2c6d7eeaf39becd3a~tplv-h9hire4aei-image.jpeg",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://sprunki.com/",
    "Origin": "https://sprunki.com",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
}

session = requests.Session()
session.proxies = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

for name, url in CHAR_URLS.items():
    try:
        resp = session.get(url, headers=headers, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(f"images/{name}.png", "wb") as f:
                f.write(resp.content)
            print(f"  OK: {name}.png ({len(resp.content)} bytes)")
        else:
            print(f"  FAIL: {name} (status={resp.status_code}, size={len(resp.content)})")
    except Exception as e:
        print(f"  ERR: {name} - {e}")
    time.sleep(0.3)

print("Done!")
