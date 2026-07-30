# Model comparison

| Model | Accuracy | Macro F1 | Avg latency (ms/sample) |
|---|---|---|---|
| TF-IDF + CalibratedClassifierCV(LinearSVC) | 1.0000 | 1.0000 | 0.019 |
| sentence-embeddings (all-MiniLM-L6-v2) + LogisticRegression | 1.0000 | 1.0000 | 1.389 |

**Decision:** Shipping 'TF-IDF + CalibratedClassifierCV(LinearSVC)' - it matches or beats model B (0.0000 macro-F1 ahead) while staying lighter.