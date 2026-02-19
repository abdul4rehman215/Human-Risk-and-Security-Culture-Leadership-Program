# 🎤 Interview Q&A — Lab 05: Role-Based Risk Identification

## 1️⃣ What is role-based risk identification?

Role-based risk identification is a security assessment approach that evaluates risks based on organizational roles rather than individual users. It considers access levels, data sensitivity, privilege levels, and exposure to determine the security posture of each role.

---

## 2️⃣ Why are executives considered high-risk roles?

Executives typically:
- Have access to highly sensitive strategic data
- Possess administrative privileges
- Have high external exposure
- Are prime targets for spear phishing and social engineering attacks

This combination significantly increases their risk profile.

---

## 3️⃣ How does Cyber Threat Intelligence (CTI) improve risk analysis?

CTI provides real-world threat context.  
Instead of static scoring, CTI allows:
- Threat severity weighting
- Targeted role adjustments
- Context-aware risk amplification
- Realistic prioritization

This increases accuracy of risk scoring.

---

## 4️⃣ What factors were used to calculate the base risk score?

The weighted formula used:
```
(access_level * 0.3 +
data_sensitivity * 0.25 +
external_exposure * 0.25 +
privilege_level * 0.2) * 10
```
These factors represent core security exposure dimensions.

---

## 5️⃣ Why are department multipliers important?

Department multipliers:
- Reflect organizational criticality
- Adjust prioritization dynamically
- Align technical risk with business impact
- Improve governance decision-making

Example: Executive department multiplier = 1.2

---

## 6️⃣ What does a CRITICAL risk classification indicate?

A CRITICAL role:
- Has very high exposure or privilege
- Is a high-value attack target
- Requires enhanced monitoring
- Should have strong access control policies
- Needs frequent review and auditing

---

## 7️⃣ How does this tool support proactive defense?

The tool:
- Identifies high-risk roles early
- Generates mitigation recommendations
- Enables prioritization
- Automates risk scoring
- Supports continuous assessment

---

## 8️⃣ What are examples of generated recommendations?

For CRITICAL/HIGH roles:
- Enforce Multi-Factor Authentication (MFA)
- Implement privileged access monitoring
- Conduct frequent access reviews
- Apply enhanced monitoring and alerting

---

## 9️⃣ Why is automation important in risk management?

Manual assessment:
- Is inconsistent
- Is slow
- Is error-prone

Automation:
- Standardizes scoring
- Enables repeatable analysis
- Scales across large organizations
- Supports compliance documentation

---

## 🔟 How can this be applied in real-world environments?

This model can be integrated into:
- IAM governance programs
- SOC prioritization workflows
- Insider threat detection systems
- Risk-based access control strategies
- Compliance reporting frameworks (ISO 27001, NIST, etc.)

---

## 1️⃣1️⃣ What is the benefit of generating visualization charts?

Visualization:
- Helps management understand risk distribution
- Identifies high-risk departments quickly
- Supports executive decision-making
- Makes reporting easier

---

## 1️⃣2️⃣ How does risk classification support compliance?

Role-based risk classification:
- Aligns with least privilege principle
- Supports audit readiness
- Demonstrates proactive risk management
- Provides documented evidence of security controls

---

# ✅ Summary

This lab demonstrates how organizational structure directly impacts security risk posture.  
By integrating CTI, automation, and classification logic, risk analysis becomes dynamic, contextual, and actionable.
