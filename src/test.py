import unittest
import random
import os
import shutil
import uuid
from main import external_merge_sort
from constants import PAGE_SIZE

random.seed(0)
DATA_FOLDER = "./data"


def split_nums(nums, k):
    i = 0
    strs = []
    while i < len(nums):
        strs.append(' '.join(map(str, nums[i:i + k])))
        i += k
    return strs


def write_to_txt_files(strs, folder):
    for s in strs:
        with open(os.path.join(folder, uuid.uuid4().hex + ".txt"), "w") as fout:
            fout.write(s)


def reset_folder(folder):
    shutil.rmtree(folder, ignore_errors=True)
    os.mkdir(folder)


class TestExternalMergeSort(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reset_folder(DATA_FOLDER)

    def prepare_folder(self, memory_size, total_size):
        sub_folder = f"memory_{memory_size}_total_{total_size}"
        data_folder = os.path.join(DATA_FOLDER, sub_folder)
        reset_folder(data_folder)
        return data_folder

    def auto_test_util(self, memory_size, total_size):
        data_folder = self.prepare_folder(
            memory_size=memory_size, total_size=total_size)
        nums = [random.randint(1, total_size * 2) for _ in range(total_size)]
        strs = split_nums(nums, PAGE_SIZE)
        write_to_txt_files(strs, folder=data_folder)
        nums.sort()
        sorted_strs = split_nums(nums, PAGE_SIZE)
        external_merge_sort(memory_size, data_folder=data_folder)
        for i, s in enumerate(sorted_strs):
            with open(os.path.join(data_folder, f"{i+1}.txt")) as fin:
                res = fin.read()
                self.assertEqual(
                    s, res, f"Unmatched result in '{i+1}.txt'. {memory_size=}, {total_size=}")

    def test_different_memory_size_and_numbers(self):
        for memory_size in range(300, 1100, 100):
            for total_size in [300, 5000, 10000]:
                with self.subTest(msg=f"subtest", memory_size=memory_size, total_size=total_size):
                    self.auto_test_util(
                        memory_size=memory_size, total_size=total_size)


if __name__ == "__main__":
    unittest.main()
