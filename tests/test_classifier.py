import pytest

from backend.services.classifier import (
    CLICKBAIT_LABEL,
    NON_CLICKBAIT_LABEL,
    classify_title,
    mock_classify_title,
    normalize_model_label,
    to_clickbait_score,
)
from backend.services import classifier


@pytest.mark.parametrize(
    "raw_label, expected",
    [
        ("LABEL_1", CLICKBAIT_LABEL),
        ("label_1", CLICKBAIT_LABEL),
        ("1", CLICKBAIT_LABEL),
        ("clickbait", CLICKBAIT_LABEL),
        ("ClickBait", CLICKBAIT_LABEL),
        ("LABEL_0", NON_CLICKBAIT_LABEL),
        ("non_clickbait", NON_CLICKBAIT_LABEL),
        ("non-clickbait", NON_CLICKBAIT_LABEL),
        ("unknown", NON_CLICKBAIT_LABEL),
    ],
)
def test_normalize_model_label(raw_label, expected):
    assert normalize_model_label(raw_label) == expected


def test_to_clickbait_score():
    assert to_clickbait_score(CLICKBAIT_LABEL, 0.82) == pytest.approx(0.82)
    assert to_clickbait_score(NON_CLICKBAIT_LABEL, 0.18) == pytest.approx(0.82)


def test_mock_classify_non_clickbait():
    result = mock_classify_title("總統今天出席記者會")

    assert result["label"] == NON_CLICKBAIT_LABEL
    assert result["mode"] == "mock"
    assert result["score"] == pytest.approx(0.18)


def test_mock_classify_clickbait():
    result = mock_classify_title("驚！真相曝光")

    assert result["label"] == CLICKBAIT_LABEL
    assert result["mode"] == "mock"
    assert result["score"] > 0.55


def test_mock_classify_score_cap():
    result = mock_classify_title(
        "驚！震驚！曝光！真相！原因！內幕！超狂！慘了！爆！瘋傳！"
    )

    assert result["label"] == CLICKBAIT_LABEL
    assert result["score"] <= 0.95


def test_classify_title_mock_mode(monkeypatch):
    monkeypatch.setattr(classifier.settings, "classifier_mode", "mock")

    result = classify_title("驚！真相曝光")

    assert result["mode"] == "mock"
    assert result["label"] == CLICKBAIT_LABEL