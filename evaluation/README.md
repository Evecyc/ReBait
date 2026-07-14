# Evaluation

This folder contains a small-scale manual evaluation of Clickbait Rewriter using Taiwanese news headlines collected from Yahoo News Taiwan, ETtoday, and UDN.

## Scope

The evaluation includes:

-   clickbait classification evaluation
-   headline rewrite quality evaluation
-   error analysis

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

### Results

### Analysis

## Error Analysis