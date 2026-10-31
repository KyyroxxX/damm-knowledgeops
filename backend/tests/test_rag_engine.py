import pytest
from app.rag_engine import cosine_similarity

def test_cosine_similarity_identical():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert pytest.approx(cosine_similarity(v1, v2), 0.0001) == 1.0

def test_cosine_similarity_orthogonal():
    v1 = [1.0, 0.0, 0.0]
    v2 = [0.0, 1.0, 0.0]
    assert pytest.approx(cosine_similarity(v1, v2), 0.0001) == 0.0

def test_cosine_similarity_zero_vector():
    v1 = [0.0, 0.0, 0.0]
    v2 = [1.0, 2.0, 3.0]
    assert cosine_similarity(v1, v2) == 0.0
