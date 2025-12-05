# Problem 3

def count_min_sketch(a, b, w, p, stream):

    # Get d (depth) from length of a or b
    d = len(a)
    
    # Initialize sketch matrix with zeros
    sketch = [[0 for _ in range(w)] for _ in range(d)]
    
    # Define hash functions: h_i(x) = ((a_i * x + b_i) mod p) mod w
    def hash_func(x, i):
        return ((a[i] * x + b[i]) % p) % w
    
    # Process the stream
    for x in stream:
        # For each hash function (each row)
        for i in range(d):
            # Compute hash and increment the corresponding cell
            col = hash_func(x, i)
            sketch[i][col] += 1
    
    return sketch


# Test with the provided example
def test_example():
    # Example parameters
    a = [1, 2]
    b = [3, 5]
    w = 3
    p = 100
    
    # Create stream generator
    def stream_gen():
        for x in [10, 11, 10]:
            yield x
    
    # Run count_min_sketch
    result = count_min_sketch(a, b, w, p, stream_gen())
    
    print("Result sketch matrix:")
    for i, row in enumerate(result):
        print(f"Row {i}: {row}")
    
    print("\nExpected: [[0, 2, 1], [1, 2, 0]]")
    print(f"Match: {result == [[0, 2, 1], [1, 2, 0]]}")
    
    # Verify hash computations
    print("\nHash function verification:")
    for x in [10, 11, 10]:
        h1 = ((1 * x + 3) % 100) % 3
        h2 = ((2 * x + 5) % 100) % 3
        print(f"x={x}: h1(x)={h1}, h2(x)={h2}")


if __name__ == "__main__":
    test_example()