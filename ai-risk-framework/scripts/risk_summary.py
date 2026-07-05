"""
risk_summary.py

Reads a CSV export of the SupportBot v2 risk register and prints a
priority-ordered summary (highest Risk Score first), plus a count of
risks requiring immediate action.

Usage:
    python3 scripts/risk_summary.py register/risk-register.csv
"""
import csv
import sys


def load_register(filepath):
    risks = []
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['Risk Score'] = int(row['Likelihood']) * int(row['Impact'])
                risks.append(row)
            except (ValueError, KeyError):
                continue
    return risks


def print_summary(risks):
    sorted_risks = sorted(risks, key=lambda x: x['Risk Score'], reverse=True)
    print(f"\n{'='*72}")
    print(f"{'SUPPORTBOT V2 - RISK REGISTER SUMMARY':^72}")
    print(f"{'='*72}")
    for r in sorted_risks:
        level = r.get('Risk Level', 'Unknown')
        print(f"[{r['Risk ID']}] Score: {r['Risk Score']:>3} | {level:<8} | "
              f"{r['Threat Description'][:55]}")
    print(f"{'='*72}")

    critical = [r for r in risks if r['Risk Score'] >= 20]
    high = [r for r in risks if 15 <= r['Risk Score'] < 20]
    print(f"Critical risks requiring immediate action: {len(critical)}")
    print(f"High risks requiring near-term action:      {len(high)}")
    print(f"Total risks registered:                      {len(risks)}\n")


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "register/risk-register.csv"
    risks = load_register(filepath)
    print_summary(risks)
