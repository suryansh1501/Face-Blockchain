import hashlib
import json
import time
from pathlib import Path

CHAIN_FILE = Path("data/blockchain.json")

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def canonical_json(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def load_chain() -> list:
    if not CHAIN_FILE.exists():
        return []
    return json.loads(CHAIN_FILE.read_text(encoding="utf-8"))

def save_chain(chain: list):
    CHAIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHAIN_FILE.write_text(json.dumps(chain, indent=2, ensure_ascii=False), encoding="utf-8")

def add_record(payload: dict) -> dict:
    chain = load_chain()
    previous_hash = chain[-1]["block_hash"] if chain else "0" * 64

    block = {
        "index": len(chain),
        "timestamp": int(time.time()),
        "previous_hash": previous_hash,
        "payload": payload,
    }

    block_hash = sha256_text(canonical_json(block))
    block["block_hash"] = block_hash
    chain.append(block)
    save_chain(chain)
    return block

def verify_chain() -> dict:
    chain = load_chain()
    previous = "0" * 64

    for i, block in enumerate(chain):
        expected = sha256_text(canonical_json({
            "index": block["index"],
            "timestamp": block["timestamp"],
            "previous_hash": block["previous_hash"],
            "payload": block["payload"],
        }))

        if block["index"] != i:
            return {"valid": False, "reason": f"bad index at block {i}"}
        if block["previous_hash"] != previous:
            return {"valid": False, "reason": f"broken previous hash at block {i}"}
        payload = block["payload"]
        content_hash = payload.get("content_hash")
        if content_hash:
            unsigned_payload = {
                key: value for key, value in payload.items() if key != "content_hash"
            }
            if content_hash != sha256_text(canonical_json(unsigned_payload)):
                return {"valid": False, "reason": f"bad content hash at block {i}"}
        if block["block_hash"] != expected:
            return {"valid": False, "reason": f"tampering detected at block {i}"}

        previous = block["block_hash"]

    return {"valid": True, "blocks": len(chain)}

def verify_payload(block: dict, payload: dict) -> bool:
    return block["payload"].get("content_hash") == sha256_text(canonical_json(payload))
