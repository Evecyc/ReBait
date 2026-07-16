# Evaluation

This folder contains a small-scale manual evaluation of Clickbait Rewriter using Taiwanese news headlines collected from Yahoo News Taiwan, ETtoday, and UDN.

## Scope

The evaluation includes:

-   clickbait classification evaluation
-   headline rewrite quality evaluation
-   overall system analysis

## Classification Evaluation

### Labels

-   `clickbait`: headline hides key information, uses suspense, exaggeration, emotional wording, or encourages clicking to reveal the main point
-   `non_clickbait`: headline directly states the main subject and event without misleading or suspenseful wording

### Method

The classification evaluation uses 100 manually labeled Taiwanese news headlines collected from Yahoo News Taiwan, ETtoday, and UDN.

The dataset is balanced with 50 clickbait and 50 non-clickbait headlines. The classifier was evaluated using a custom clickbait threshold of 0.3.

### Results

| Metric    | Score |
|-----------|------:|
| Accuracy  | 82.0% |
| Precision | 86.4% |
| Recall    | 76.0% |
| F1 Score  | 80.9% |

### Confusion Matrix

|                      | Predicted clickbait | Predicted non-clickbait |
|----------------------|--------------------:|------------------------:|
| Actual clickbait     |                  38 |                      12 |
| Actual non-clickbait |                   6 |                      44 |

### Analysis

The classifier achieved an overall accuracy of 82.0% with an F1 score of 80.9% on the manually labeled evaluation set.

Precision was higher than recall, indicating reliable clickbait predictions, while the custom threshold of 0.3 increased the detection of borderline clickbait headlines.

Most misclassifications were associated with ambiguous wording or emotionally expressive but factual headlines.

## Rewrite Quality Evaluation

### Criteria

Each criterion is rated from 1 (poor) to 5 (excellent):

-   `clarity`: whether the rewritten headline is easy to understand
-   `informativeness`: whether hidden key information is clearly revealed
-   `faithfulness`: whether the rewritten headline accurately reflects the article without adding unsupported information
-   `readability`: whether the headline reads naturally as a news headline in Traditional Chinese

### Method

The rewrite evaluation uses 25 manually selected clickbait headlines collected from Yahoo News Taiwan, ETtoday, and UDN.

Each rewritten headline was manually evaluated using the four criteria above, and the overall result is calculated as the average score of the four criteria.

### Results

| Metric | Score |
|--------|------:|
| Clarity | 4.84 |
| Informativeness | 4.44 |
| Faithfulness | 5.00 |
| Readability | 4.68 |
| Overall | **4.74 / 5.00** |

### Analysis

The rewritten headlines consistently preserved the original article content while reducing sensational or ambiguous wording.

Faithfulness achieved the highest score, indicating that the system rarely introduced unsupported information. Lower scores were primarily associated with headlines that did not fully reveal hidden information or occasionally resembled news summaries rather than concise headlines.

## Overall Analysis

The classification and rewrite evaluations demonstrate that the system can reliably detect clickbait headlines and generate more informative, neutral, and faithful alternatives.

The main remaining limitations include borderline clickbait headlines that are difficult to classify, rewritten headlines that occasionally omit part of the hidden information, and dependency on the Gemini API, whose free-tier quota and service availability may affect rewriting performance.