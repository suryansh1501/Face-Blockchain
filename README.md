# Face Identification -> Web Search -> Blockchain Verification

HackerHouse Goa 2026 Task 3 project.

This command-line project takes an image containing a face, describes the face with an ArcFace embedding, sends the image to a live reverse-image search, and records the first returned web result in a local hash-linked JSON chain. The result is a candidate match for investigation. It is not proof of a person's identity.

## Project Overview

The project demonstrates how face analysis, reverse-image search, and tamper-evident record keeping can be connected in one small pipeline. It is an MVP intended for a local demo, not a production identity-verification service.

### Problem

When an image is found online, it can be useful to know whether similar images appear elsewhere and whether the evidence recorded for a review has changed later. A search result alone is difficult to audit if the result, source metadata, or selected record is edited after the search.

### Solution

The pipeline combines:

- Face detection and face representation with DeepFace, OpenCV, and ArcFace.
- A live SerpApi Image API upload followed by a Google Lens search.
- Candidate web and social-media result extraction and URL de-duplication.
- SHA-256 fingerprints and a local JSON blockchain-style hash chain.
- A final integrity check that recalculates every block hash and previous-block link.

## Complete Workflow

```text
Input image
    |
    v
OpenCV face detection through DeepFace
    |
    v
ArcFace representation (embedding metadata)
    |
    v
Upload image to SerpApi Image API
    |
    v
Google Lens search through SerpApi
    |
    v
Extract visual_matches and exact_matches
    |
    v
De-duplicate URLs and select the first candidate
    |
    v
SHA-256 fingerprint of the stored payload
    |
    v
Append a block to data/blockchain.json
    |
    v
Recalculate hashes and verify the chain
```

## Face Detection and ArcFace

`src/face.py` uses `DeepFace.extract_faces` with the OpenCV detector backend to count detected faces. It then calls `DeepFace.represent` with the ArcFace model and the same OpenCV detector. The pipeline reports the number of faces, the model name, the detector name, and the embedding dimension in its output.

ArcFace produces a numerical representation of a detected face. In this project, the embedding is used to demonstrate the face-analysis step; the current pipeline does not save the embedding or compare it with an image downloaded from a search result. `verify_face_pair` exists as a helper for a separate two-image comparison, but it is not called by the command-line pipeline.

DeepFace provides the face-analysis interface and model integration. OpenCV is the detector backend selected in the code. ArcFace is the representation model selected in the code.

## Reverse-Image Search

`src/search.py` uses the SerpApi Image API to upload the input image. The returned image ID is then passed to SerpApi's Google Lens engine with `type=all`.

The search is live and dynamic. The project does not contain hardcoded identities or fixed social-media URLs. `extract_candidates` collects entries from Google Lens `visual_matches` and `exact_matches`, keeps fields such as title, link, source, snippet, and thumbnail, removes duplicate URLs, and limits the final list to the requested result count.

Returned pages may include social platforms, news sites, image pages, or other indexed websites. These are genuine search results from the service for the submitted image, but a visual or exact match does not establish that the person in the input image is the person named or shown on the page.

### Candidate Match and Identity Limits

For this MVP, the first candidate returned by Google Lens is selected and stored. There is no identity confirmation step in the pipeline. Search ranking, image reuse, captions, lookalikes, and incorrect indexing can all produce misleading results. A real identity workflow would need consent, stronger evidence, a comparison image, quality checks, human review, and legal and privacy safeguards.

## SHA-256 and the Local Chain

`src/blockchain.py` stores records in `data/blockchain.json`. Before a record is added, the pipeline creates a payload containing the input filename, search metadata, selected candidate, and face model. It computes a SHA-256 fingerprint over canonical JSON for that payload and stores it as `content_hash`.

Each block also contains an index, a Unix timestamp, the previous block's hash, the payload, and its own `block_hash`. The block hash is calculated from the block fields other than `block_hash`. This links each block to the one before it and makes later edits detectable.

This is a local simulated, tamper-evident blockchain-style implementation using JSON and SHA-256. It is not Ethereum, Polygon, or any other public blockchain. It has no consensus, distributed nodes, smart contract, or independently trusted external ledger.

## Blockchain Integrity Verification

After adding the record, the pipeline loads the chain again and checks:

