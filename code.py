from datetime import datetime, timedelta

def calculate_earliest_date(n, y, d, absences):
    # Convert absences into datetime objects
    absence_periods = []
    for start, end in absences:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        absence_periods.append((start_date, end_date))
    
    # Sort absences by start date
    absence_periods.sort()
    
    # Calculate the total days required
    required_days = y * d
    
    # Start checking from the last date in the absences list
    last_absence_date = max(end for _, end in absence_periods)
    current_date = last_absence_date + timedelta(days=1)
    
    # Iterate backward to find the earliest date meeting the requirement
    while True:
        # Calculate the 5-year window
        start_window = current_date - timedelta(days=5 * 365)
        days_present = 0
        
        # Calculate days present in the 5-year window
        current = start_window
        for start, end in absence_periods:
            if end < start_window:
                continue
            if start > current_date:
                break
            if current < start:
                days_present += (start - current).days
            current = max(current, end + timedelta(days=1))
        
        # Add remaining days in the window
        if current <= current_date:
            days_present += (current_date - current).days + 1
        
        # Check if the days present meet the requirement
        if days_present >= required_days:
            return current_date.strftime("%Y-%m-%d")
        
        # Move to the next day
        current_date += timedelta(days=1)

# Input reading
n, y, d = map(int, input().split())
absences = [input().split() for _ in range(n)]

# Solve the problem
result = calculate_earliest_date(n, y, d, absences)
print(result)
