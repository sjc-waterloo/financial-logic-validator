import json
import logging

# Set up logging for professional audit trails
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class FinancialAuditor:
    def __init__(self, model_path, config_path):
        with open(model_path, 'r') as f:
            self.data = json.load(f)
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.errors = []
        self.rationale = []

    def check_hallucinations(self):
        """Checks if AI output exceeds realistic industry benchmarks."""
        sector = "tech_sector" # Hardcoded for this demo
        tg = self.data['assumptions']['terminal_growth']
        max_tg = self.config[sector]['max_terminal_growth']
        
        if tg > max_tg:
            msg = f"Hallucination Warning: Terminal Growth of {tg*100}% exceeds the threshold of {max_tg*100}%."
            self.errors.append(f"[H-01] {msg}")
            self.rationale.append(f"The model assumes infinite growth higher than historical GDP, which is a common AI hallucination.")

    def verify_financial_integrity(self):
        """Checks internal consistency between financial statements."""
        is_data = self.data['income_statement']
        bs_data = self.data['balance_sheet']
        
        # Check 1: Retained Earnings Flow
        expected_re = bs_data['previous_retained_earnings'] + is_data['net_income']
        if bs_data['current_retained_earnings'] != expected_re:
            self.errors.append("[BS-01] Retained Earnings Mismatch.")
            self.rationale.append(f"Net Income of {is_data['net_income']} should result in Retained Earnings of {expected_re}, but model shows {bs_data['current_retained_earnings']}.")

    def generate_markdown_report(self):
        """Outputs a professional audit report for AI trainers."""
        report = "# AI Model Audit Report\n\n"
        report += f"**Status:** {'FAILED' if self.errors else 'PASSED'}\n\n"
        report += "## Critical Errors\n"
        for err in self.errors:
            report += f"- {err}\n"
        
        report += "\n## Trainer Rationale (to be used in Labelbox feedback)\n"
        for rat in self.rationale:
            report += f"> {rat}\n\n"
            
        with open('audit_report.md', 'w') as f:
            f.write(report)
        print("Audit report generated: audit_report.md")

    def get_summary_stats(self):
        """Returns a dictionary of findings for high-level reporting."""
        return {
            "ticker": self.data.get("ticker", "Unknown"),
            "status": "FAIL" if self.errors else "PASS",
            "error_count": len(self.errors),
            "critical_fail": any("[BS" in err for err in self.errors) # Flag Balance Sheet errors as critical
        }

    def run(self):
        logging.info("Starting financial audit...")
        self.check_hallucinations()
        self.verify_financial_integrity()
        self.generate_markdown_report()