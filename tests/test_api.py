from fastapi.testclient import TestClient

from backend.main import app
from backend import main

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "clickbait-rewriter-api"


def test_classify(monkeypatch):
    monkeypatch.setattr(
        main,
        "classify_candidates",
        lambda candidates: [
            {
                "id": "1",
                "title": "測試標題",
                "url": "https://example.com",
                "classification": {
                    "label": "clickbait",
                    "score": 0.9,
                    "mode": "mock",
                },
            }
        ],
    )

    response = client.post(
        "/api/classify",
        json={
            "candidates": [
                {
                    "id": "1",
                    "title": "測試標題",
                    "url": "https://example.com",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_extract(monkeypatch):
    monkeypatch.setattr(
        main,
        "extract_article",
        lambda url: {
            "url": url,
            "success": True,
            "title": "新聞標題",
            "text": "新聞內容",
            "textLength": 4,
            "method": "mock",
            "error": None,
        },
    )

    response = client.post(
        "/api/extract",
        json={"url": "https://example.com"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rewrite(monkeypatch):
    monkeypatch.setattr(
        main,
        "rewrite_title",
        lambda original_title, article_text: {
            "success": True,
            "originalTitle": original_title,
            "rewrittenTitle": "新的標題",
            "reason": "更客觀",
            "mode": "mock",
            "error": None,
        },
    )

    response = client.post(
        "/api/rewrite",
        json={
            "originalTitle": "舊標題",
            "articleText": "文章內容",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation():
    assert client.post("/api/classify", json={}).status_code == 422
    assert client.post("/api/extract", json={}).status_code == 422
    assert client.post("/api/rewrite", json={}).status_code == 422