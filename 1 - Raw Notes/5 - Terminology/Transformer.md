Date: 2025-10-26
Course:
Tags: [[Terminology]] [[ML]] [[LLM]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

In **`sklearn.preprocessing`**, the `Scaler` classes are utilities for **feature scaling**.

## 🔹 What is a Scaler?

A **Scaler** in scikit-learn is a transformer that **changes the scale of your feature values** (columns in your dataset).

* Many machine learning algorithms (e.g., SVMs, Logistic Regression, KNN, Neural Nets) are **sensitive to feature magnitudes**.
* Scaling makes sure features are **comparable** and avoids one feature dominating because it has bigger numeric ranges.
* All Scalers follow the same API:

  * `.fit(X)` → learn parameters (mean, std, min, IQR, etc.) from data.
  * `.transform(X)` → scale the data.
  * `.fit_transform(X)` → do both in one call.


## 🔹 Main Scalers in `sklearn.preprocessing`

| Scaler                                      | Formula                                                     | When to Use                                                                           |            |                                                                                         |
| ------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------- |
| **StandardScaler**                          | $X' = \frac{X - \mu}{\sigma}$                               | Data roughly Gaussian; want mean 0, variance 1.                                       |            |                                                                                         |
| **MinMaxScaler**                            | $X' = \frac{X - X_{min}}{X_{max} - X_{min}}$                | Scale into a fixed range (default \[0,1]); good for NN or bounded features.           |            |                                                                                         |
| **MaxAbsScaler**                            | ( X' = \frac{X}{                                            | X                                                                                     | \_{max}} ) | Keeps sparsity; scales features to \[-1,1]. Useful for sparse data (e.g., text counts). |
| **RobustScaler**                            | $X' = \frac{X - \text{median}}{\text{IQR}}$                 | When data has **outliers** (median & IQR are robust stats).                           |            |                                                                                         |
| **Normalizer** (not exactly a Scaler)       | $X' = \frac{X}{\|X\|_p}$                                    | Scale each **row** (sample) to unit norm. Useful for text vectors, cosine similarity. |            |                                                                                         |
| **QuantileTransformer**                     | Maps to uniform \[0,1] or normal distribution via quantiles | When you want to squash outliers and get a uniform/normal-like distribution.          |            |                                                                                         |
| **PowerTransformer** (Yeo-Johnson, Box-Cox) | Applies power transform                                     | Makes skewed data more Gaussian-like.                                                 |            |                                                                                         |

## 🔹 Quick Example

```python
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

X = np.array([[1.0], [2.0], [2.1], [10.0]])  # has an outlier

print("StandardScaler:", StandardScaler().fit_transform(X).ravel())
print("MinMaxScaler:  ", MinMaxScaler().fit_transform(X).ravel())
print("RobustScaler:  ", RobustScaler().fit_transform(X).ravel())
```

Output (approx):

```
StandardScaler: [-0.85 -0.54 -0.51  1.91]
MinMaxScaler:   [0.0 0.111 0.122 1.0]
RobustScaler:   [-0.5 0.0  0.05  4.0]
```

Notice:

* **StandardScaler** got “pulled” by the outlier.
* **MinMaxScaler** squeezed most values into a small range because of the outlier.
* **RobustScaler** ignored the outlier more gracefully.


✅ In short:
`xxxScaler` in sklearn are just different **ways of rescaling your features** depending on whether you care about mean/std, min/max, outliers, or distribution shape.


## Python Script Example
```py
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

num_mild = ["age", "income"]
num_outlier = ["txn_amt", "duration"]
cat = ["state", "plan"]

pre = ColumnTransformer([
    ("num_std", StandardScaler(), num_mild),
    ("num_rob", RobustScaler(), num_outlier),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat)
])

clf = Pipeline([
    ("pre", pre),
    ("model", LogisticRegression(max_iter=1000))
])
clf.fit(X_train, y_train)

```

#### 1. Import statements

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
```

* `Pipeline`: lets you chain steps (preprocessing + model) into one object with `.fit` / `.predict`.
* `ColumnTransformer`: applies different preprocessing to different subsets of columns.
* `StandardScaler`: standardizes numerical features (subtract mean, divide by std).
* `RobustScaler`: scales numerical features using median & IQR (resistant to outliers).
* `OneHotEncoder`: turns categorical variables into binary dummy columns.
* `LogisticRegression`: a linear classifier.

#### 2. Feature groups

```python
num_mild = ["age", "income"]
num_outlier = ["txn_amt", "duration"]
cat = ["state", "plan"]
```

We’re grouping features by **what kind of preprocessing they need**:

* `num_mild`: numeric features with mild or no outliers → good candidates for **StandardScaler**.
* `num_outlier`: numeric features with big outliers (e.g. transaction amounts) → use **RobustScaler**.
* `cat`: categorical features (string-like, e.g. states, plans) → need **OneHotEncoder**.

#### 3. Preprocessing step

```python
pre = ColumnTransformer([
    ("num_std", StandardScaler(), num_mild),
    ("num_rob", RobustScaler(), num_outlier),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat)
])
```

* **ColumnTransformer** = “apply transformer X to these columns.”
* `("num_std", StandardScaler(), num_mild)`
  → Apply StandardScaler to `age`, `income`.
* `("num_rob", RobustScaler(), num_outlier)`
  → Apply RobustScaler to `txn_amt`, `duration`.
* `("cat", OneHotEncoder(handle_unknown="ignore"), cat)`
  → Apply OneHotEncoder to categorical columns.

  * `handle_unknown="ignore"` ensures that if a category appears in test data but wasn’t seen in train, it won’t break — it just ignores it.

So `pre` will output a **new feature matrix** where:

* `age` and `income` are standardized,
* `txn_amt` and `duration` are robust-scaled,
* `state` and `plan` become multiple binary columns.

#### 4. Build the pipeline

```python
clf = Pipeline([
    ("pre", pre),
    ("model", LogisticRegression(max_iter=1000))
])
```

This chains two steps:

1. `"pre"` → apply `pre` ColumnTransformer to raw input.
2. `"model"` → run LogisticRegression on the transformed features.

#### 5. Fit the model

```python
clf.fit(X_train, y_train)
```

* `X_train`: your original raw DataFrame (with columns: age, income, txn\_amt, duration, state, plan).
* `y_train`: your target labels (e.g., churn yes/no).

During `.fit()`:

1. `pre.fit(X_train)` learns scaling parameters:

   * StandardScaler stores mean & std of `age` and `income`.
   * RobustScaler stores median & IQR of `txn_amt` and `duration`.
   * OneHotEncoder learns all unique categories of `state` and `plan`.
2. `pre.transform(X_train)` creates the processed feature matrix.
3. LogisticRegression trains on that processed matrix.

At prediction time (`clf.predict(X_test)`), the same preprocessing is applied **automatically** with the saved parameters — ensuring no data leakage.

#### 6. Why this design is powerful

* **Consistency**: ensures test/production data goes through identical preprocessing.
* **Safety**: avoids train/test mismatch (e.g., scaling with test mean).
* **Flexibility**: easily mix scalers, encoders, custom transformers.
* **Searchable**: whole pipeline can be passed to `GridSearchCV` or `RandomizedSearchCV`.

#### 🔹 Example Walkthrough

Say you have one row of data:

```text
age=40, income=60000, txn_amt=2000, duration=30, state="TX", plan="Gold"
```

Pipeline transforms it into something like:

```text
[-0.23,  0.57,  1.95, 0.11,  0, 1, 0,  ... ]
```

* First two values = standardized `age`, `income`.
* Next two = robust-scaled `txn_amt`, `duration`.
* Rest = one-hot columns for `state` and `plan`.

Logistic regression then works on this numeric feature vector.

✅ In short:
This script builds a **production-ready ML pipeline** that **cleans, scales, encodes, and trains** in one unified object, ensuring **no leakage** and smooth deployment.



# Note


# Reference

