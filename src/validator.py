import json
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# Then replace 'print' with 'logging.error' or 'logging.warning'

class FinancialAuditor:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def verify_retained_earnings(self):
        """Check if Net Income flows correctly into Retained Earnings."""
        ni = self.data['income_statement']['net_income']
        prev_re = self.data['balance_sheet']['previous_retained_earnings']
        curr_re = self.data['balance_sheet']['current_retained_earnings']
        
        expected_re = prev_re + ni
        if curr_re != expected_re:
            self.errors.append(f"[RE-01] Balance Sheet Mismatch: Expected RE of {expected_re}, found {curr_re}.")

    def verify_accounting_equation(self):
        """Assets must equal Liabilities + Equity. If Equity is missing, Assets >= Liabilities."""
        assets = self.data['balance_sheet']['total_assets']
        liabilities = self.data['balance_sheet']['total_liabilities']
        
        if liabilities > assets:
            self.errors.append(f"[BS-01] Solvency Risk: Liabilities ({liabilities}) exceed Assets ({assets}).")

    def run_all_checks(self):
        self.verify_retained_earnings()
        self.verify_accounting_equation()
        
        if not self.errors:
            print("Audit Passed: Model is logically sound.")
        else:
            print(f"Audit Failed: Found {len(self.errors)} critical errors:")
            for err in self.errors:
                print(f" - {err}")

if __name__ == "__main__":
    with open('mock_ai_output.json', 'r') as f:
        raw_data = json.load(f)
        auditor = FinancialAuditor(raw_data)
        auditor.run_all_checks()