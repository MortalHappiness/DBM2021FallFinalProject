import unittest
import random
import os
import shutil
import uuid
from main import external_merge_sort

DATA_FOLDER = "data"
NumbersInAFile = 100
memory_sizes = list(range(300, 1100, 100))


def split_nums(nums, k):
    i = 0
    strs = []
    while i < len(nums):
        strs.append(' '.join(map(str, nums[i:i + k])))
        i += k
    return strs


def write_to_txt_files(strs):
    for s in strs:
        with open(os.path.join(DATA_FOLDER, uuid.uuid4().hex + ".txt"), "w") as fout:
            fout.write(s)


class TestExternalMergeSort(unittest.TestCase):
    def setUp(self):
        shutil.rmtree(DATA_FOLDER)
        os.mkdir(DATA_FOLDER)

    def test_300_memory_size_500_numbers(self):
        n = 300
        nums = [random.randint(1, 500 * 2) for i in range(500)]
        strs = split_nums(nums, NumbersInAFile)
        write_to_txt_files(strs)
        nums.sort()
        sorted_strs = split_nums(nums, NumbersInAFile)
        external_merge_sort(n, data_folder=DATA_FOLDER)
        for i, s in enumerate(sorted_strs):
            with open(os.path.join(DATA_FOLDER, f"{i+1}.txt")) as fin:
                res = fin.read()
                self.assertEqual(
                    s, res, f"Unmatched result in '{i+1}.txt'")


if __name__ == "__main__":
    unittest.main()
