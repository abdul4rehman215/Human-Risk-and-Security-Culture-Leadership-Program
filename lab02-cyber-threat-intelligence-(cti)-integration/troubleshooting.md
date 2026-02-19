# 🛠️ Troubleshooting Guide — Lab 2: Cyber Threat Intelligence (CTI) Integration

## Issue 1: `curl` download fails or returns HTML
### Cause
Some feeds redirect or require `-L` to follow redirects.

### Fix
```bash
curl -L -o data/file.csv "URL"
````

---

## Issue 2: SSL verification error during downloads

### Cause

Environment certificate or proxy issues.

### Fix (temporary / last resort)

```bash
curl --insecure -L -o data/file.csv "URL"
```

---

## Issue 3: CSV parsing errors / broken rows

### Cause

Feed contains comment headers and inconsistent rows.

### Fix

* Ensure scripts skip lines starting with `#`
* Use `errors="ignore"` (already used)
* Inspect file format:

```bash
file -i data/malware_hashes.csv
head -n 20 data/malware_hashes.csv
```

---

## Issue 4: Empty output datasets

### Cause

Files not downloaded correctly or wrong paths.

### Fix

```bash
ls -lh data/
head -n 20 data/malware_hashes.csv
head -n 20 data/feodo_ips.csv
head -n 20 data/urlhaus_domains.csv
python3 scripts/process_cti.py
```

---

## Issue 5: JSON formatting error

### Fix

```bash
python3 -m json.tool output/master_cti_dataset.json
python3 -m json.tool output/risk_assessment_report.json
```

---

## Issue 6: LibreOffice won’t open / hangs

### Fix

```bash
killall soffice.bin
libreoffice --calc output/cti_main_sheet.csv &
```

---

## Issue 7: `firefox: command not found`

### Cause

Firefox not installed in lab VM.

### Fix

Use system opener:

```bash
xdg-open output/threat_dashboard.html &
```

---

## Issue 8: Risk Matrix shows only “Top 10”

### Cause

The risk matrix script uses `top_10_prioritized_threats` from `risk_assessment_report.json`.

### Fix (Optional Enhancement)

To build a full matrix, re-score all 150 indicators from `output/master_cti_dataset.json` directly.

