# 🎤 Interview Q&A — Lab 2: Cyber Threat Intelligence (CTI) Integration

## 1) What is CTI (Cyber Threat Intelligence)?
CTI is threat data + context (IOCs, TTPs, actor behavior) used to improve detection, prevention, and response.

## 2) What are Indicators of Compromise (IOCs)?
Observable artifacts like hashes, IPs, domains/URLs, file names, or registry keys that indicate malicious activity.

## 3) Why normalize CTI feeds?
Feeds come in different formats and fields. Normalization allows consistent scoring, searching, and reporting across sources.

## 4) Why use multiple CTI sources?
One feed rarely covers everything; combining sources increases coverage and reduces blind spots.

## 5) Why do CTI feeds include comment headers?
Many public feeds include metadata (last updated time, format info) and legal notes at the top.

## 6) What is the difference between an IP indicator and a URL indicator?
IP is a network endpoint; URLs/domains are user-facing and often used in phishing or malware delivery.

## 7) Why is “human-targeting” detection important?
Many attacks succeed through user interaction (phishing clicks, credential entry, social engineering).

## 8) What is risk scoring in CTI context?
It’s a way to convert qualitative intelligence (High/Medium/Low) into a numeric priority for action.

## 9) Why treat trusted sources differently?
A trusted source improves confidence, reducing false positives and helping prioritize response faster.

## 10) What are common CTI response actions?
Block at DNS/proxy/firewall, update EDR rules, hunt in logs, isolate endpoints, and investigate affected users.

## 11) Why produce spreadsheets if we already have JSON?
Security teams and leadership often use spreadsheets for review, reporting, filtering, and operational tracking.

## 12) Why generate a risk matrix?
A matrix turns raw priorities into response categories (Critical/High/Medium/Low), aligning response with SLA.

## 13) What is the limitation of using only “Top 10” for a risk matrix?
It does not represent the full dataset; it shows prioritized examples, not complete coverage.

## 14) How would you operationalize this in a SOC?
Automate ingestion (cron), store in DB, integrate with SIEM, and correlate indicators with live telemetry.

## 15) What is the key takeaway from this lab?
CTI becomes actionable when it’s structured, scored, prioritized, and tied to concrete response steps—especially human-focused threats.
