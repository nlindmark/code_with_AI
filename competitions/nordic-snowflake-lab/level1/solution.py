def is_symmetric(snowflake):
    """Check if all arms of the snowflake are identical."""
    return len(set(snowflake)) == 1

# Read the snowflake pattern
with open('snowflake.txt', 'r') as f:
    pattern = f.read().strip()

# Check symmetry
result = "yes" if is_symmetric(pattern) else "no"
print(result)
