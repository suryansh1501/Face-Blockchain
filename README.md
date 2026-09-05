# Face Identification & Blockchain Verification

HackerHouse Goa 2026 - Task 3

## About the Project

This project takes a face image as input, detects and represents the face, searches the web for related content using reverse image search, and creates a tamper-evident record of the selected result using blockchain hashing.

The main idea is to connect face processing, real web search, and blockchain verification in one pipeline.

The project does not use hardcoded social media links. Search results are obtained dynamically during execution.

## How It Works

The complete pipeline works in the following order:

```text
Input Image
    |
    v
Face Detection
    |
    v
Face Representation using ArcFace
    |
    v
Reverse Image Search
    |
    v
Google Lens / Web Results
    |
    v
Candidate Online Content
    |
    v
SHA-256 Fingerprint
    |
    v
Blockchain Record
    |
    v
Blockchain Integrity Check