import pandas as pd
import argparse
import sys

def audit_calendar(input_file):
    """
    Audits a CSV calendar export for Deep Work vs Meetings.
    Expected columns: Subject, Start Date, Start Time, End Date, End Time
    """
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return

    # Normalize columns (Google Calendar export standard)
    # Usually: 'Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event'
    df.columns = [c.strip() for c in df.columns]
    
    # Combine Date+Time
    try:
        df['Start'] = pd.to_datetime(df['Start Date'] + ' ' + df['Start Time'])
        df['End'] = pd.to_datetime(df['End Date'] + ' ' + df['End Time'])
        df['Duration'] = (df['End'] - df['Start']).dt.total_seconds() / 3600 # Hours
    except KeyError:
        print("Error: Could not find Start/End Date/Time columns. Check CSV format.")
        return

    # Filters
    keywords = ['meeting', 'sync', 'call', '1:1', 'zoom', 'huddle', 'standup']
    pattern = '|'.join(keywords)
    
    df['Is_Meeting'] = df['Subject'].str.contains(pattern, case=False, na=False) | (df['Duration'] < 0.75)
    
    # Metrics
    total_hours = df['Duration'].sum()
    meeting_hours = df[df['Is_Meeting']]['Duration'].sum()
    deep_work_hours = df[~df['Is_Meeting'] & (df['Duration'] >= 1.5)]['Duration'].sum()
    
    # Fragmentation logic: Gaps < 60 mins between events
    df = df.sort_values('Start')
    df['Gap'] = (df['Start'] - df['End'].shift(1)).dt.total_seconds() / 60
    fragmented_gaps = df[(df['Gap'] > 0) & (df['Gap'] < 60)]
    
    # Output
    print(f"# 📅 Time Audit Report")
    print(f"**Total Tracked:** {total_hours:.1f} hrs")
    print(f"**Meeting Load:** {meeting_hours:.1f} hrs ({(meeting_hours/total_hours)*100:.1f}%)")
    print(f"**Deep Work:** {deep_work_hours:.1f} hrs ({(deep_work_hours/total_hours)*100:.1f}%)")
    
    print("\n## ⚠️ Fragmentation Alert")
    print(f"Found {len(fragmented_gaps)} small gaps (Swiss Cheese schedule).")
    if not fragmented_gaps.empty:
         print(fragmented_gaps[['Start Date', 'Start Time', 'Gap', 'Subject']].head().to_markdown(index=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Calendar CSV export')
    args = parser.parse_args()
    
    audit_calendar(args.input)
