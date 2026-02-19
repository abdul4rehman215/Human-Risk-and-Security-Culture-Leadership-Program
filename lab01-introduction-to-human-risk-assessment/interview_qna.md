# 🎤 Interview Q&A — Lab 1: Introduction to Human Risk Assessment

## 1. What is human risk in cybersecurity?
Human risk refers to vulnerabilities introduced by user behavior, lack of awareness, or cultural weaknesses in an organization.

## 2. Why is human risk measurement important?
Because most modern breaches exploit human factors such as phishing, weak passwords, or social engineering.

## 3. Why use SQLite for this lab?
SQLite is lightweight, serverless, and ideal for local prototyping and analytics workflows.

## 4. What does a 0–100 risk score represent?
It normalizes behavior-based responses into a measurable security posture score.

## 5. Why is higher score considered lower risk?
Because survey responses are designed so higher values indicate better security practices.

## 6. Why separate categories (password, email, social engineering)?
To identify specific behavioral weaknesses instead of relying on a single global score.

## 7. Why use weighted scoring?
Not all categories carry equal risk impact; weighting improves realistic assessment.

## 8. Why enable foreign keys in SQLite?
To maintain referential integrity between participants and responses.

## 9. What security issue can arise with Apache + SQLite?
Permission errors when the web server user (www-data) cannot access the database file.

## 10. How can this system scale?
By replacing SQLite with PostgreSQL and integrating with SIEM or awareness platforms.

## 11. What does 75% Medium Risk mean?
Most users exhibit moderate security posture with room for improvement.

## 12. What category scored lowest?
Social engineering — indicating phishing susceptibility risk.

## 13. Why generate sample data?
To simulate realistic behavior and test the analytics pipeline.

## 14. How does visualization help?
It communicates risk posture clearly to non-technical stakeholders.

## 15. What is the key takeaway?
Human behavior is measurable and manageable with structured analytics.
