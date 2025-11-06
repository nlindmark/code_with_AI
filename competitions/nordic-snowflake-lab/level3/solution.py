from collections import Counter

def calculate_complexity(snowflake):
    """Calculate complexity score of a snowflake."""
    # Count unique character types
    unique_types = len(set(snowflake))
    
    # Get frequency of most common character
    char_counts = Counter(snowflake)
    max_frequency = max(char_counts.values())
    
    # Complexity = unique_types × length / max_frequency (rounded down)
    score = int((unique_types * len(snowflake)) / max_frequency)
    
    return score

# Read the snowflake pattern
with open('sample.txt', 'r') as f:
    pattern = f.read().strip()

# Calculate complexity score
score = calculate_complexity(pattern)
print(score)
