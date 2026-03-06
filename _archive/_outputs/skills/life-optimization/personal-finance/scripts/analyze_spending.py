import pandas as pd
import argparse
import glob
import re
import os
import sys

# Default patterns (fallback if not loaded from file)
CATEGORY_PATTERNS = {
    'Income': r'payroll|direct\s?dep|gusto|adp|salary|interest|dividend',
    'Housing': r'rent|mortgage|lease|hoa|con\s?ed|utilities|water',
    'Transport': r'uber|lyft|mta|subway|metro|shell|bp|gas|parking',
    'Groceries': r'whole\s?fds|trader\s?joes|safeway|kroger|aldi|wegmans',
    'Dining': r'doordash|ubereats|grubhub|starbucks|chipotle|cafe|restaurant|bar',
    'Shopping': r'amazon|amzn|prime|target|walmart|costco|cvs|walgreens',
    'Subscriptions': r'netflix|spotify|aws|github|notion|nytimes|wsj',
    'Health': r'gym|equinox|fitness|doctor|dental'
}

def load_data(input_dir):
    """Loads all CSVs from the input directory into a single DataFrame."""
    files = glob.glob(os.path.join(input_dir, '*.csv'))
    if not files:
        print(f"No CSV files found in {input_dir}")
        sys.exit(1)
        
    df_list = []
    for f in files:
        try:
            # Try parsing with default options
            temp_df = pd.read_csv(f)
            
            # Normalize Columns
            cols = [c.lower() for c in temp_df.columns]
            temp_df.columns = cols
            
            # Find date column
            date_col = next((c for c in cols if 'date' in c), None)
            # Find amount column
            amount_col = next((c for c in cols if 'amount' in c or 'cost' in c), None)
            # Find description column
            desc_col = next((c for c in cols if 'desc' in c or 'merchant' in c or 'name' in c), None)
            
            if date_col and amount_col and desc_col:
                temp_df = temp_df[[date_col, amount_col, desc_col]].copy()
                temp_df.columns = ['date', 'amount', 'description']
                df_list.append(temp_df)
            else:
                print(f"Skipping {f}: Could not identify date/amount/description columns")
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    if not df_list:
        print("No valid data found.")
        sys.exit(1)
        
    full_df = pd.concat(df_list, ignore_index=True)
    full_df['date'] = pd.to_datetime(full_df['date'])
    return full_df

def categorize(description):
    """Categorizes a description based on regex patterns."""
    description = str(description).lower()
    for cat, pattern in CATEGORY_PATTERNS.items():
        if re.search(pattern, description, re.IGNORECASE):
            return cat
    return 'Uncategorized'

def detect_anomalies(df):
    """Detects transactions > 3 std devs from the category mean."""
    anomalies = []
    for cat, group in df.groupby('category'):
        if cat == 'Uncategorized':
            continue
        mean = group['amount'].mean()
        std = group['amount'].std()
        if pd.isna(std) or std == 0:
            continue
            
        outliers = group[((group['amount'] - mean).abs() / std) > 3]
        if not outliers.empty:
            anomalies.append(outliers)
            
    if anomalies:
        return pd.concat(anomalies)
    return pd.DataFrame()

def generate_report(df, output_file):
    """Generates a markdown report."""
    total_spend = df['amount'].sum()
    by_category = df.groupby('category')['amount'].agg(['sum', 'count']).reset_index()
    by_category.columns = ['Category', 'Total', 'Count']
    by_category['% of Total'] = (by_category['Total'] / total_spend * 100).round(1)
    by_category = by_category.sort_values('Total', ascending=False)
    
    anomalies = detect_anomalies(df)
    
    with open(output_file, 'w') as f:
        f.write(f"# 💸 Financial Report\n\n")
        f.write(f"**Total Processed:** ${total_spend:,.2f}\n")
        f.write(f"**Date Range:** {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}\n\n")
        
        f.write("## Category Breakdown\n")
        f.write(by_category.to_markdown(index=False, floatfmt=".2f"))
        f.write("\n\n")
        
        f.write("## 🚨 Anomalies / High Variance\n")
        if not anomalies.empty:
            f.write(anomalies[['date', 'description', 'amount', 'category']].to_markdown(index=False))
        else:
            f.write("No statistical anomalies detected.")
            
        f.write("\n\n")
        f.write("## Uncategorized Transactions\n")
        uncat = df[df['category'] == 'Uncategorized']
        if not uncat.empty:
            f.write(uncat[['date', 'description', 'amount']].head(10).to_markdown(index=False))
            if len(uncat) > 10:
                f.write(f"\n...and {len(uncat) - 10} more.")
        else:
            f.write("All transactions categorized! 🎉")

def main():
    parser = argparse.ArgumentParser(description='Analyze personal finances from CSVs')
    parser.add_argument('--input', required=True, help='Directory containing CSV files')
    parser.add_argument('--output', required=True, help='Output markdown file path')
    args = parser.parse_args()
    
    df = load_data(args.input)
    df['category'] = df['description'].apply(categorize)
    generate_report(df, args.output)
    print(f"Report generated at {args.output}")

if __name__ == "__main__":
    main()
