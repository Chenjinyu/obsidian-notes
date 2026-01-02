Date: 2025-10-26
Course:
Tags: [[LLM]] [[ML]] [[Base Knowledge]] [[Terminology]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
# 🔹 1. **Multi-Class Classification**

**Definition**:

* Each sample belongs to **exactly one class** out of **three or more possible classes**.
* Classes are **mutually exclusive**.

**Examples**:

* Handwritten digit recognition (digits 0–9 → each image is only one digit).
* Animal classification (cat, dog, horse → each image has only one label).
* Sentiment analysis (positive, negative, neutral).

**Key points**:

* One sample = **one label only**.
* Often uses **softmax activation** in neural networks to pick the most likely class.

---

# 🔹 2. **Multi-Label Classification**

**Definition**:

* Each sample can belong to **multiple classes simultaneously**.
* Classes are **not mutually exclusive**.

**Examples**:

* Movie genre classification (a movie can be Comedy + Romance + Drama).
* News tagging (an article might be tagged with *politics*, *economy*, *health*).
* Image recognition (a picture may contain *car*, *tree*, *person*).

**Key points**:

* One sample = **one or more labels**.
* Typically uses **sigmoid activation** (independent probabilities per class).
* Evaluation metrics differ (e.g., hamming loss, F1-score per label).

---

# 🔄 **Differences at a Glance**

| Aspect                          | **Multi-Class**                       | **Multi-Label**                                   |
| ------------------------------- | ------------------------------------- | ------------------------------------------------- |
| **Number of labels per sample** | Exactly 1                             | One or more (0–N)                                 |
| **Class relationship**          | Mutually exclusive                    | Non-exclusive                                     |
| **Examples**                    | Digit recognition, Sentiment analysis | Movie genres, News topics, Multi-object detection |
| **Model output**                | One class (highest probability)       | Multiple classes (thresholded probabilities)      |
| **Activation function**         | Softmax                               | Sigmoid                                           |


# ✅ Summary

* **Multi-class** = “Choose **one** from many.”
* **Multi-label** = “Choose **any combination** from many.”

---

## 🔹 1. Multi-class preview (Iris dataset)

This table shows **5 flower samples** from the Iris dataset. Each row has:

* The **flower features** (sepal length, sepal width, petal length, petal width).
* The **true\_label** → the real flower species.
* The **pred\_label** → what the model predicted.

👉 Since this is **multi-class**, each flower has **exactly one label**.

**Example row (simplified):**

| sepal length | sepal width | petal length | petal width | true\_label | pred\_label |
| ------------ | ----------- | ------------ | ----------- | ----------- | ----------- |
| 6.7          | 3.1         | 4.4          | 1.4         | versicolor  | versicolor  |

```sh
Sample: Flower
 ├── True label: Virginica
 └── Predicted label: Versicolor   ❌ (wrong, because only ONE choice is allowed)
```

Meaning: This flower really is *versicolor*, and the model also predicted *versicolor* (correct).

## 🔹 2. Multi-label preview (Synthetic dataset)

This table shows **5 samples** from a **synthetic dataset** where each sample can belong to **multiple classes at once**.

* `true_labels`: the actual set of labels assigned to the sample.
* `pred_labels`: the labels the model predicted.
* Labels are shown as **class IDs** like `(0, 3)` meaning "this sample belongs to class 0 and class 3".

👉 Since this is **multi-label**, each sample can have **more than one label**, or even none.

**Example row:**

| true\_labels | pred\_labels |
| ------------ | ------------ |
| (0, 2)       | (0, 2, 4)    |

```sh
Sample: Movie
 ├── True labels: [Comedy, Romance]
 └── Predicted labels: [Comedy, Romance, Action]  
       → 2 correct (Comedy, Romance) + 1 wrong extra (Action)
```
Meaning: This sample truly belongs to classes **0 and 2**.
The model predicted **0, 2, and 4** → so it got 0 and 2 correct, but also added a wrong extra label (4).

## ✅ Key takeaway

* **Multi-class table** → every row has **one true label** and **one predicted label**.
* **Multi-label table** → every row has **a set of true labels** and **a set of predicted labels** (can overlap partly, fully, or have mistakes).




# Note


# Reference

