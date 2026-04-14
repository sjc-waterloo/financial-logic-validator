from src.auditor import FinancialAuditor

if __name__ == "__main__":
    # Updated paths to reflect the new data/ directory structure
    auditor = FinancialAuditor('data/mock_ai_output.json', 'data/industry_benchmarks.json')
    auditor.run()
    
    # Summary Console Output
    stats = auditor.get_summary_stats()
    print("\n" + "="*30)
    print(f"AUDIT SUMMARY FOR {stats['ticker']}")
    print(f"Final Status: {stats['status']}")
    print(f"Issues Found: {stats['error_count']}")
    if stats['critical_fail']:
        print("ALERT: Critical Accounting Failures Detected.")
    print("="*30)
