def prime_factorization(n):
    """Find all prime factors of n (with repetition)."""
    factors = []
    
    # Check for 2s
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check odd numbers starting from 3
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    
    # If n is still greater than 1, it's a prime factor
    if n > 1:
        factors.append(n)
    
    return factors

# Read number from file
with open('composite.txt', 'r') as f:
    number = int(f.read().strip())

# Get prime factors and sum them
factors = prime_factorization(number)
result = sum(factors)
print(result)
