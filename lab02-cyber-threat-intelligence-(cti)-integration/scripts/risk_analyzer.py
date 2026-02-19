#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any


class CTIRiskAnalyzer:
    def __init__(self, data_file: str):
        """Initialize analyzer with CTI data."""
        # Load JSON data from file
        with open(data_file, "r", encoding="utf-8") as f:
            self.data: List[Dict[str, Any]] = json.load(f)

        # Define risk_matrix with weights for high/medium/low
        self.risk_matrix = {
            "High": 5,
            "Medium": 3,
            "Low": 1
        }

        # Define trusted sources
        self.trusted_sources = {"MalwareBazaar", "Feodo Tracker", "URLhaus"}

        # Social engineering keywords to detect in descriptions/indicator values
        self.social_engineering_terms = [
            "login", "password", "verify", "account", "urgent", "invoice", "payment",
            "reset", "security", "update", "support", "admin", "microsoft", "office",
            "bank", "paypal", "alert"
        ]

        # Malware families that often target end users (example list)
        self.user_targeting_malware_families = [
            "agenttesla", "redline", "lokibot", "remcos", "formbook", "raccoon", "vidar"
        ]

    def analyze_threat_landscape(self):
        """
        Perform threat landscape analysis.

        Calculate and display:
        - Total indicator count
        - Threat level distribution (percentages)
        - Source distribution
        - Indicator type distribution
        """
        total = len(self.data)
        print("\n===== THREAT LANDSCAPE ANALYSIS =====")
        print(f"Total indicators: {total}")

        if total == 0:
            print("No indicators found. Ensure dataset exists and processing succeeded.")
            return

        threat_levels = Counter([rec.get("threat_level", "Unknown") for rec in self.data])
        sources = Counter([rec.get("source", "Unknown") for rec in self.data])
        types = Counter([rec.get("type", "Unknown") for rec in self.data])

        print("\nThreat Level Distribution:")
        for level, cnt in threat_levels.items():
            pct = (cnt / total) * 100
            print(f" - {level}: {cnt} ({pct:.1f}%)")

        print("\nSource Distribution:")
        for src, cnt in sources.most_common():
            pct = (cnt / total) * 100
            print(f" - {src}: {cnt} ({pct:.1f}%)")

        print("\nIndicator Type Distribution:")
        for t, cnt in types.most_common():
            pct = (cnt / total) * 100
            print(f" - {t}: {cnt} ({pct:.1f}%)")

    def calculate_priority_score(self, record: Dict[str, Any]) -> int:
        """
        Calculate priority score (1-15) based on multiple factors.

        Factors:
        - Threat level weight × 3
        - Source reliability: +2 for trusted sources
        - Indicator type: URL/Domain=+3, IP=+2, Hash=+1
        - Recency: +1 if recent timestamp

        Args:
            record: Indicator dictionary

        Returns:
            Integer priority score (1-15)
        """
        score = 0

        # Calculate base score from threat level
        tl = record.get("threat_level", "Low")
        base_weight = self.risk_matrix.get(tl, 1)
        score += base_weight * 3

        # Add source reliability factor
        if record.get("source") in self.trusted_sources:
            score += 2

        # Add indicator type factor
        itype = (record.get("type") or "").lower()
        if "url" in itype or "domain" in itype:
            score += 3
        elif "ip" in itype:
            score += 2
        elif "hash" in itype:
            score += 1

        # Add recency factor if timestamp exists
        ts = record.get("timestamp", "")
        if ts:
            # best-effort parse date
            # many feeds provide "YYYY-MM-DD HH:MM:SS" or "YYYY-MM-DD"
            recent = False
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
                try:
                    dt = datetime.strptime(ts.strip(), fmt)
                    if dt >= datetime.now() - timedelta(days=7):
                        recent = True
                    break
                except Exception:
                    continue
            if recent:
                score += 1

        # Cap at 15 and floor at 1
        if score > 15:
            score = 15
        if score < 1:
            score = 1

        return score

    def prioritize_threats(self) -> List[Dict[str, Any]]:
        """
        Prioritize all threats and return sorted list.

        Returns:
        List of threat dictionaries sorted by priority_score
        """
        prioritized = []

        for rec in self.data:
            ps = self.calculate_priority_score(rec)

            action = "Monitor"
            timeline = "Ongoing"
            if ps >= 12:
                action = "Immediate Response"
                timeline = "Within 24 hours"
            elif ps >= 8:
                action = "Urgent Investigation"
                timeline = "Within 72 hours"
            elif ps >= 5:
                action = "Scheduled Review"
                timeline = "Within 2 weeks"

            enriched = dict(rec)
            enriched["priority_score"] = ps
            enriched["recommended_action"] = action
            enriched["response_timeline"] = timeline

            prioritized.append(enriched)

        prioritized.sort(key=lambda x: x.get("priority_score", 0), reverse=True)

        print("\n===== TOP 10 PRIORITIZED THREATS =====")
        for i, t in enumerate(prioritized[:10], start=1):
            print(f"{i}. [{t.get('priority_score')}] {t.get('type')} | {t.get('indicator_value')} | "
                  f"{t.get('threat_level')} | {t.get('source')} | {t.get('recommended_action')}")

        return prioritized

    def analyze_human_risk_factors(self) -> List[Dict[str, Any]]:
        """
        Identify threats targeting human vulnerabilities.

        Human risk indicators:
        - URLs/Domains (direct user interaction)
        - Social engineering keywords
        - User-targeting malware families

        Returns:
        List of human-targeting threats with risk scores
        """
        human_threats = []

        for rec in self.data:
            human_score = 0
            itype = (rec.get("type") or "").lower()
            val = (rec.get("indicator_value") or "").lower()
            desc = (rec.get("description") or "").lower()
            fam = (rec.get("malware_family") or "").lower()

            # Score URLs/domains higher (+3)
            if "url" in itype or "domain" in itype:
                human_score += 3

            # Check for social engineering terms (+2)
            if any(term in val or term in desc for term in self.social_engineering_terms):
                human_score += 2

            # Check for user-targeting malware (+2)
            if fam and any(m in fam for m in self.user_targeting_malware_families):
                human_score += 2

            if human_score > 0:
                enriched = dict(rec)
                enriched["human_risk_score"] = human_score
                human_threats.append(enriched)

        human_threats.sort(key=lambda x: x.get("human_risk_score", 0), reverse=True)

        print("\n===== TOP 5 HUMAN-TARGETING THREATS =====")
        for i, t in enumerate(human_threats[:5], start=1):
            print(f"{i}. [HumanScore={t.get('human_risk_score')}] {t.get('type')} | {t.get('indicator_value')} | "
                  f"{t.get('threat_level')} | {t.get('source')}")

        return human_threats

    def generate_recommendations(self, prioritized: List[Dict[str, Any]], human_risks: List[Dict[str, Any]]) -> List[str]:
        """
        Generate actionable security recommendations.

        Categories:
        - Immediate Actions (for high-priority threats)
        - Human Risk Mitigation
        - Ongoing Security Improvements
        """
        recommendations = []

        recommendations.append("## Immediate Actions")
        high_priority = [t for t in prioritized if t.get("priority_score", 0) >= 12]
        if high_priority:
            recommendations.append("- Block high-priority URLs/domains and IPs at firewall/proxy/DNS.")
            recommendations.append("- Quarantine endpoints matching malware hashes and run full AV/EDR scans.")
            recommendations.append("- Review email gateway logs for delivery of suspicious links/domains.")
        else:
            recommendations.append("- No threats reached 'Immediate Response' threshold in current dataset.")

        recommendations.append("\n## Human Risk Mitigation")
        if human_risks:
            recommendations.append("- Run targeted phishing awareness campaigns focusing on login/account verification themes.")
            recommendations.append("- Enforce MFA and password manager usage, especially for roles frequently targeted.")
            recommendations.append("- Provide user guidance on reporting suspicious emails/links immediately.")
        else:
            recommendations.append("- No strong human-targeting indicators detected; continue routine awareness training.")

        recommendations.append("\n## Ongoing Security Improvements")
        recommendations.append("- Automate daily CTI ingestion and re-scoring of indicators.")
        recommendations.append("- Integrate CTI into SIEM for correlation with authentication, proxy, and endpoint logs.")
        recommendations.append("- Periodically review and tune scoring thresholds and trusted source list.")

        return recommendations

    def generate_report(self, output_file: str) -> Dict[str, Any]:
        """Generate comprehensive risk assessment report."""
        self.analyze_threat_landscape()
        prioritized = self.prioritize_threats()
        human_risks = self.analyze_human_risk_factors()
        recommendations = self.generate_recommendations(prioritized, human_risks)

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_indicators": len(self.data),
            "top_10_prioritized_threats": prioritized[:10],
            "top_5_human_targeting_threats": human_risks[:5],
            "recommendations": recommendations,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"\nReport saved to: {output_file}")
        return report


def main():
    analyzer = CTIRiskAnalyzer("output/master_cti_dataset.json")

    # Run all analysis methods and generate final report
    analyzer.generate_report("output/risk_assessment_report.json")


if __name__ == "__main__":
    main()
