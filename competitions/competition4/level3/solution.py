def fibonacci(n):
    """Calculate the nth Fibonacci number (0-indexed)"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def sum_fibonacci_at_indices(indices):
    """Sum Fibonacci numbers at given indices"""
    total = 0
    for index in indices:
        total += fibonacci(index)
    return total

if __name__ == "__main__":
    # Level 3: Sum F(15) + F(25) + F(30) + F(12) + F(18)
    indices = [15, 25, 30, 12, 18]
    
    # Show individual values for verification
    for i in indices:
        print(f"F({i}) = {fibonacci(i)}")
    
    result = sum_fibonacci_at_indices(indices)
    print(f"\nSum: {result}")  # Expected: 848288
