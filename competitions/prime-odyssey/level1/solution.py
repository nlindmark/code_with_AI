def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Read the number from file
with open('number.txt', 'r') as f:
    number = int(f.read().strip())

# Check if prime
result = "yes" if is_prime(number) else "no"
print(result)
