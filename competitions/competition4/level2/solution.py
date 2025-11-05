def fibonacci(n):
    """Calculate the nth Fibonacci number (0-indexed)"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def sum_even_fibonacci(max_n):
    """Sum all even Fibonacci numbers up to F(max_n)"""
    total = 0
    for i in range(max_n + 1):
        fib = fibonacci(i)
        if fib % 2 == 0:
            total += fib
    return total

if __name__ == "__main__":
    # Level 2: Sum of even Fibonacci numbers up to F(20)
    result = sum_even_fibonacci(20)
    print(result)  # Expected: 3382
