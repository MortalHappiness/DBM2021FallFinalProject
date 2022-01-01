import glob
from typing import List, IO
import tempfile
import shutil

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


def read_page(fp: IO, memory: List[int], idx: int):
    """
    Read page into memory address idx.

    Arguments:
        fp: The input file.
        memory: The memory.
        idx: The memory address to put the page.
    """
    fp.seek(0)
    for i, num in enumerate(map(int, fp.read().split())):
        memory[idx + i] = num


def write_page(fp: IO, memory: List[int], idx: int):
    """
    Read page content at memory address idx into filename.

    Arguments:
        fp: The output file.
        memory: The memory.
        idx: The memory address of the page to be written.
    """
    fp.seek(0)
    fp.write(" ".join([str(num) for num in memory[idx:idx+PAGE_SIZE]]))


def merge(memory: List[int],
          k: int,
          run_len: int,
          input_pages: List[IO],
          output_pages: List[IO]):
    """
    k-way merge.

    Merge pages, run_len is the number of pages in a sorted run.
    Read from input_pages and write to output_pages.
    """
    assert len(memory) == (k + 1) * PAGE_SIZE
    assert len(input_pages) == len(output_pages)

    # TODO: Replace the following with k-way merge implementation
    L = [0] * (len(input_pages) * PAGE_SIZE)
    for i, page in enumerate(input_pages):
        read_page(page, L, i * PAGE_SIZE)
    L.sort()
    for i in range(len(output_pages)):
        write_page(output_pages[i], L, i * PAGE_SIZE)


def main():
    n = int(input("n = "))
    memory = [0] * n
    B = n // PAGE_SIZE

    # Phase 1: sorting
    i = 0
    tempfiles = list()
    for filename in sorted(glob.glob("*.txt")):
        with open(filename) as fin:
            read_page(fin, memory, i * PAGE_SIZE)
        if i + 1 == B:
            memory.sort()
            for idx in range(0, len(memory), PAGE_SIZE):
                fp = tempfile.TemporaryFile("w+")
                write_page(fp, memory, idx)
                tempfiles.append(fp)
            i = 0
        else:
            i += 1
    if i != 0:
        qsort(memory, 0, i * PAGE_SIZE - 1)
        for idx in range(0, i * PAGE_SIZE, PAGE_SIZE):
            fp = tempfile.TemporaryFile("w+")
            write_page(fp, memory, idx)
            tempfiles.append(fp)

    # Phase 2: merging
    num_pages = len(tempfiles)
    run_len = B
    k = B - 1
    while run_len < num_pages:
        for i in range(0, num_pages, k * run_len):
            start = i
            end = min(i + k * run_len, num_pages)
            pages = tempfiles[start:end]
            out_pages = [tempfile.TemporaryFile("w+")
                         for _ in range(len(pages))]
            merge(memory, k, run_len, pages, out_pages)
            for j in range(start, end):
                tempfiles[j].close()
                tempfiles[j] = out_pages[j - start]
        run_len <<= 1

    # Output and Close temporary files
    for i, fp in enumerate(tempfiles):
        fp.seek(0)
        with open(f"{i+1}.txt", "w") as fout:
            shutil.copyfileobj(fp, fout)
        fp.close()


if __name__ == "__main__":
    main()
