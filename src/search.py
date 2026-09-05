import os
from pathlib import Path
import requests

BASE = "https://serpapi.com"

def upload_image(image_path: str, api_key: str) -> str:
    with open(image_path, "rb") as f:
        response = requests.post(
            f"{BASE}/image",
            files={"image": f},
            data={"api_key": api_key},
            timeout=60,
        )
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data["image_id"]

def google_lens(image_id: str, api_key: str, max_results: int = 10) -> dict:
    params = {
        "engine": "google_lens",
        "image_id": image_id,
        "type": "all",
        "hl": "en",
        "api_key": api_key,
    }
    response = requests.get(
        f"{BASE}/search",
        params=params,
        timeout=90,
    )
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data

def extract_candidates(data: dict, max_results: int = 10) -> list[dict]:
    candidates = []

    for key in ("visual_matches", "exact_matches"):
        for item in data.get(key, [])[:max_results]:
            candidates.append({
                "match_type": key,
                "title": item.get("title"),
                "link": item.get("link"),
                "source": item.get("source"),
                "snippet": item.get("snippet"),
                "thumbnail": item.get("thumbnail"),
            })

    # Deduplicate by URL.
    seen = set()
    unique = []
    for c in candidates:
        url = c.get("link")
        if url and url not in seen:
            seen.add(url)
            unique.append(c)
    return unique[:max_results]
