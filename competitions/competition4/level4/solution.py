def fibonacci(n):
    """Calculate the nth Fibonacci number (0-indexed)"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def count_golden_ratio_pairs(max_n):
    """Count pairs where F(n+1)/F(n) rounds to 1.618 (3 decimal places)"""
    count = 0
    
    for n in range(1, max_n):
        f_n = fibonacci(n)
        f_n_plus_1 = fibonacci(n + 1)
        
        if f_n > 0:  # Avoid division by zero
            ratio = f_n_plus_1 / f_n
            # Round to 3 decimal places
            rounded_ratio = round(ratio, 3)
            
            if rounded_ratio == 1.618:
                count += 1
                print(f"F({n+1})/F({n}) = {f_n_plus_1}/{f_n} = {ratio:.6f} → {rounded_ratio}")
    
    return count

if __name__ == "__main__":
    # Level 4: Count pairs from F(1) to F(50) where ratio rounds to 1.618
    result = count_golden_ratio_pairs(50)
    print(f"\nTotal pairs that round to 1.618: {result}")  # Expected: 42
