import unittest
import random
import os
import shutil
import uuid
from main import qsort, external_merge_sort, phase1_sorting
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
    filenames = [uuid.uuid4().hex + ".txt" for _ in range(len(strs))]
    filenames.sort()
    for s, filename in zip(strs, filenames):
        with open(os.path.join(folder, filename), "w") as fout:
            fout.write(s)


def reset_folder(folder):
    shutil.rmtree(folder, ignore_errors=True)
    os.mkdir(folder)


class TestBase(unittest.TestCase):
    data_folder = ""

    @classmethod
    def setUpClass(cls):
        if not cls.data_folder:
            raise ValueError("data_folder must not be empty string")
        reset_folder(cls.data_folder)

    def prepare_folder(self, memory_size, total_size):
        sub_folder = f"memory_{memory_size}_total_{total_size}"
        data_folder = os.path.join(type(self).data_folder, sub_folder)
        reset_folder(data_folder)
        return data_folder

    def prepare_input(self, memory_size, total_size):
        data_folder = self.prepare_folder(
            memory_size=memory_size, total_size=total_size)
        nums = [random.randint(1, total_size * 2) for _ in range(total_size)]
        strs = split_nums(nums, PAGE_SIZE)
        write_to_txt_files(strs, folder=data_folder)
        return data_folder, nums

    def run_single_test(self, memory_size, total_size):
        raise NotImplementedError

    def run_testcase_matrix(self):
        for memory_size in range(300, 1100, 100):
            for total_size in [300, 5000, 10000]:
                with self.subTest(msg=f"subtest", memory_size=memory_size, total_size=total_size):
                    self.run_single_test(
                        memory_size=memory_size, total_size=total_size)


class TestPhase1(TestBase):
    data_folder = os.path.join(DATA_FOLDER, "phase1")

    def run_single_test(self, memory_size, total_size):
        random.seed(0)
        data_folder, nums = self.prepare_input(
            memory_size=memory_size, total_size=total_size)

        for i in range(0, total_size, memory_size):
            qsort(nums, i, min(i + memory_size, total_size) - 1)
        expected_strs = split_nums(nums, PAGE_SIZE)

        memory = [0] * memory_size
        tempfiles = phase1_sorting(memory, data_folder=data_folder)
        actual_strs = list()
        for fp in tempfiles:
            fp.seek(0)
            actual_strs.append(fp.read())
            fp.close()

        self.assertEqual(len(expected_strs), len(actual_strs))
        for expected, actual in zip(expected_strs, actual_strs):
            self.assertEqual(expected, actual)

    def test_different_memory_size_and_numbers(self):
        self.run_testcase_matrix()


class TestExternalMergeSort(TestBase):
    data_folder = os.path.join(DATA_FOLDER, "integration")

    def run_single_test(self, memory_size, total_size):
        data_folder, nums = self.prepare_input(
            memory_size=memory_size, total_size=total_size)
        nums.sort()
        sorted_strs = split_nums(nums, PAGE_SIZE)
        external_merge_sort(memory_size, data_folder=data_folder)
        for i, s in enumerate(sorted_strs):
            with open(os.path.join(data_folder, f"{i+1}.txt")) as fin:
                res = fin.read()
                self.assertEqual(
                    s, res, f"Unmatched result in '{i+1}.txt'. {memory_size=}, {total_size=}")

    def test_different_memory_size_and_numbers(self):
        self.run_testcase_matrix()


if __name__ == "__main__":
    reset_folder(DATA_FOLDER)
    unittest.main()
