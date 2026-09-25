#!/usr/bin/env python3
"""Send a message to a Telegram chat using only the standard library."""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

def _parse_env(path: Path) -> None:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip().removeprefix("export ").strip()
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))

def load_env() -> Optional[Path]:
    # 1. Явный путь: его передаёт Claude (см. SKILL.md)
    explicit = os.getenv("SKILL_ENV_FILE")
    if explicit and Path(explicit).is_file():
        _parse_env(Path(explicit)); return Path(explicit)

    # 2. Поиск от текущей папки вверх (на 3 уровня)
    here = Path.cwd().resolve()
    for d in [here, *list(here.parents)[:3]]:
        for p in (d / ".env", d / "my-skill-secrets" / ".env"):
            if p.is_file():
                _parse_env(p); return p
    return None


def get_config():
    load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        sys.exit(
            "Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set "
            "in the environment or in a .env file (pass its path via SKILL_ENV_FILE)."
        )

    return token, chat_id


def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode("utf-8"))
        sys.exit(f"Telegram API error: {body.get('description', body)}")
    except urllib.error.URLError as e:
        sys.exit(f"Network error: {e.reason}")

    if not body.get("ok"):
        sys.exit(f"Telegram API error: {body}")

    return body


def main():
    text = " ".join(sys.argv[1:]).strip()
    if not text:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()

    if not text:
        sys.exit("Usage: send.py <message text> (or pipe text via stdin)")

    token, chat_id = get_config()
    send_message(token, chat_id, text)
    print("Message sent.")


if __name__ == "__main__":
    main()
