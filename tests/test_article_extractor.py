import pytest

from backend.services.article_extractor import (
    apply_patterns,
    clean_text,
    get_html_title,
    postprocess_article_text,
    remove_common_noise,
    remove_duplicate_title_prefix,
    remove_end_blocks,
    remove_prefix_blocks,
    remove_related_reading_sections,
)


def test_clean_text():
    assert clean_text("  Hello   World  ") == "Hello World"
    assert clean_text(None) == ""
    assert clean_text("") == ""


def test_get_html_title():
    html = """
    <html>
        <head>
            <meta property="og:title" content="OG Title">
            <title>HTML Title</title>
        </head>
    </html>
    """

    assert get_html_title(html) == "OG Title"


def test_apply_patterns():
    text = "Hello Google News"
    result = apply_patterns(text, [r"Google\s*News"])

    assert result == "Hello"


def test_remove_prefix_blocks():
    text = (
        "AI重點 文章重點整理："
        "- 重點一：今天下雨。"
        "- 重點二：請帶傘。"
        "正式新聞內容開始。"
    )

    assert "AI重點" not in remove_prefix_blocks(text)


def test_remove_end_blocks():
    text = "今天真的下雨。更多相關新聞 明天放晴。"

    result = remove_end_blocks(text)

    assert result == "今天真的下雨。"


def test_remove_related_reading_sections():
    text = (
        "今天真的下雨。"
        "👉延伸閱讀 今天會更冷。"
        "其他人也在看..."
    )

    result = remove_related_reading_sections(text)

    assert "延伸閱讀" not in result


def test_remove_common_noise():
    text = (
        "YT:https://youtube.com/abc "
        "https://example.com "
        "今天真的下雨"
    )

    result = remove_common_noise(text)

    assert "http" not in result
    assert "YT" not in result
    assert "今天真的下雨" in result


def test_remove_duplicate_title_prefix():
    title = "今天真的下雨"

    text = (
        "今天真的下雨 "
        "今天真的下雨了，記得帶傘。"
    )

    result = remove_duplicate_title_prefix(title, text)

    assert result.startswith("今天真的下雨了")


def test_postprocess_article_text():
    text = (
        "今天真的下雨。 "
        "YT:https://youtube.com/test "
        "更多相關新聞 明天放晴。"
    )

    result = postprocess_article_text(text)

    assert "YT" not in result
    assert "更多相關新聞" not in result