def linear_search(packages, boxes):

    if not packages or not boxes:
        return -1
    
    n = len(packages)
    m = len(boxes)
    
    min_waste = float('inf')
    
    # Iterate through each supplier - O(m)
    for supplier_idx in range(m):
        supplier_boxes = boxes[supplier_idx]
        total_waste = 0
        valid_supplier = True
        
        # For each package, find the best box from this supplier - O(n)
        for package_size in packages:
            min_box_waste = float('inf')
            found_box = False
            
            # Check each box type from this supplier - O(b)
            for box_size in supplier_boxes:
                # Box must be at least as large as the package
                if box_size >= package_size:
                    waste = box_size - package_size
                    if waste < min_box_waste:
                        min_box_waste = waste
                        found_box = True
            
            # If no box can fit this package, this supplier is invalid
            if not found_box:
                valid_supplier = False
                break
            
            total_waste += min_box_waste
        
        # Update best waste if this supplier is valid
        if valid_supplier:
            min_waste = min(min_waste, total_waste)
    
    # Return result
    return min_waste if min_waste != float('inf') else -1


# Test cases
if __name__ == "__main__":
    # Example 1
    packages1 = [2, 3, 5]
    boxes1 = [[4, 8], [2, 8]]
    result1 = linear_search(packages1, boxes1)
    print(f"Example 1:")
    print(f"Input: packages = {packages1}, boxes = {boxes1}")
    print(f"Output: {result1}")
    print(f"Expected: 6")
    print()
    
    # Example 2
    packages2 = [2, 3, 5]
    boxes2 = [[1, 4], [2, 3], [3, 4]]
    result2 = linear_search(packages2, boxes2)
    print(f"Example 2:")
    print(f"Input: packages = {packages2}, boxes = {boxes2}")
    print(f"Output: {result2}")
    print(f"Expected: -1")
    print()
    
    # Example 3
    packages3 = [3, 5, 8, 10, 11, 12]
    boxes3 = [[12], [11, 9], [10, 5, 14]]
    result3 = linear_search(packages3, boxes3)
    print(f"Example 3:")
    print(f"Input: packages = {packages3}, boxes = {boxes3}")
    print(f"Output: {result3}")
    print(f"Expected: 9")
    print()
    
    # Additional test case: Single package, single supplier
    packages4 = [5]
    boxes4 = [[10]]
    result4 = linear_search(packages4, boxes4)
    print(f"Test 4:")
    print(f"Input: packages = {packages4}, boxes = {boxes4}")
    print(f"Output: {result4}")
    print(f"Expected: 5")
    print()
    
    # Additional test case: Multiple packages, optimal choice
    packages5 = [1, 2, 3, 4, 5]
    boxes5 = [[5, 10], [1, 2, 3, 4, 5]]
    result5 = linear_search(packages5, boxes5)
    print(f"Test 5:")
    print(f"Input: packages = {packages5}, boxes = {boxes5}")
    print(f"Output: {result5}")
    print(f"Expected: 0 (perfect fit with supplier 1)")