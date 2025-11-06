#!/usr/bin/env python3
"""
ADAS Collision Risk Calculator - Reference Solution

Calculate time-to-collision for ADAS system.
"""

def calculate_ttc(vehicle_speed, obstacle_distance, obstacle_speed):
    """
    Calculate time-to-collision.
    
    Args:
        vehicle_speed: Speed of your vehicle (m/s)
        obstacle_distance: Distance to obstacle (m)
        obstacle_speed: Speed of obstacle in same direction (m/s)
    
    Returns:
        float: Time-to-collision in seconds (rounded to 1 decimal)
    """
    relative_speed = vehicle_speed - obstacle_speed
    
    if relative_speed <= 0:
        # Not catching up or obstacle is faster
        return float('inf')
    
    ttc = obstacle_distance / relative_speed
    return round(ttc, 1)


if __name__ == "__main__":
    # Given parameters
    vehicle_speed = 25  # m/s
    obstacle_distance = 75  # meters
    obstacle_speed = 10  # m/s
    
    # Calculate TTC
    ttc = calculate_ttc(vehicle_speed, obstacle_distance, obstacle_speed)
    
    # Output result
    print(f"{ttc}")  # Expected: 5.0
