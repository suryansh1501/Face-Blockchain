# Face Identification & Blockchain Verification

## HackerHouse Goa 2026 — Task #3

An end-to-end AI pipeline that takes a face image, detects and encodes the face, performs a genuine reverse-image/web search to discover matching online content, and creates a tamper-evident blockchain record of the discovered result.

---

## 🎯 Objective

The system demonstrates three major capabilities:

1. **Face Detection & Encoding**
2. **Genuine Web / Social Media Search**
3. **Blockchain-based Verification**

The complete pipeline runs from a single input image without relying on hardcoded search results.

---

## 🔄 End-to-End Workflow

```text
Input Face Image
       ↓
Face Detection
       ↓
Face Encoding using ArcFace
       ↓
Reverse Image Search
       ↓
Google Lens / Web Results
       ↓
Candidate Web & Social Media Matches
       ↓
Select Matching Content
       ↓
Generate SHA-256 Fingerprint
       ↓
Store Fingerprint on Blockchain
       ↓
Verify Blockchain Integrity