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

# Read numbers from file
with open('numbers.txt', 'r') as f:
    numbers = [int(line.strip()) for line in f if line.strip()]

# Count primes
prime_count = sum(1 for num in numbers if is_prime(num))
print(prime_count)
