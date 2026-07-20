<a id="top"></a>

# Clickbait Rewriter

Many news websites use headlines that hide key information, exaggerate emotion, or encourage users to click before understanding the main point. This project rewrites potentially clickbait headlines using article-level context, helping readers understand the main idea before deciding whether to open the article.

This project is a personal rebuild and extension of an undergraduate research project originally developed with teammates under Taiwan's NSTC Undergraduate Research Project program.

<details>
<summary><strong>Table of Contents</strong></summary>

- [Demo](#demo)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)
- [API Overview](#api-overview)
- [Evaluation](#evaluation)
- [Testing](#testing)
- [Limitations](#limitations)

</details>

## Demo

### End-to-end workflow on Yahoo News Taiwan

![Yahoo demo](assets/demo_yahoo.gif)

### UDN headline highlighting

![UDN highlight](assets/udn_highlight.png)

### ETtoday rewrite result

![ETtoday rewrite](assets/ettoday_rewrite.png)

### Popup

![Popup](assets/popup.png)

## Architecture

Overall workflow:

``` text
News website
→ Chrome Extension
→ FastAPI backend
→ Headline classification
→ Article extraction
→ Gemini rewrite
→ Highlight & tooltip display
```

``` mermaid
flowchart TD
    A[Supported News Websites] --> B[Chrome Extension]
    B --> C[Headline Candidate Extraction]
    C --> D[FastAPI Backend]

    D --> E[Clickbait Classifier]
    E --> F[Yellow Highlight]
    F --> B

    B -- User hovers --> D
    D --> G[Article Extractor]
    G --> H[Gemini Rewriter]
    H --> I[Tooltip: Original + Rewritten]
    I --> B
```

## Features

-   Supports Yahoo News Taiwan, ETtoday, and UDN
-   Detects and highlights clickbait-style headlines on supported news websites
-   Extracts article content from the original news page
-   Rewrites headlines with Gemini using article-level context
-   Shows live processing status and rewritten results in a tooltip
-   Control headline highlighting and hover-based rewriting from the popup

## Tech Stack

### Frontend

-   Chrome Extension Manifest V3
-   JavaScript
-   CSS

### Backend

-   Python
-   FastAPI
-   Pydantic
-   Trafilatura
-   Readability
-   BeautifulSoup
-   Hugging Face Transformers
-   Google Gemini API

## Project Structure

``` text
clickbait-rewriter/
├── assets/
├── backend/
│   ├── main.py         # FastAPI entry point
│   ├── config.py       # Configuration
│   ├── schemas.py      # Pydantic models
│   └── services/
│       ├── classifier.py
│       ├── article_extractor.py
│       └── rewriter.py
├── extension/
├── evaluation/         # Evaluation results
├── tests/              # Pytest test suite
├── requirements.txt
├── .env.example
└── README.md
```

## Running the Project

### Install Dependencies

``` bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure Environment Variables

Create a local `.env` file:

``` bash
cp .env.example .env
```

Fill in the required values:

``` env
CLASSIFIER_MODE=model
CLASSIFIER_MODEL_NAME=Stremie/xlm-roberta-base-clickbait

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash-lite

CLICKBAIT_THRESHOLD=0.3
```

### Start the Backend

``` bash
python -m uvicorn backend.main:app --reload
```

Backend URLs:

``` text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

### Load the Chrome Extension

1.  Open `chrome://extensions/`
2.  Enable **Developer mode**
3.  Click **Load unpacked**
4.  Select the `extension/` folder

### Usage

Open a supported news website and hover over highlighted headlines to view rewritten versions generated from article-level context.

## API Overview

The FastAPI backend exposes four main endpoints:

``` text
GET  /health        # Check backend status
POST /api/classify  # Classify headline candidates
POST /api/extract   # Extract article content
POST /api/rewrite   # Rewrite headline with article context
```

Interactive API documentation is available at:

``` text
http://127.0.0.1:8000/docs
```

## Evaluation

Evaluation datasets and results are available in the `evaluation/` directory.

## Testing

Run all tests:

```bash
pytest
```

Current test status:

```text
28 passed
```

## Limitations

-   Article extraction quality depends on each website's HTML structure.
-   Gemini API quota may limit rewrite availability.
-   Generated rewrites may still require prompt tuning for different news categories.

<p align="right">
  <a href="#top">Back to top ↑</a>
</p>