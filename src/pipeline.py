import argparse
import json
import os
from pathlib import Path
from dotenv import load_dotenv

from .face import detect_and_encode
from .search import upload_image, google_lens, extract_candidates
from .blockchain import add_record, verify_chain, sha256_text, canonical_json

def main():
    parser = argparse.ArgumentParser(description="HH Goa 2026 Task 3 MVP")
    parser.add_argument("--image", required=True, help="Input face image")
    parser.add_argument("--max-results", type=int, default=10)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise SystemExit("Missing SERPAPI_KEY. Put it in .env")

    image_path = Path(args.image)
    if not image_path.exists():
        raise SystemExit(f"Input image not found: {image_path}")

    print("\n[1/4] Detecting and encoding face...")
    face_info = detect_and_encode(str(image_path))
    print(f"      Faces detected: {face_info['faces_detected']}")
    print(f"      Model: {face_info['model']}")

    print("\n[2/4] Performing genuine reverse-image web search...")
    image_id = upload_image(str(image_path), api_key)
    lens = google_lens(image_id, api_key, args.max_results)
    candidates = extract_candidates(lens, args.max_results)
    print(f"      Web matches found: {len(candidates)}")

    if not candidates:
        raise SystemExit("No web matches returned. Try another image.")

    for i, c in enumerate(candidates, 1):
        print(f"      {i}. {c.get('title')} — {c.get('link')}")

    # For the MVP, the first returned match is recorded as the discovered result.
    # The UI/demo should make clear that it is a candidate web match, not identity proof.
    selected = candidates[0]

    print("\n[3/4] Creating tamper-evident blockchain record...")
    payload = {
        "input_image": image_path.name,
        "search_engine": "Google Lens via SerpApi",
        "match_type": selected.get("match_type"),
        "title": selected.get("title"),
        "source": selected.get("source"),
        "link": selected.get("link"),
        "snippet": selected.get("snippet"),
        "thumbnail": selected.get("thumbnail"),
        "face_model": face_info["model"],
    }
    payload_hash = sha256_text(canonical_json(payload))
    payload["content_hash"] = payload_hash

    block = add_record(payload)
    print(f"      Block: {block['index']}")
    print(f"      SHA-256: {payload_hash}")
    print(f"      Block hash: {block['block_hash']}")

    print("\n[4/4] Re-verifying blockchain...")
    verification = verify_chain()
    print(f"      Chain valid: {verification['valid']}")

    result = {
        "face": face_info,
        "image_id": image_id,
        "candidates": candidates,
        "selected_match": selected,
        "block": block,
        "blockchain_verification": verification,
    }

    Path("data").mkdir(exist_ok=True)
    Path("data/run_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n✅ Pipeline completed.")
    print("   Output: data/run_result.json")
    print("   Blockchain: data/blockchain.json")

if __name__ == "__main__":
    main()
