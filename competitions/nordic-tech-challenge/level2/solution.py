#!/usr/bin/env python3
"""
LoRaWAN Sensor Analysis - Reference Solution

Calculate average temperature from LoRaWAN sensor network data.
"""

def calculate_average_temperature(csv_data):
    """
    Calculate average temperature from sensor CSV data.
    
    Args:
        csv_data: String containing CSV with format:
                 SensorID,Temperature,RSSI,Battery
    
    Returns:
        float: Average temperature rounded to 1 decimal place
    """
    lines = csv_data.strip().split('\n')
    temperatures = []
    
    for line in lines:
        parts = line.split(',')
        temp = float(parts[1])
        temperatures.append(temp)
    
    avg_temp = sum(temperatures) / len(temperatures)
    return round(avg_temp, 1)


if __name__ == "__main__":
    # Read sensor data
    with open("sensor_data.csv", "r") as f:
        data = f.read()
    
    # Calculate average
    avg = calculate_average_temperature(data)
    
    # Output result
    print(f"{avg}")  # Expected: 18.7
