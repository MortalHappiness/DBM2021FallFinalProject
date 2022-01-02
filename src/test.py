import unittest
import random
import os
import shutil
import uuid
from main import external_merge_sort
from constants import PAGE_SIZE

DATA_FOLDER = "./data"


def split_nums(nums, k):
    i = 0
    strs = []
    while i < len(nums):
        strs.append(' '.join(map(str, nums[i:i + k])))
        i += k
    return strs


def write_to_txt_files(strs):
    for i, s in enumerate(strs):
        with open(os.path.join(DATA_FOLDER, uuid.uuid4().hex + ".txt"), "w") as fout:
            fout.write(s)


class TestExternalMergeSort(unittest.TestCase):
    def cleanUp(self):
        shutil.rmtree(DATA_FOLDER, ignore_errors=True)
        os.mkdir(DATA_FOLDER)

    def auto_test_util(self, memory_size, total_size):
        nums = [random.randint(1, total_size * 2) for i in range(total_size)]
        strs = split_nums(nums, PAGE_SIZE)
        write_to_txt_files(strs)
        nums.sort()
        sorted_strs = split_nums(nums, PAGE_SIZE)
        external_merge_sort(memory_size, data_folder=DATA_FOLDER)
        for i, s in enumerate(sorted_strs):
            with open(os.path.join(DATA_FOLDER, f"{i+1}.txt")) as fin:
                res = fin.read()
                self.assertEqual(
                    s, res, f"Unmatched result in '{i+1}.txt'. memory_size={memory_size}, total_size={total_size}")

    def test_different_memory_size_and_numbers(self):
        for memory_size in range(300, 900, 200):
            for total_size in [300, 5000, 10000]:
                with self.subTest(msg=f"subtest", memory_size=memory_size, total_size=total_size):
                    self.cleanUp()
                    self.auto_test_util(memory_size=memory_size, total_size=total_size)


if __name__ == "__main__":
    unittest.main()
