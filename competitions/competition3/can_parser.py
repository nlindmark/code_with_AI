"""
CAN log parser utility for BUSMASTER format logs.
Parses ASCII CAN logs in BUSMASTER format and provides functions for analysis.
"""
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CANMessage:
    """Represents a single CAN message."""
    timestamp: str  # Format: HH:MM:SS:mmmm
    direction: str  # Tx or Rx
    channel: int
    can_id: str  # Hex format like "0xCF073E3"
    message_type: str  # x, xr, s, etc.
    dlc: int  # Data Length Code
    data: List[str]  # List of hex bytes as strings


def parse_busmaster_log(file_path: str) -> List[CANMessage]:
    """
    Parse a BUSMASTER format CAN log file.
    
    Format: HH:MM:SS:mmmm <Tx/Rx> <Channel> <CAN_ID> <Type> <DLC> <DataBytes...>
    Example: 11:38:07:5682 Rx 1 0xCF073E3 x 8 FE E3 4B 49 9A 01 00 00
    
    Args:
        file_path: Path to the CAN log file
        
    Returns:
        List of CANMessage objects
    """
    messages = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip header lines (start with ***) and empty lines
            if not line or line.startswith('***'):
                continue
            
            # Skip lines that don't start with timestamp (format: HH:MM:SS:mmmm)
            if not re.match(r'^\d{2}:\d{2}:\d{2}:\d+', line):
                continue
            
            # Parse the line
            parts = line.split()
            if len(parts) < 6:
                continue
            
            try:
                timestamp = parts[0]
                direction = parts[1]
                channel = int(parts[2])
                can_id = parts[3]
                message_type = parts[4]
                dlc = int(parts[5])
                
                # Extract data bytes (everything after DLC)
                data = parts[6:] if len(parts) > 6 else []
                
                # Ensure data matches DLC
                if len(data) > dlc:
                    data = data[:dlc]
                
                messages.append(CANMessage(
                    timestamp=timestamp,
                    direction=direction,
                    channel=channel,
                    can_id=can_id,
                    message_type=message_type,
                    dlc=dlc,
                    data=data
                ))
            except (ValueError, IndexError):
                # Skip malformed lines
                continue
    
    return messages


def count_unique_can_ids(messages: List[CANMessage]) -> int:
    """
    Count the number of unique CAN IDs in the log.
    
    Args:
        messages: List of CAN messages
        
    Returns:
        Number of unique CAN IDs
    """
    unique_ids = set(msg.can_id for msg in messages)
    return len(unique_ids)


def get_messages_by_id(messages: List[CANMessage], can_id: str) -> List[CANMessage]:
    """
    Get all messages with a specific CAN ID.
    
    Args:
        messages: List of CAN messages
        can_id: CAN ID to filter (e.g., "0xCF11000")
        
    Returns:
        List of messages with the specified CAN ID
    """
    return [msg for msg in messages if msg.can_id == can_id]


def find_first_message_with_pattern(
    messages: List[CANMessage],
    can_id: str,
    byte_index: int,
    byte_value: str
) -> Optional[CANMessage]:
    """
    Find the first message with a specific CAN ID where a specific byte equals a value.
    
    Args:
        messages: List of CAN messages
        can_id: CAN ID to search for
        byte_index: Index of byte to check (0-based)
        byte_value: Hex value to match (e.g., "7F" or "0x7F")
        
    Returns:
        First matching message or None
    """
    byte_value = byte_value.upper().replace('0X', '')
    
    for msg in messages:
        if msg.can_id == can_id and len(msg.data) > byte_index:
            if msg.data[byte_index].upper() == byte_value:
                return msg
    return None


def find_first_message_with_multi_byte_pattern(
    messages: List[CANMessage],
    can_id: str,
    byte_values: Dict[int, str]
) -> Optional[CANMessage]:
    """
    Find the first message matching multiple byte conditions.
    
    Args:
        messages: List of CAN messages
        can_id: CAN ID to search for
        byte_values: Dictionary mapping byte index to expected hex value
                    (e.g., {0: "7F", 1: "18"})
        
    Returns:
        First matching message or None
    """
    for msg in messages:
        if msg.can_id != can_id:
            continue
        
        # Check all byte conditions
        match = True
        for byte_index, expected_value in byte_values.items():
            expected_value = expected_value.upper().replace('0X', '')
            if len(msg.data) <= byte_index:
                match = False
                break
            if msg.data[byte_index].upper() != expected_value:
                match = False
                break
        
        if match:
            return msg
    
    return None


def extract_timestamp_hhmmss(timestamp: str) -> str:
    """
    Extract HH:MM:SS from full timestamp (HH:MM:SS:mmmm).
    
    Args:
        timestamp: Full timestamp string
        
    Returns:
        HH:MM:SS format timestamp
    """
    parts = timestamp.split(':')
    if len(parts) >= 3:
        return f"{parts[0]}:{parts[1]}:{parts[2]}"
    return timestamp


def find_first_uds_message(messages: List[CANMessage]) -> Optional[CANMessage]:
    """
    Find the first UDS diagnostic message (CAN IDs 0x7E0-0x7EF).
    
    Args:
        messages: List of CAN messages
        
    Returns:
        First UDS message or None
    """
    # UDS diagnostic IDs range from 0x7E0 to 0x7EF
    uds_ids = [f"0x7E{i:X}" for i in range(0x0, 0x10)]
    
    for msg in messages:
        if msg.can_id in uds_ids:
            return msg
    
    return None


def count_messages_by_pattern(
    messages: List[CANMessage],
    can_id: str,
    byte_index: int,
    byte_value: str
) -> int:
    """
    Count messages with a specific CAN ID where a specific byte equals a value.
    
    Args:
        messages: List of CAN messages
        can_id: CAN ID to search for
        byte_index: Index of byte to check (0-based)
        byte_value: Hex value to match
        
    Returns:
        Count of matching messages
    """
    byte_value = byte_value.upper().replace('0X', '')
    count = 0
    
    for msg in messages:
        if msg.can_id == can_id and len(msg.data) > byte_index:
            if msg.data[byte_index].upper() == byte_value:
                count += 1
    
    return count

