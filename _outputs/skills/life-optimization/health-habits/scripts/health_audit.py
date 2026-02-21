import pandas as pd
import argparse
import matplotlib.pyplot as plt
import sys

def analyze_health(input_file, activity_filter=None):
    try:
        df = pd.read_csv(input_file)
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter
    if activity_filter:
        df = df[df['activity'].str.contains(activity_filter, case=False, na=False)]
        
    if df.empty:
        print("No data found.")
        return

    # Stats
    total_duration = df['duration_mins'].sum()
    count = len(df)
    
    # Streak Calculation
    df = df.sort_values('date')
    dates = df['date'].dt.date.unique()
    dates.sort()
    
    current_streak = 0
    if len(dates) > 0:
        import datetime
        today = datetime.date.today()
        # check if start is today or yesterday
        last_entry = dates[-1]
        if (today - last_entry).days <= 1:
            current_streak = 1
            for i in range(len(dates)-2, -1, -1):
                if (dates[i+1] - dates[i]).days == 1:
                    current_streak += 1
                else:
                    break
        else:
            current_streak = 0
            
    # Output ASCII visualization
    print(f"# Health Report {'- ' + activity_filter if activity_filter else ''}")
    print(f"**Total Sessions:** {count}")
    print(f"**Total Duration:** {total_duration} mins")
    print(f"**Current Streak:** {current_streak} days 🔥")
    
    print("\n## Recent Log")
    print(df[['date', 'activity', 'metric_value', 'metric_unit']].tail().to_markdown(index=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--filter', help='Filter by activity')
    args = parser.parse_args()
    
    analyze_health(args.input, args.filter)
