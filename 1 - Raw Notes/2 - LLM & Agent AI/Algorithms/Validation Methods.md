Date: 2025-10-26
Course:
Tags:  [[LLM]] [[ML]] [[Base Knowledge]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

### 🔹 1. **Holdout Cross-Validation**

**What it is**:

* You split the dataset into **two (or three) parts**:

  * Training set (e.g., 70–80%)
  * Test set (e.g., 20–30%)
  * (Optionally) Validation set for hyperparameter tuning.

**When to use**:

* When you have **lots of data** (splitting still leaves enough for training & testing).
* For a **quick baseline** evaluation.

**Downside**:

* Performance depends heavily on the random split.
* Risk of **high variance** in results.

### 🔹 2. **K-Fold Cross-Validation**

**What it is**:

* Split data into **K folds** (e.g., K=5 or 10).
* Train on K–1 folds and test on the remaining fold.
* Repeat K times (each fold used once as test).
* Average performance across folds = final score.

**When to use**:

* When you want **more reliable estimates** of performance.
* Works well with **small/medium datasets**, where a single holdout test isn’t enough.

**Difference vs Holdout**:

* K-fold reduces variance by testing on multiple splits instead of one.
* More computationally expensive.

### 🔹 3. **Stratified K-Fold Cross-Validation**

**What it is**:

* Same as K-fold, but ensures **class proportions are preserved** in each fold.

  * Example: If dataset has 90% negative and 10% positive, each fold keeps the same ratio.

**When to use**:

* When dealing with **imbalanced datasets** (fraud detection, medical data, etc.).
* Ensures fairer evaluation across folds.

**Difference vs K-Fold**:

* K-fold may create folds with skewed class ratios.
* Stratified K-fold keeps class distribution balanced in every fold.

#### More Detail Explaination for Stratified K-Fold Cross Validation
##### 🔹 What Cross-Validation Really Does

* **Yes**, we are **training** the model multiple times (once per fold).
* But the **purpose** is **not** to get a final trained model — it’s to **evaluate** how well the model generalizes to unseen data.

Each fold is like a **mini experiment**:

1. Split the data into training (K–1 folds) and validation (1 fold).
2. Train on training folds.
3. Validate (evaluate) on the held-out fold.
4. Repeat for every fold.
5. Average the validation scores → this is your **cross-validation estimate of model performance**.

##### 🔹 Why It Looks Like Training

* During cross-validation, the model **is trained K times**.
* But **those models are temporary** → they exist only to test performance on the validation folds.
* At the end, you **throw them away**.

Only after cross-validation do you typically:
👉 Retrain one **final model** on the **entire dataset** (with tuned hyperparameters).

##### 🔹 Analogy

Think of cross-validation like **practice exams**:

* You split your study material into K chunks.
* Each time, you “train” on K–1 chunks and test yourself on the held-out chunk.
* You’re not keeping those mini test scores for real life — but they tell you how prepared you are.
* After practice, you take the **final exam** (train on all data, deploy the model).

##### ✅ In Short

* **Cross-validation is an evaluation technique**, not the final training.
* The repeated training is just a **means to validate** performance fairly.
* Final step = retrain the chosen model on **all the data** before using it in production.

👉 Do you want me to extend the script to **show both parts** clearly:

1. Cross-validation (for evaluation).
2. Final training on the full dataset (for deployment)?


### 🔹 4. **Accuracy**

**What it is**:

* A **performance metric** = proportion of correct predictions.

$$
\text{Accuracy} = \frac{\text{Correct Predictions}}{\text{Total Predictions}}
$$

**When to use**:

* Good when **classes are balanced**.
* Example: Cat vs Dog classification with equal samples.

**When NOT to use**:

* Bad for **imbalanced datasets**.

  * Example: 99% normal, 1% fraud → predicting everything as normal gives 99% accuracy (but useless).
* In such cases, better metrics: **Precision, Recall, F1-score, AUC**.


### ✅ Summary Table

| Technique / Metric    | What it Does                           | Best Used When                          | Key Difference                   |
| --------------------- | -------------------------------------- | --------------------------------------- | -------------------------------- |
| **Holdout**           | Simple train/test split                | Large datasets, quick baseline          | Single split, can be unstable    |
| **K-Fold**            | Multiple splits, average performance   | Small/medium datasets, stable estimates | More compute, less variance      |
| **Stratified K-Fold** | K-fold but preserves class proportions | Imbalanced datasets                     | Avoids skewed folds              |
| **Accuracy**          | Metric: % correct predictions          | Balanced datasets                       | Misleading if data is imbalanced |

---

⚡ Would you like me to also show a **Python example** where we compare Holdout vs K-Fold vs Stratified K-Fold (with sklearn), so you can see the differences in practice?


# Note


# Reference

