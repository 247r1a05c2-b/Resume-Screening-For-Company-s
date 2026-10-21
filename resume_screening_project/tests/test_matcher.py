import pytest

from src import matcher


def test_tfidf_similarity_returns_scores_for_each_resume():
    scores = matcher.tfidf_similarity(
        {"candidate_a": "python sql machine learning", "candidate_b": "graphic design"},
        "python machine learning",
    )
    assert set(scores) == {"candidate_a", "candidate_b"}
    assert scores["candidate_a"] > scores["candidate_b"]
    assert all(0.0 <= score <= 1.0 for score in scores.values())


def test_tfidf_similarity_handles_empty_inputs():
    assert matcher.tfidf_similarity({}, "python") == {}
    assert matcher.tfidf_similarity({"candidate": ""}, "") == {"candidate": 0.0}


def test_combined_similarity_normalizes_weights(monkeypatch):
    monkeypatch.setattr(matcher, "tfidf_similarity", lambda resumes, jd: {"a": 0.2, "b": 0.8})
    monkeypatch.setattr(matcher, "semantic_similarity", lambda resumes, jd: {"a": 0.8, "b": 0.2})

    scores = matcher.combined_similarity({"a": "text", "b": "other"}, "jd", 1, 3)

    assert scores == {"a": 0.65, "b": 0.35}


def test_combined_similarity_rejects_invalid_weights():
    with pytest.raises(ValueError):
        matcher.combined_similarity({"a": "text"}, "jd", 0, 0)
    with pytest.raises(ValueError):
        matcher.combined_similarity({"a": "text"}, "jd", -1, 2)


def test_combined_similarity_uses_tfidf_when_semantic_model_unavailable(monkeypatch):
    monkeypatch.setattr(matcher, "tfidf_similarity", lambda resumes, jd: {"a": 0.6})
    monkeypatch.setattr(matcher, "semantic_similarity", lambda resumes, jd: {})

    assert matcher.combined_similarity({"a": "text"}, "jd", 1, 3) == {"a": 0.6}
