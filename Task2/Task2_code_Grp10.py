def heapify(arr, n, i):
    """
    It looks like something like this:
    Index:   0    1   2   3  4  5

                 [13]          <- index 0 (root, always MAX)
                /    \
            [11]      [12]     <- index 1, 2
            /  \      /
          [5]  [6]  [7]        <- index 3, 4, 5

    Parameters:
        arr: The array to process
        n:   Size of the heap (effective length of the array)
        i:   Index of the root node to heapify
    """
    largest = i          # Initialize largest as root
    left = 2 * i + 1     # Left child index
    right = 2 * i + 2    # Right child index

    # If left child exists and is greater than current largest
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If right child exists and is greater than current largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not the root, swap and recursively adjust the affected subtree
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  
        heapify(arr, n, largest)                     


def heap_sort(arr):
    """
    Main heap sort function.
    """
    n = len(arr)

    # 1. Build Max Heap
    # Start from the last non-leaf node and heapify bottom-up
    # Index of the last non-leaf node is n//2 - 1
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 2. Extract elements one by one for sorting
    # Swap the heap top (max element) with the last element of the current heap,
    # then shrink the heap range and re-heapify
    for i in range(n - 1, 0, -1):
        # Swap heap top with the last element of the heap
        arr[0], arr[i] = arr[i], arr[0]

        # Heapify the reduced heap (size i) with root at index 0
        heapify(arr, i, 0)

    return arr


# =================== Test Example ===================
if __name__ == "__main__":
    test_array = [12, 11, 13, 5, 6, 7]
    print("Original array:", test_array)
    
    heap_sort(test_array)
    print("Sorted array:", test_array)
    
    # Additional test: random array
    import random
    random_array = [random.randint(1, 100) for _ in range(10)]
    print("\nRandom array:", random_array)
    heap_sort(random_array)
    print("Sorted:", random_array)
