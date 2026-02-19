#!/usr/bin/env python3
"""
Comprehensive test suite for Fogg Cybersecurity Model
Students: Complete the TODO sections to implement tests
"""

import json
import os
from fogg_model import FoggBehaviorModel
from risk_prioritization import CybersecurityRiskPrioritizer


def _pass(msg: str):
    print(f"[PASS] {msg}")


def _fail(msg: str):
    print(f"[FAIL] {msg}")


def _assert_true(condition: bool, msg: str):
    if condition:
        _pass(msg)
        return True
    _fail(msg)
    return False


def test_fogg_model():
    """Test the basic Fogg model implementation"""
    print("=== Testing Fogg Model ===\n")

    fogg = FoggBehaviorModel()

    test_cases = [
        ("All zeros", {"motivation": 0, "ability": 0, "trigger": 0}, 0.0, "Low", "High"),
        ("All tens", {"motivation": 10, "ability": 10, "trigger": 10}, 100.0, "High", "Low"),
        ("Mixed mid", {"motivation": 5, "ability": 5, "trigger": 5}, 12.5, "Low", "High"),
        ("High M/A low T", {"motivation": 9, "ability": 9, "trigger": 2}, 16.2, "Low", "High"),
        ("High M/T low A", {"motivation": 9, "ability": 2, "trigger": 9}, 16.2, "Low", "High"),
        ("Edge over max clamp", {"motivation": 15, "ability": 12, "trigger": 11}, 100.0, "High", "Low"),
        ("Negative clamp", {"motivation": -3, "ability": -1, "trigger": -10}, 0.0, "Low", "High"),
    ]

    all_ok = True

    for name, profile, expected_score, expected_likelihood, expected_risk in test_cases:
        result = fogg.assess_cybersecurity_behavior(name, profile)
        score = result["scores"]["behavior_score"]
        likelihood = result["likelihood"]
        risk_level = result["risk_level"]
        recs = result["recommendations"]

        ok1 = _assert_true(abs(score - expected_score) < 0.01,
                           f"{name}: behavior_score expected {expected_score}, got {score}")
        ok2 = _assert_true(likelihood == expected_likelihood,
                           f"{name}: likelihood expected {expected_likelihood}, got {likelihood}")
        ok3 = _assert_true(risk_level == expected_risk,
                           f"{name}: risk_level expected {expected_risk}, got {risk_level}")

        if profile.get("motivation", 5) < 5 or \
           profile.get("ability", 5) < 5 or \
           profile.get("trigger", 5) < 5:
            ok4 = _assert_true(len(recs) > 0,
                               f"{name}: recommendations generated for weak component(s)")
        else:
            ok4 = _assert_true(len(recs) > 0,
                               f"{name}: recommendations present (maintenance acceptable)")

        all_ok = all_ok and ok1 and ok2 and ok3 and ok4

    trends = fogg.get_behavior_trends()
    ok_trends = _assert_true(
        "total_assessments" in trends and trends["total_assessments"] == len(test_cases),
        "Trends: total_assessments matches number of test cases"
    )
    all_ok = all_ok and ok_trends

    print("\n=== Fogg Model Tests Complete ===\n")
    return all_ok


def test_risk_prioritization():
    """Test the risk prioritization algorithm"""
    print("=== Testing Risk Prioritization ===\n")

    prioritizer = CybersecurityRiskPrioritizer()

    high_risk_users = [
        {"motivation": 2, "ability": 2, "trigger": 2},
        {"motivation": 3, "ability": 2, "trigger": 3},
    ]

    medium_risk_users = [
        {"motivation": 6, "ability": 5, "trigger": 5},
        {"motivation": 5, "ability": 6, "trigger": 5},
    ]

    low_risk_users = [
        {"motivation": 9, "ability": 9, "trigger": 9},
        {"motivation": 8, "ability": 9, "trigger": 8},
    ]

    prioritizer.add_risk_scenario("R-1", "Credential Phishing", 9.0, high_risk_users, 9.0)
    prioritizer.add_risk_scenario("R-2", "Weak Patch Hygiene", 8.0, medium_risk_users, 7.0)
    prioritizer.add_risk_scenario("R-3", "USB Usage Policy", 5.0, low_risk_users, 4.0)

    prioritized = prioritizer.prioritize_risks()

    ok1 = _assert_true(len(prioritized) == 3, "3 risks prioritized")

    scores = [r["priority_score"] for r in prioritized]
    ok2 = _assert_true(scores == sorted(scores, reverse=True),
                       "Risks sorted by priority_score descending")

    ok3 = _assert_true(all("priority_level" in r for r in prioritized),
                       "Each risk has a priority_level")

    ok4 = _assert_true(prioritized[0]["risk_name"] == "Credential Phishing",
                       "Top prioritized risk is Credential Phishing")

    ok5 = _assert_true(all(len(r.get("recommendations", [])) > 0 for r in prioritized),
                       "Recommendations generated for all risks")

    print("\n=== Risk Prioritization Tests Complete ===\n")
    return ok1 and ok2 and ok3 and ok4 and ok5


