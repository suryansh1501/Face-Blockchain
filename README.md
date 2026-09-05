# HH Goa 2026 - Task 3
## Face Identification -> Web Search -> Blockchain Verification

This project is built for HackerHouse Goa 2026 Task 3.

The main idea is to take an image containing a face, generate a face representation using ArcFace, perform a genuine reverse-image search to find matching web/social media results, and store the selected match in a tamper-evident blockchain-style record.

The project is implemented as a command-line pipeline. No website or hosting is required.

---

## About the Project

The pipeline combines face recognition, reverse-image search and blockchain verification into one workflow.

Given an input image, the system:

1. Detects the face in the image.
2. Generates a face embedding using ArcFace.
3. Uploads the image to SerpApi.
4. Performs a Google Lens reverse-image search.
5. Collects real web/social media results.
6. Selects a candidate result from the search.
7. Generates a SHA-256 fingerprint for the result.
8. Stores the record in a local blockchain-style chain.
9. Recalculates and verifies the blockchain hashes.

The web result is treated as a candidate match. It is not considered proof of a person's identity.

---

## How It Works

```text
Input Image
     |
     v
Face Detection
     |
     v
ArcFace Face Embedding
     |
     v
SerpApi Image Upload
     |
     v
Google Lens Reverse Image Search
     |
     v
Web / Social Media Matches
     |
     v
Candidate Match
     |
     v
SHA-256 Fingerprint
     |
     v
Local Blockchain Record
     |
     v
Hash & Chain Verification
Technologies Used
Python 3.11
DeepFace
ArcFace
OpenCV
TensorFlow
SerpApi
Google Lens
SHA-256
JSON-based local blockchain simulation
WSL Ubuntu / Windows
Project Structure
HH_Goa_Task3_MVP/
|
|-- src/
|   |-- __init__.py
|   |-- face.py
|   |-- search.py
|   |-- blockchain.py
|   |-- pipeline.py
|
|-- data/
|   |-- input.jpg
|   |-- blockchain.json
|   |-- run_result.json
|
|-- .env.example
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- run_demo.bat
|-- run_demo.sh
Requirements

Before running the project, make sure you have:

Python 3.10 or newer
Internet connection
SerpApi API key
NVIDIA GPU is optional

The project can also run without a dedicated NVIDIA GPU, although face processing may be slower.

Installation

Clone the repository:

git clone https://github.com/suryansh1501/Face-Blockchain.git
cd Face-Blockchain

Create a virtual environment:

python -m venv .venv

Activate it on Linux / WSL:

source .venv/bin/activate

On Windows:

.venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt
API Configuration

Create a .env file in the project root.

Add:

SERPAPI_API_KEY=your_api_key_here

Do not commit the .env file to GitHub.

The API key is required because the project uses SerpApi for the reverse-image search.

Running the Project

Place the image you want to test inside the data folder.

For example:

data/input.jpg

Run the complete pipeline using:

python -m src.pipeline --image data/input.jpg

You can also specify the maximum number of search results:

python -m src.pipeline --image data/input.jpg --max-results 10
Example Output

A successful run looks similar to:

Faces detected: 1
Model: ArcFace

Uploading image for reverse search...
Google Lens search completed.

Web matches found: 10

Candidate match:
https://example.com/...

Block: 0
SHA-256: <hash>
Block hash: <block_hash>

Chain valid: True

Pipeline completed.

The exact search results will depend on the input image and the current reverse-image search results.

Face Detection and Encoding

The face processing is implemented in:

src/face.py

DeepFace is used for:

Face detection
Face representation
Face embedding generation

The project uses:

ArcFace

as the face recognition model.

The generated embedding represents the detected face numerically and can be used for face comparison.

Reverse Image Search

The reverse-image search implementation is in:

src/search.py

The pipeline uses:

SerpApi Image API

followed by:

Google Lens

This is a genuine online reverse-image search.

The search results are obtained dynamically from the image submitted to the API.

There are no hardcoded social media URLs or predefined identities in the pipeline.

Possible results may include websites and social platforms such as:

Instagram
Facebook
Reddit
Threads
Pinterest
News websites
Other indexed web pages

The results are treated as candidate matches only.

Blockchain Verification

The blockchain implementation is located in:

src/blockchain.py

For every selected search result, the pipeline creates a record containing information such as:

Source URL
Search result metadata
SHA-256 fingerprint
Previous block hash
Current block hash

Each block is connected to the previous block using its hash.

Simplified structure:

Block 0
   |
   | previous_hash
   v
Block 1
   |
   | previous_hash
   v
Block 2

If data inside an earlier block is changed, its hash changes and the chain verification will fail.

SHA-256 Fingerprint

The project uses SHA-256 to generate a fingerprint of the stored match data.

Example:

SHA-256:
f8d8144a38a68f68b8a1f814d15ea44c7027fc5ab5b537170a2e982493d83023

The hash acts as a tamper-evident fingerprint for the stored record.

Blockchain Integrity Check

After creating the blockchain record, the pipeline reads the stored blockchain again and verifies the chain.

Example:

Chain valid: True

This verifies that:

Block hashes are correct.
Previous block references are correct.
The stored data has not been modified.
The chain structure is internally consistent.
Output Files

After running the pipeline, two important files are generated.

data/run_result.json

Contains the result of the latest pipeline execution, including:

Face detection result
Model information
Search results
Selected candidate
SHA-256 fingerprint
Blockchain information
Verification result
data/blockchain.json

Contains the blockchain-style record created by the pipeline.

Important Limitation

The blockchain used in this MVP is a local simulated blockchain implemented using JSON files and SHA-256 hashing.

It is not deployed on Ethereum, Polygon, or another public blockchain network.

The purpose of the implementation is to demonstrate:

Hash-based records
Block linking
Tamper detection
Blockchain-style verification

A production version could replace the local chain with a real blockchain smart contract.

Another Important Limitation

Reverse-image search results do not automatically prove that the person in the input image is the person shown on a returned webpage.

The system therefore treats search results as:

Candidate Match

rather than:

Confirmed Identity

Additional verification would be required for a real-world identity verification system.

Security Notes

Never commit API keys to GitHub.

The following files should remain private:

.env

API keys should be stored using environment variables.

If an API key is accidentally pushed to a public repository, it should be revoked and replaced immediately.

Demo

The complete pipeline can be demonstrated from the terminal:

python -m src.pipeline --image data/input.jpg

The demonstration should show the complete flow:

Input Image
    ->
Face Detection
    ->
ArcFace Encoding
    ->
Reverse Image Search
    ->
Real Web/Social Results
    ->
SHA-256
    ->
Blockchain Record
    ->
Blockchain Verification
Future Scope

Possible improvements include:

Real public blockchain integration
Smart contract based verification
Better face quality checks
Multiple-face handling
Face similarity scoring
Result ranking
More reverse-image search providers
Evidence snapshots and timestamps
Digital signatures
Distributed storage such as IPFS
Stronger identity verification workflows
Repository

GitHub:

https://github.com/suryansh1501/Face-Blockchain

HackerHouse Goa 2026

This project is developed for:

HackerHouse Goa 2026 - Task 3

Task

Face Identification & Blockchain Verification

The project focuses on combining face processing, genuine reverse-image search and tamper-evident blockchain verification in a single pipeline.

Team

Built as an MVP for HackerHouse Goa 2026.