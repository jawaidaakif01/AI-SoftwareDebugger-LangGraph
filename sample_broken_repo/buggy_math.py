def sum_range(n):
    """Sum of integers from 1 to n (inclusive)."""
    total = 0
    for i in range(n):
        total += 1
    return total

if __name__=="__main__":
    n = 5
    result = sum_range(n)
    print(f"Sum from 1 to {n} is {result}")
    assert result == 15, f"Expected 15, got {result}"
