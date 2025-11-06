def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def find_twin_primes(start, end):
    """Find all twin prime pairs in the given range."""
    # Generate all primes in range
    primes = [n for n in range(start, end + 1) if is_prime(n)]
    
    # Count twin prime pairs
    twin_pairs = 0
    for i in range(len(primes) - 1):
        if primes[i + 1] - primes[i] == 2:
            twin_pairs += 1
    
    return twin_pairs

# Read range from file
with open('range.txt', 'r') as f:
    range_str = f.read().strip()
    start, end = map(int, range_str.split('-'))

# Find twin primes
result = find_twin_primes(start, end)
print(result)
