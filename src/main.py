import glob
from typing import List

PAGE_SIZE = 2


def _partition(arr, low, high):
    i = (low-1)
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)


def qsort(arr, low, high):
    """
    Quicksort arr from index low to index high inclusive.

    Reference: https://www.geeksforgeeks.org/python-program-for-quicksort/
    """
    if len(arr) == 1:
        return arr
    if low < high:
        pi = _partition(arr, low, high)
        qsort(arr, low, pi-1)
        qsort(arr, pi+1, high)


def read_page(filename: str, memory: List[int], idx: int):
    """
    Read page into memory address idx.

    Arguments:
        filename: The input filename.
        memory: The memory.
        idx: The memory address to put the page.
    """
    with open(filename) as fin:
        for i, num in enumerate(map(int, fin.read().split())):
            memory[idx + i] = num


def write_page(filename: str, memory: List[int], idx: int):
    """
    Read page content at memory address idx into filename.

    Arguments:
        filename: The output filename.
        memory: The memory.
        idx: The memory address of the page to be written.
    """
    with open(filename, "w") as fout:
        fout.write(" ".join([str(num) for num in memory[idx:idx+PAGE_SIZE]]))


def merge(memory: List[int], k: int, start: int, end: int, run_len: int):
    """
    k-way merge.

    Merge pages p with start <= p < end, p = 0, 1, 2...
    Page p comes from f"{p+1}.txt"
    run_len is the number of pages in a sorted run.
    """
    assert len(memory) == (k + 1) * PAGE_SIZE
    out_idx = start + 1
    print(k, start, end, run_len)


def main():
    n = int(input("n = "))
    memory = [0] * n
    B = n // PAGE_SIZE

    # Phase 1: sorting
    i = 0
    out_idx = 1
    for filename in sorted(glob.glob("*.txt")):
        read_page(filename, memory, i * PAGE_SIZE)
        if i + 1 == B:
            memory.sort()
            for idx in range(0, len(memory), PAGE_SIZE):
                write_page(f"{out_idx}.txt", memory, idx)
                out_idx += 1
            i = 0
        else:
            i += 1
    if i != 0:
        qsort(memory, 0, i * PAGE_SIZE - 1)
        for idx in range(0, i * PAGE_SIZE, PAGE_SIZE):
            write_page(f"{out_idx}.txt", memory, idx)
            out_idx += 1

    # Phase 2: merging
    num_pages = out_idx - 1
    out_idx = 0
    run_len = B
    k = B - 1
    while run_len < num_pages:
        for i in range(0, num_pages, k * run_len):
            merge(memory, k, i, min(i + k * run_len, num_pages), run_len)
        run_len <<= 1


if __name__ == "__main__":
    main()
