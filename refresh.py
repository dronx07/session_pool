import json
import random
import time
from pathlib import Path
import random
from seleniumbase import SB

OUTPUT_FILE = Path("session_pool.json")
TARGET_URL = "https://www.google.com/search?q={}"
POOL_SIZE = 100
SLEEP = 3
MAX_SESSIONS = 50000

prefixes = [
    "how to", "best", "top", "what is", "why does", "where to buy",
    "cheap", "free", "guide to", "tips for", "examples of",
    "benefits of", "problems with", "difference between"
]

topics = [
    "python programming", "machine learning", "bitcoin", "iphone",
    "digital marketing", "seo", "youtube growth", "weight loss",
    "healthy diet", "home workout", "laptop for students",
    "gaming pc", "electric cars", "tesla stock", "remote jobs",
    "ai tools", "chatgpt", "data science", "web development",
    "cybersecurity", "cloud computing", "online business",
    "dropshipping", "affiliate marketing", "freelancing"
]

suffixes = [
    "for beginners", "in 2025", "step by step", "tutorial",
    "explained", "near me", "with examples", "for students",
    "for business", "for passive income"
]

keywords = []

while len(keywords) < 100:
    keyword = f"{random.choice(prefixes)} {random.choice(topics)} {random.choice(suffixes)}"
    keywords.append(keyword)

for i, k in enumerate(keywords, 1):
    print(f"{i}. {k}")

def grab_session(session_id: str, keyword: str):
    try:
        sb_kwargs = {
            "headless": True,
            "uc": True,
        }

        with SB(**sb_kwargs) as sb:
            sb.open(TARGET_URL.format(keyword))
            sb.sleep(SLEEP)
            sb.driver.refresh()
            sb.sleep(SLEEP)

            cookies = sb.get_cookies()

    except Exception as e:
        raise RuntimeError(
            f"Failed to create session {session_id} with keyword {keyword}"
        ) from e

    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)

    return {
        "id": session_id,
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Cookie": cookie_str,
            "Downlink": "10",
            "Priority": "u=0, i",
            "Rtt": "50",
            "Sec-Ch-Prefers-Color-Scheme": random.choice(["light", "dark"]),
            "Sec-Ch-Ua": '"Not:A-Brand";v="99", "Google Chrome";v="142", "Chromium";v="142"',
            "Sec-Ch-Ua-Arch": "x86",
            "Sec-Ch-Ua-Bitness": "64",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-ua-Model": "",
            "Sec-Ch-ua-Platform": "Windows",
            "Sec-Ch-ua-Platform-version": "19.0.0",
            "Sec-Ch-ua-Wow64": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "X-Browser-Channel": "stable",
            "X-Browser-Copyright": "Copyright 2026 Google LLC. All Rights reserved.",
            "X-Browser-Year": "2026"
        }
    }

def main():
    if OUTPUT_FILE.exists():
        try:
            existing_data = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
            sessions = existing_data.get("sessions", [])
        except Exception:
            sessions = []
    else:
        sessions = []

    for _ in range(POOL_SIZE):
        keyword = random.choice(keywords)
        session_id = f"s{len(sessions) + 1}"
        print(f"[INFO] Generating session {session_id} using keyword {keyword}")
        session = grab_session(session_id, keyword)
        sessions.append(session)

        if len(sessions) > MAX_SESSIONS:
            sessions = sessions[-MAX_SESSIONS:]

    payload = {
        "updated_at": int(time.time()),
        "sessions": sessions,
    }

    OUTPUT_FILE.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
