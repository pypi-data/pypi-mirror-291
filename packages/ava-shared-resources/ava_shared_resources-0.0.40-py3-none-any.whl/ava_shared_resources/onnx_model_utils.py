"""Utility functions for ONNX models."""

import logging
from typing import List

import numpy as np
from numpy.linalg import norm

log = logging.getLogger(__name__)


def create_batches(content: List[str], batch_size: int):
    """Create batches of content for ONNX model inference.

    :param content: list strings for batching
    :param batch_size: approximate batch size for ONNX model batch inference.
    :return: batches of content
    """
    no_of_batches = (
        len(content) // batch_size
        if len(content) % batch_size == 0
        else len(content) // batch_size + 1
    )
    # Split an array into multiple sub-arrays of equal or near-equal size.
    return np.array_split(np.array(content), no_of_batches)


def normalize_embeddings(
    s2v_embeddings: np.ndarray, to_normalize_vector: bool
) -> List[np.ndarray]:
    """Normalize the sentence embeddings based on the to_normalize_vector flag.

    :param s2v_embeddings: sentence embeddings to be normalized
    :param to_normalize_vector: whether to normalize the sentence embeddings
    :return: s2v_embeddings: normalized sentence embeddings
    """
    if to_normalize_vector:
        log.debug(f"Normalizing embeddings: {s2v_embeddings.shape}...")
        s2v_embeddings = [
            normalize_vector(s2v_embedding) for s2v_embedding in s2v_embeddings
        ]

    return s2v_embeddings


def normalize_vector(s2v_embedding_vector: np.ndarray) -> np.ndarray:
    """Normalize a single sentence vector.

    :param s2v_embedding_vector: sentence vector to be normalized
    :return: s2v_embedding_vector: normalized sentence vector
    """
    s2v_embedding_vector = s2v_embedding_vector.squeeze()
    s2v_embedding_vector_norm = norm(s2v_embedding_vector)

    if s2v_embedding_vector_norm != 0:
        return s2v_embedding_vector / s2v_embedding_vector_norm

    return s2v_embedding_vector
