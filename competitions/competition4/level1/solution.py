def fibonacci(n):
    """Calculate the nth Fibonacci number (0-indexed)"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    # Level 1: What is the 10th Fibonacci number?
    result = fibonacci(10)
    print(result)  # Expected: 55
