#!/usr/bin/env python3
"""
Statistical analysis helpers for Kirkpatrick evaluation
"""

import numpy as np
from scipy import stats


def calculate_cohens_d(pre_scores, post_scores):
    """
    Calculate Cohen's d effect size.
    """
    pre = np.array(pre_scores, dtype=float)
    post = np.array(post_scores, dtype=float)

    sd_pre = np.std(pre, ddof=1)
    sd_post = np.std(post, ddof=1)

    pooled_sd = np.sqrt(((sd_pre ** 2) + (sd_post ** 2)) / 2)

    if pooled_sd == 0:
        return 0.0

    d = (np.mean(post) - np.mean(pre)) / pooled_sd
    return float(d)


def perform_ttest(pre_scores, post_scores):
    """
    Perform paired t-test for learning significance.
    """
    pre = np.array(pre_scores, dtype=float)
    post = np.array(post_scores, dtype=float)

    t_stat, p_value = stats.ttest_rel(post, pre, nan_policy="omit")
    return float(t_stat), float(p_value)


def calculate_confidence_interval(data, confidence=0.95):
    """
    Calculate confidence interval for mean.
    """
    arr = np.array(data, dtype=float)
    arr = arr[~np.isnan(arr)]

    if len(arr) == 0:
        return 0.0, 0.0

    mean = np.mean(arr)
    se = stats.sem(arr)

    if se == 0:
        return float(mean), float(mean)

    h = se * stats.t.ppf((1 + confidence) / 2.0, len(arr) - 1)
    return float(mean - h), float(mean + h)


def calculate_correlation(metric1, metric2):
    """
    Calculate correlation between two metrics.
    """
    x = np.array(metric1, dtype=float)
    y = np.array(metric2, dtype=float)

    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]

    if len(x) < 2:
        return 0.0, 1.0

    r, p = stats.pearsonr(x, y)
    return float(r), float(p)
