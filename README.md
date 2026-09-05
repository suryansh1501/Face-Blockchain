# HH Goa 2026 — Task 3 MVP
## Face Identification → Web/Social Search → Blockchain Verification

This MVP implements the required pipeline:

1. Detect/encode a face from an input image using DeepFace.
2. Upload the input image to SerpApi Image API and perform a genuine Google Lens search.
3. Collect visual/exact web matches and optionally verify candidate images against the input face.
4. Hash the discovered post metadata/content and write it to a local tamper-evident simulated blockchain.
5. Re-read the blockchain record and verify the hash.

> Important: this project does **not** claim that a visual web match is proof of a person's identity. Face similarity is treated as a candidate signal and should be manually reviewed.

## Requirements

- Python 3.10+
- A SerpApi API key for Google Lens.
- Internet access for the search step.

## Install

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Create `.env`:

```env
SERPAPI_KEY=your_key_here
```

## Run

```bash
python -m src.pipeline --image path/to/face.jpg
```

Optional:

```bash
python -m src.pipeline --image path/to/face.jpg --max-results 10
```

The program creates:
- `data/blockchain.json` — local simulated blockchain
- `data/run_result.json` — pipeline output

## Demo flow

**Input face**
→ DeepFace face detection/embedding
→ SerpApi Image API upload
→ Google Lens visual/exact matches
→ candidate result selection
→ SHA-256 content fingerprint
→ local blockchain block
→ re-hash + on-chain verification

## Why SerpApi?

SerpApi documents an Image API that accepts JPG/JPEG/PNG/WebP uploads and returns an `image_id`; that ID can then be supplied to its Google Lens API. The Lens API returns visual matches and related web data.

## Limitations

- Google Lens results depend on the image, search engine, region and API availability.
- Social platforms may block automated access or expose limited metadata.
- A reverse-image result is not automatically a verified identity.
- The local chain is a simulated blockchain for the MVP. For a stronger final demo, replace `src/blockchain.py` with an Ethereum/Polygon testnet adapter while keeping the same hash payload.