- Block indexes are sequential.
- Each `previous_hash` matches the preceding block.
- Each block hash matches a fresh hash of its stored contents.

The command prints `Chain valid: True` when the local chain is internally consistent. This detects changes to the stored chain after the fact; it does not prove that the original search result or input image was truthful.

## Installation

Requirements:

- Python 3.11 (the repository includes `.python-version` with `3.11.11`)
- Internet access for SerpApi
- A SerpApi API key
- A dedicated NVIDIA GPU is optional; DeepFace can run on CPU, but face processing may be slower

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Copy `.env.example` to `.env` and put your own key in it:

```bash
SERPAPI_API_KEY=your_serpapi_key_here
```

The code loads this value with `python-dotenv`. Keep `.env` private. `.env.*` files are ignored by Git, while the safe placeholder `.env.example` remains tracked. Never paste an API key into source code, the README, a commit, or a terminal log.

## Running the Project

Put the image to test at `data/input.jpg`, or pass another image path. From the repository root, run the complete pipeline with:

```bash
python -m src.pipeline --image data/input.jpg
```

To change the maximum number of returned candidates:

```bash
python -m src.pipeline --image data/input.jpg --max-results 10
```

The included demo scripts use the default input path:

```bash
bash run_demo.sh
```

On Windows, run `run_demo.bat` from Command Prompt.

## Expected Output

The exact URLs and titles depend on the submitted image and the live search response. A successful run follows this shape:

```text
[1/4] Detecting and encoding face...
      Faces detected: 1
      Model: ArcFace

[2/4] Performing genuine reverse-image web search...
      Web matches found: 10
      1. <result title> - <result URL>

[3/4] Creating tamper-evident blockchain record...
      Block: 0
      SHA-256: <64-character hash>
      Block hash: <64-character hash>

[4/4] Re-verifying blockchain...
      Chain valid: True

Pipeline completed.
   Output: data/run_result.json
   Blockchain: data/blockchain.json
```

## Output Files

After a successful run:

- `data/run_result.json` contains face metadata, the SerpApi image ID, all extracted candidates, the selected candidate, the block, and blockchain verification details.
- `data/blockchain.json` contains the append-only local chain of records created by runs. Re-running the pipeline appends another block.

Both generated JSON files are ignored by Git because they can contain search metadata and image-related URLs.

## Project Structure

```text
.
|-- src/
|   |-- __init__.py
|   |-- face.py          Face detection and ArcFace metadata
|   |-- search.py        SerpApi upload and Google Lens results
|   |-- blockchain.py    JSON chain and SHA-256 verification
|   |-- pipeline.py      Command-line workflow
|-- data/
|   |-- input.jpg       Example input image
|   |-- blockchain.json  Generated local chain
|   |-- run_result.json  Generated latest run result
|-- .env.example         Safe configuration template
|-- .gitignore
|-- requirements.txt
|-- run_demo.bat
|-- run_demo.sh
|-- README.md
```

## Limitations and Security Notes

- A reverse-image result is a candidate match, not identity proof.
- The current pipeline selects the first result returned by the search service.
- The pipeline does not compare the detected face to a candidate image or produce an identity confidence score.
- Results can change over time because they come from a live external API.
- SerpApi usage requires a valid API key and may incur provider limits or costs.
- Do not commit `.env`, `.env.save`, or any other file containing keys, credentials, tokens, or personal images.
- If a key is exposed, revoke it in SerpApi and create a replacement immediately. Removing it from a later commit does not make an exposed key safe.
- The local JSON chain is tamper-evident, not tamper-proof. Anyone who can rewrite the file can also rewrite the history.
- Obtain permission to process face images and respect the terms and privacy policies of the services used.

## Future Scope

Possible next steps include adding an explicit comparison-image workflow, face quality checks, multiple-face handling, candidate ranking, human review, signed evidence and timestamps, encrypted or access-controlled storage, and integration with a real blockchain or distributed evidence store. Those changes would require careful privacy, consent, and security design.

## HackerHouse Goa 2026 Task 3

This repository was built for HackerHouse Goa 2026, Task 3: **Face Identification -> Web Search -> Blockchain Verification**. The implementation focuses on demonstrating the end-to-end connection between the three stages while keeping the blockchain component local and transparent for a hackathon MVP.
