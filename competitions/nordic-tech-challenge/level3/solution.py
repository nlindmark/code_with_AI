#!/usr/bin/env python3
"""
EV Charging Load Balancing - Reference Solution

Find peak power demand across charging schedule.
"""

def find_peak_power_demand(schedule_data):
    """
    Find the peak simultaneous power demand from EV charging schedule.
    
    Args:
        schedule_data: String with format:
                      VehicleID,StartTime,EndTime,ChargingRate
    
    Returns:
        int: Peak power demand in kW
    """
    lines = schedule_data.strip().split('\n')
    
    # Parse charging sessions
    sessions = []
    max_hour = 0
    for line in lines:
        parts = line.split(',')
        start = int(parts[1])
        end = int(parts[2])
        rate = int(parts[3])
        sessions.append((start, end, rate))
        max_hour = max(max_hour, end)
    
    # Calculate power demand for each hour
    peak_demand = 0
    for hour in range(0, max_hour + 1):
        current_demand = 0
        for start, end, rate in sessions:
            # Check if this session is active during this hour
            if start <= hour < end:
                current_demand += rate
        peak_demand = max(peak_demand, current_demand)
    
    return peak_demand


if __name__ == "__main__":
    # Read charging schedule
    with open("charging_schedule.txt", "r") as f:
        data = f.read()
    
    # Find peak
    peak = find_peak_power_demand(data)
    
    # Output result
    print(f"{peak}")  # Expected: 135