def test_data_export():
    """Test data export functionality"""
    print("=== Testing Data Export ===\n")

    fogg = FoggBehaviorModel()
    fogg.assess_cybersecurity_behavior("Test Behavior",
                                       {"motivation": 4, "ability": 4, "trigger": 4})
    fogg_file = "fogg_export_test.json"

    ok1 = _assert_true(fogg.export_data(fogg_file),
                       "Fogg model export_data returns True")

    ok2 = _assert_true(os.path.exists(fogg_file),
                       "Fogg export file created")

    try:
        with open(fogg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        ok3 = _assert_true(isinstance(data, list) and len(data) >= 1,
                           "Fogg export JSON content valid")
    except Exception:
        ok3 = _assert_true(False, "Fogg export JSON content valid")

    prioritizer = CybersecurityRiskPrioritizer()
    prioritizer.add_risk_scenario(
        "R-EXP", "Export Test Risk", 7.0,
        [{"motivation": 3, "ability": 3, "trigger": 3}],
        7.0
    )
    prioritizer.prioritize_risks()
    pri_file = "prioritized_export_test.json"

    ok4 = _assert_true(prioritizer.export_prioritized_risks(pri_file),
                       "Prioritizer export_prioritized_risks returns True")
    ok5 = _assert_true(os.path.exists(pri_file),
                       "Prioritized risks export file created")

    try:
        with open(pri_file, "r", encoding="utf-8") as f:
            pdata = json.load(f)
        ok6 = _assert_true(isinstance(pdata, list) and len(pdata) >= 1,
                           "Prioritized risks JSON content valid")
    except Exception:
        ok6 = _assert_true(False, "Prioritized risks JSON content valid")

    print("\n=== Data Export Tests Complete ===\n")
    return ok1 and ok2 and ok3 and ok4 and ok5 and ok6


def run_integration_test():
    """Run comprehensive integration test"""
    print("=== Integration Test ===\n")

    prioritizer = CybersecurityRiskPrioritizer()

    departments = {
        "Finance": [{"motivation": 7, "ability": 4, "trigger": 6},
                    {"motivation": 6, "ability": 5, "trigger": 5}],
        "HR": [{"motivation": 6, "ability": 4, "trigger": 4},
               {"motivation": 5, "ability": 4, "trigger": 5}],
        "IT": [{"motivation": 6, "ability": 8, "trigger": 4},
               {"motivation": 7, "ability": 9, "trigger": 5}],
        "Executives": [{"motivation": 5, "ability": 3, "trigger": 3},
                       {"motivation": 6, "ability": 3, "trigger": 2}],
    }

    prioritizer.add_risk_scenario("ORG-001",
                                  "Business Email Compromise",
                                  9.5,
                                  departments["Finance"],
                                  8.5)

    prioritized = prioritizer.prioritize_risks()
    report = prioritizer.generate_risk_report()

    ok1 = _assert_true(len(prioritized) == 1,
                       "Integration: risks prioritized")

    ok2 = _assert_true("CYBERSECURITY RISK PRIORITIZATION REPORT" in report,
                       "Integration: report generated with header")

    out_file = "integration_prioritized_risks.json"
    ok3 = _assert_true(prioritizer.export_prioritized_risks(out_file),
                       "Integration: export prioritized risks succeeded")

    ok4 = _assert_true(os.path.exists(out_file),
                       "Integration: exported file exists")

    print("\n=== Integration Test Complete ===\n")
    return ok1 and ok2 and ok3 and ok4


if __name__ == "__main__":
    ok_a = test_fogg_model()
    ok_b = test_risk_prioritization()
    ok_c = test_data_export()
    ok_d = run_integration_test()

    if ok_a and ok_b and ok_c and ok_d:
        print("\n=== All Tests Complete ===")
        print("Overall Result: PASS")
    else:
        print("\n=== All Tests Complete ===")
        print("Overall Result: FAIL")
