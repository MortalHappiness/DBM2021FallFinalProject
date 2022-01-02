import unittest
import random
import pathlib
from config import PAGE_SIZE, DATA_FOLDER
from main import solve

# ensure data folder exists
pathlib.Path(DATA_FOLDER).mkdir(exist_ok=True)


def split_nums(nums, k):
    i = 0
    strs = []
    while i < len(nums):
        strs.append(' '.join(map(str, nums[i:i + k])))
        i += k
    return strs


def write_to_txt_files(strs):
    for index, s in enumerate(strs):
        with open(f"{DATA_FOLDER}/{index}.txt", "w") as f:
            f.write(s)


class TestExternalMergeSort(unittest.TestCase):
    def setUp(self):
        # default constants
        self.TestSize = 1000
        self.NumbersInAFile = PAGE_SIZE

    def test_main(self):
        n = self.TestSize
        nums = [random.randint(1, n * 2) for i in range(n)]
        strs = split_nums(nums, self.NumbersInAFile)
        write_to_txt_files(strs)
        # print("value:", nums)
        nums.sort()
        # print("sort :", nums)
        sorted_strs = split_nums(nums, self.NumbersInAFile)

        solve(self.TestSize)

        for index, s in enumerate(sorted_strs):
            with open(f"{DATA_FOLDER}/{index}.txt", "r") as f:
                res = f.read()
                self.assertEqual(s, res, f"Unmatched result in '{index}.txt'")


if __name__ == "__main__":
    unittest.main()
