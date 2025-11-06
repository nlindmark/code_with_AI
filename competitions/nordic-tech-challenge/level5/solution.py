#!/usr/bin/env python3
"""
Nordic Winter Battery Degradation - Reference Solution

Calculate total energy loss percentage from battery test data.
"""

def calculate_energy_loss_percentage(test_data):
    """
    Calculate total energy loss percentage across all battery tests.
    
    Args:
        test_data: CSV string with format:
                  TestDay,TempC,CapacityKWh,OriginalCapacityKWh
    
    Returns:
        float: Total energy loss percentage (rounded to 1 decimal)
    """
    lines = test_data.strip().split('\n')
    
    total_loss = 0
    total_original = 0
    
    for line in lines:
        parts = line.split(',')
        current_capacity = float(parts[2])
        original_capacity = float(parts[3])
        
        loss = original_capacity - current_capacity
        total_loss += loss
        total_original += original_capacity
    
    loss_percentage = (total_loss / total_original) * 100
    return round(loss_percentage, 1)


if __name__ == "__main__":
    # Read battery test data
    with open("battery_test.csv", "r") as f:
        data = f.read()
    
    # Calculate loss percentage
    loss_pct = calculate_energy_loss_percentage(data)
    
    # Output result
    print(f"{loss_pct}")  # Expected: 12.3
