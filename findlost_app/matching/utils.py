"""Face detection, encoding, and comparison utilities.
See Project Report Section 7.2 and Appendix A.2.

NOTE: requires the `face_recognition` and `dlib` packages (see
requirements.txt). These are not installed in every environment by
default because dlib requires a C++ build toolchain — see
Appendix B.1 (Prerequisites) in the project report.
"""
import io
import numpy as np

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:  # pragma: no cover
    FACE_RECOGNITION_AVAILABLE = False


def encode_face(image_path):
    """Detect a face in the image at `image_path` and return its
    128-dimensional encoding, or None if no face is found."""
    if not FACE_RECOGNITION_AVAILABLE:
        raise RuntimeError(
            'face_recognition is not installed. Run: pip install face-recognition dlib'
        )
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return None
    encodings = face_recognition.face_encodings(image, face_locations)
    return encodings[0] if encodings else None


def encode_face_from_fieldfile(field_file):
    """Convenience wrapper: encode a face directly from a Django
    ImageField/FieldFile (e.g. `person.photo`) without needing a
    separate saved-to-disk path lookup."""
    if not FACE_RECOGNITION_AVAILABLE:
        raise RuntimeError(
            'face_recognition is not installed. Run: pip install face-recognition dlib'
        )
    field_file.seek(0)
    image = face_recognition.load_image_file(io.BytesIO(field_file.read()))
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return None
    encodings = face_recognition.face_encodings(image, face_locations)
    return encodings[0] if encodings else None


def bytes_to_encoding(data):
    """Convert a BinaryField's raw bytes back into a numpy float64 array."""
    return np.frombuffer(data, dtype=np.float64)


def compare_faces(known_encoding, candidate_encoding, threshold=0.6):
    """Return (is_match, distance) for two 128-d encodings, using
    Euclidean distance as described in Report Section 7.2, Step 4."""
    distance = np.linalg.norm(known_encoding - candidate_encoding)
    return distance <= threshold, distance
