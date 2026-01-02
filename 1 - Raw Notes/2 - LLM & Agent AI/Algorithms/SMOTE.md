Date: 2025-10-26
Course:
Tags: [[LLM]] [[Terminology]] [[ML]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
The **Synthetic Minority Oversampling Technique (SMOTE)** is a popular method in **machine learning** for handling **imbalanced datasets**, especially in **classification problems**.

## 🔹 Why SMOTE is Needed
* In many real-world datasets, one class (the **majority class**) has **much more data** than the other (the **minority class**).
* Example: Fraud detection → 99% transactions are normal, 1% are fraud.
* Standard ML models trained on such data often become biased, predicting mostly the majority class.

## 🔹 What SMOTE Does
* Instead of just **duplicating existing minority samples**, SMOTE creates **new synthetic samples**.
* It does this by:

  1. Taking a minority sample.
  2. Finding its **k nearest neighbors** (usually k=5).
  3. Randomly selecting one neighbor.
  4. Generating a **synthetic sample** along the line between the sample and its neighbor.

This way, the minority class becomes better represented without simple duplication.

## 🔹 Example
Suppose we have two features (x1, x2):

* A minority point at (2, 3)
* Its neighbor at (3, 4)
* SMOTE may generate a new point at (2.4, 3.4), which lies between them.

## 🔹 Benefits
* Balances the dataset → improves model’s ability to detect minority class.
* Helps avoid **overfitting** that happens with naive oversampling (just copying rows).
* Widely used in fraud detection, medical diagnosis, churn prediction, etc.

## 🔹 Limitations
* Can create **ambiguous samples** if classes overlap.
* Not always suitable for **high-dimensional** data (noise gets amplified).
* Needs careful parameter tuning (like k-nearest neighbors).

✅ **In short**:
SMOTE is a **data preprocessing technique** that generates **synthetic samples of the minority class** to balance imbalanced datasets and improve classification performance.

--- 


Perfect 👍 Let’s walk through a simple **Python example** using `imblearn`’s implementation of **SMOTE**.

### 🔹 Install Required Package

If you don’t already have `imbalanced-learn` installed:

```bash
pip install imbalanced-learn scikit-learn
```

### 🔹 Python Example with SMOTE

```python
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE

# 1. Create an imbalanced dataset
X, y = make_classification(n_classes=2, class_sep=2,
                           weights=[0.9, 0.1],  # 90% vs 10%
                           n_informative=3, n_redundant=1, flip_y=0,
                           n_features=2, n_clusters_per_class=1,
                           n_samples=500, random_state=42)

print("Original class distribution:", Counter(y))

# 2. Apply SMOTE
smote = SMOTE(random_state=42, k_neighbors=5)
X_res, y_res = smote.fit_resample(X, y)

print("Resampled class distribution:", Counter(y_res))

# 3. Visualize before and after
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Original
ax1.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', edgecolor='k')
ax1.set_title("Before SMOTE (Imbalanced)")

# Resampled
ax2.scatter(X_res[:, 0], X_res[:, 1], c=y_res, cmap='coolwarm', edgecolor='k')
ax2.set_title("After SMOTE (Balanced)")

plt.show()
```

### 🔹 What Happens Here

1. We create an **imbalanced dataset** (90% class 0, 10% class 1).
2. We run **SMOTE** to generate synthetic minority samples.
3. We print class distribution **before and after**:
   ```
   Original class distribution: Counter({0: 450, 1: 50})
   Resampled class distribution: Counter({0: 450, 1: 450})
   ```
4. The plot will show:
   * **Before**: class 1 is tiny compared to class 0.
   * **After**: both classes are balanced with synthetic points.



# Note


# Reference

