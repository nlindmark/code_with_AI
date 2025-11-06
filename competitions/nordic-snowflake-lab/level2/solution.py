def is_symmetric(snowflake):
    """Check if all arms of the snowflake are identical."""
    return len(set(snowflake)) == 1

# Read all snowflake patterns
with open('storm_data.txt', 'r') as f:
    snowflakes = [line.strip() for line in f if line.strip()]

# Count symmetric snowflakes
symmetric_count = sum(1 for flake in snowflakes if is_symmetric(flake))
print(symmetric_count)
