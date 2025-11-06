#!/usr/bin/env python3
"""
CAN Bus Signal Decoder - Reference Solution

This solution demonstrates how to parse a CAN message and extract
the vehicle speed from bytes 3-4 (big-endian format).
"""

def decode_can_speed(can_message):
    """
    Decode vehicle speed from CAN message.
    
    Args:
        can_message: String containing CAN message in format:
                    "ID: 0x123  Data: 01 A2 22 36 FF 00 B4 C8"
    
    Returns:
        float: Vehicle speed in km/h
    """
    # Extract data bytes (everything after "Data: ")
    data_part = can_message.split("Data:")[1].strip()
    
    # Split into individual bytes
    bytes_hex = data_part.split()
    
    # Extract bytes 3-4 (0-indexed: bytes[2] and bytes[3])
    byte3 = int(bytes_hex[2], 16)  # 0x22 = 34
    byte4 = int(bytes_hex[3], 16)  # 0x36 = 54
    
    # Combine as big-endian 16-bit value
    raw_value = (byte3 << 8) | byte4  # (34 * 256) + 54 = 8750
    
    # Apply scaling factor: 0.01 km/h per unit
    speed_kmh = raw_value * 0.01
    
    return speed_kmh


if __name__ == "__main__":
    # Read CAN message from file
    with open("can_message.txt", "r") as f:
        can_msg = f.read().strip()
    
    # Decode speed
    speed = decode_can_speed(can_msg)
    
    # Output result
    print(f"{speed}")  # Expected: 87.5
