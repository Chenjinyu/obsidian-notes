Date: 2025-10-26
Course:
Tags: [[Testing]] [[CICD Pipeline]] [[Terminology]] [[Base Knowledge]] [[DevOps]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
## A/B testing
also known as split testing, is a method of comparing two versions of a digital asset—such as a website page, app, email, or advertisement—to determine which performs better. Users are randomly shown either the original version (A) or the variation (B), and their engagement and conversion rates are measured to identify which one achieves the desired business goal more effectively.  [1, 2, 3, 4]  
How it works 

1. Identify a Goal: Define a specific, measurable objective, like increasing conversions, click-through rates, or customer engagement. [4, 5]  
2. Create Variations: Make a single change to one element on the original asset to create a variation (B). This could be a new headline, image, call-to-action button, or page layout. [1, 2, 5, 6, 7, 8]  
3. Split Traffic: Randomly divide your target audience into two groups. [1, 5]  
4. Show Each Version: One group sees the control (A), while the other sees the new variation (B). [3]  
5. Collect Data: Track key performance metrics for both versions. [4, 5]  
6. Analyze Results: Statistically analyze the data to see which version performed better against your defined goal. [1, 5]  
7. Implement the Winner: Deploy the version that yielded the best results and discard the underperforming one. [4, 5]  

What can be tested 
A/B testing can be used for many digital assets, including: [2, 3, 9]  

• Website pages, including landing pages and components 
• Emails and newsletters 
• Advertisements and social media posts 
• Mobile app features and designs 
• Call-to-action buttons and form designs 

Benefits of A/B testing 
• Increased Conversions: Optimize elements to encourage more desired user actions. [4, 10, 11]  
• Improved User Experience: Make data-driven decisions to enhance user satisfaction and engagement. [5, 12]  
• Higher ROI: Make the most of your existing traffic and resources, leading to better business outcomes. [4]  
• Reduced Risk: Test changes with a small portion of your audience before a full rollout, minimizing potential negative impacts. [12, 13, 14]  

---

## What to instrument (FastAPI on ECS)

* Emit per-request events with: `user_id`, `variant`, `timestamp`, `endpoint`, and **conversion flag/value** (e.g., purchased? amount).
* Store to your warehouse (Redshift/Snowflake/BigQuery) and build a small daily job:

  ```sql
  -- Conversion example (one row per user)
  WITH last_assign AS (
    SELECT user_id, MAX_BY(variant, ts) AS variant -- or any sticky source
    FROM assignment_events
    GROUP BY 1
  ),
  outcomes AS (
    SELECT user_id, MAX(CASE WHEN purchased THEN 1 ELSE 0 END) AS converted
    FROM events
    WHERE ts BETWEEN :start AND :end
    GROUP BY 1
  )
  SELECT a.variant,
         COUNT(*) AS users,
         SUM(o.converted) AS converters,
         1.0 * SUM(o.converted)/COUNT(*) AS conversion_rate
  FROM last_assign a
  LEFT JOIN outcomes o USING (user_id)
  GROUP BY 1;
  ```
* Keep an **A/A test** occasionally to validate your randomization and analytics (should show no significant difference).

---

# Frequentist vs Bayesian (quick take)

* **Frequentist** (above): fixed sample, p-values, CIs. Simple, industry standard.
* **Bayesian**: posterior probability “B is better”, lets you **monitor continuously** with decision thresholds. Great for product teams, but pick one framework and stick to it.

---

# Common gotchas (avoid these)

* **SRM** (sample ratio mismatch): A\:B ≠ expected 50:50 → fix assignment/logging before trusting results.
* **Peeking**: stopping on a lucky spike increases false positives; use fixed horizon or proper sequential methods.
* **Non-independence**: mixing user-level and session-level metrics without deduping users.
* **Novelty effects**: run long enough to pass the initial excitement dip/spike.
* **Unit mismatch**: assign by **user**, not request; analyze **user-level** outcomes for most business metrics.

---

# Guardrails & kill-switches

* Set **max error-rate** or **p95 latency** thresholds; auto-disable B if exceeded.
* Use **feature flags** (e.g., LaunchDarkly, AWS AppConfig, homegrown) to flip variants safely.

---

# Tiny reference: z-test for conversion (no external libs)

```python
import math

def z_test_conv(success_a, total_a, success_b, total_b):
    p_a = success_a/total_a
    p_b = success_b/total_b
    p_pool = (success_a + success_b) / (total_a + total_b)
    se = math.sqrt(p_pool*(1-p_pool)*(1/total_a + 1/total_b))
    z = (p_b - p_a) / se
    # two-sided p-value from z (approx):
    from math import erf, sqrt
    pval = 2 * (1 - 0.5*(1 + erf(abs(z)/sqrt(2))))
    return {"p_a": p_a, "p_b": p_b, "lift_abs": p_b-p_a, "z": z, "pval": pval}
```

---

## Quick checklist to run your first good test

* [ ] One clear **primary metric** + 2–3 **guardrails**
* [ ] Baseline, **MDE**, α=0.05, power=0.8 → **sample size**
* [ ] **Sticky** randomization by user\_id (hash)
* [ ] Fixed test window (no peeking)
* [ ] Sanity checks: **SRM**, logging completeness
* [ ] Report: effect size, 95% CI, p-value, guardrails

If you share your baseline conversion and desired MDE, I can compute the exact sample size and sketch the run time given your daily traffic.



# Note


# Reference

