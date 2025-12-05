def binary_search(packages, boxes):

    if not packages or not boxes:
        return -1
    
    import bisect
    
    n = len(packages)
    m = len(boxes)
    
    # Sort packages once: O(n log n)
    sorted_packages = sorted(packages)
    
    min_waste = float('inf')
    
    # Iterate through each supplier: O(m)
    for supplier_idx in range(m):
        supplier_boxes = boxes[supplier_idx]
        
        # Sort boxes for this supplier: O(b log b)
        sorted_boxes = sorted(supplier_boxes)
        
        # Track which packages have been assigned to boxes
        package_to_box = [None] * n
        
        # For each box type: O(b)
        for box_size in sorted_boxes:
            # Binary search to find packages that can fit in this box: O(log n)
            # bisect_right returns the insertion point (number of elements <= box_size)
            insert_pos = bisect.bisect_right(sorted_packages, box_size)
            
            # Assign unassigned packages to this box (greedy: smallest box that fits)
            for pkg_idx in range(insert_pos):
                if package_to_box[pkg_idx] is None:
                    package_to_box[pkg_idx] = box_size
        
        # Check if all packages are assigned
        if all(box is not None for box in package_to_box):
            # Calculate total waste for this supplier
            total_waste = sum(package_to_box[i] - sorted_packages[i] 
                            for i in range(n))
            
            min_waste = min(min_waste, total_waste)
    
    # Return result
    return min_waste if min_waste != float('inf') else -1


# Test cases
if __name__ == "__main__":
    # Example 1
    packages1 = [2, 3, 5]
    boxes1 = [[4, 8], [2, 8]]
    result1 = binary_search(packages1, boxes1)
    print(f"Example 1:")
    print(f"Input: packages = {packages1}, boxes = {boxes1}")
    print(f"Output: {result1}")
    print(f"Expected: 6")
    print(f"Explanation: Optimal supplier is 0 (first supplier)")
    print(f"  - Package 2 -> Box 4, waste = 2")
    print(f"  - Package 3 -> Box 4, waste = 1")
    print(f"  - Package 5 -> Box 8, waste = 3")
    print(f"  - Total waste = 6")
    print()
    
    # Example 2
    packages2 = [2, 3, 5]
    boxes2 = [[1, 4], [2, 3], [3, 4]]
    result2 = binary_search(packages2, boxes2)
    print(f"Example 2:")
    print(f"Input: packages = {packages2}, boxes = {boxes2}")
    print(f"Output: {result2}")
    print(f"Expected: -1")
    print(f"Explanation: No supplier has a box that can fit package of size 5")
    print()
    
    # Example 3
    packages3 = [3, 5, 8, 10, 11, 12]
    boxes3 = [[12], [11, 9], [10, 5, 14]]
    result3 = binary_search(packages3, boxes3)
    print(f"Example 3:")
    print(f"Input: packages = {packages3}, boxes = {boxes3}")
    print(f"Output: {result3}")
    print(f"Expected: 9")
    print(f"Explanation: Optimal supplier is 2 (third supplier)")
    print(f"  - Package 3 -> Box 5, waste = 2")
    print(f"  - Package 5 -> Box 5, waste = 0")
    print(f"  - Package 8 -> Box 10, waste = 2")
    print(f"  - Package 10 -> Box 10, waste = 0")
    print(f"  - Package 11 -> Box 14, waste = 3")
    print(f"  - Package 12 -> Box 14, waste = 2")
    print(f"  - Total waste = 9")
    print()
    
    # Additional test case: Perfect fit
    packages4 = [1, 2, 3, 4, 5]
    boxes4 = [[5, 10], [1, 2, 3, 4, 5]]
    result4 = binary_search(packages4, boxes4)
    print(f"Test 4:")
    print(f"Input: packages = {packages4}, boxes = {boxes4}")
    print(f"Output: {result4}")
    print(f"Expected: 0 (perfect fit with supplier 1)")
    print()
    
    # Additional test case: Single package
    packages5 = [5]
    boxes5 = [[10]]
    result5 = binary_search(packages5, boxes5)
    print(f"Test 5:")
    print(f"Input: packages = {packages5}, boxes = {boxes5}")
    print(f"Output: {result5}")
    print(f"Expected: 5")
    print()
    
    # Performance test with larger input
    packages6 = list(range(1, 101))  # 100 packages: [1, 2, ..., 100]
    boxes6 = [list(range(50, 151)), list(range(1, 102))]
    result6 = binary_search(packages6, boxes6)
    print(f"Test 6 (Performance):")
    print(f"Input: 100 packages [1..100], 2 suppliers")
    print(f"Output: {result6}")
    print(f"Expected: 0 or minimal waste")