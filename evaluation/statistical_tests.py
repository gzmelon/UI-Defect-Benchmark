"""
Statistical testing for NS-CQA evaluation:
- McNemar's test
- Bootstrap 95% CI for F1
- Cohen's d and Cliff's delta
"""
import numpy as np
from scipy.stats import chi2
from sklearn.metrics import f1_score

def mcnemar_test(y_true, y_pred_a, y_pred_b):
    correct_a = (y_pred_a == y_true)
    correct_b = (y_pred_b == y_true)
    b = np.sum(correct_a & ~correct_b)
    c = np.sum(~correct_a & correct_b)
    if b + c == 0:
        return 1.0
    stat = (abs(b - c) - 1)**2 / (b + c)
    p = 1 - chi2.cdf(stat, df=1)
    return p

def bootstrap_f1_ci(y_true, y_pred, n_bootstrap=1000, alpha=0.05):
    rng = np.random.default_rng(42)
    scores = []
    n = len(y_true)
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        scores.append(f1_score(y_true[idx], y_pred[idx], average='macro'))
    lower = np.percentile(scores, 100*alpha/2)
    upper = np.percentile(scores, 100*(1-alpha/2))
    return np.mean(scores), (lower, upper)

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std if pooled_std > 0 else 0.0

def cliffs_delta(group1, group2):
    n1, n2 = len(group1), len(group2)
    greater = sum(1 for x in group1 for y in group2 if x > y)
    lesser = sum(1 for x in group1 for y in group2 if x < y)
    return (greater - lesser) / (n1 * n2)
