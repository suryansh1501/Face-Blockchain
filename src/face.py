from pathlib import Path
from deepface import DeepFace

def detect_and_encode(image_path: str) -> dict:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    faces = DeepFace.extract_faces(
        img_path=str(path),
        detector_backend="opencv",
        enforce_detection=True,
        align=True,
    )

    embeddings = DeepFace.represent(
        img_path=str(path),
        model_name="ArcFace",
        detector_backend="opencv",
        enforce_detection=True,
        align=True,
    )

    return {
        "faces_detected": len(faces),
        "embedding_dimensions": len(embeddings[0]["embedding"]),
        "model": "ArcFace",
        "detector": "opencv",
    }

def verify_face_pair(input_image: str, candidate_image: str) -> dict:
    result = DeepFace.verify(
        img1_path=input_image,
        img2_path=candidate_image,
        model_name="ArcFace",
        detector_backend="opencv",
        distance_metric="cosine",
        enforce_detection=True,
    )
    return {
        "verified": bool(result["verified"]),
        "distance": float(result["distance"]),
        "threshold": float(result.get("max_threshold_to_verify", 0)),
        "model": result.get("model", "ArcFace"),
        "metric": result.get("similarity_metric", "cosine"),
    }
