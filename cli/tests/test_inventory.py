import unittest
from common.InventoryHelper import InventoryHelper


class InventoryHelperTest(unittest.TestCase):
    def test_add_group(self):

        inventory_helper = InventoryHelper()

        inventory_helper.add_group("all:test", ["test1", "test2", "test3"])

        self.assertEqual(len(inventory_helper.lines), 4)

        self.assertEqual(inventory_helper.lines.__getitem__(0), "[all:test]")


if __name__ == '__main__':
    unittest.main()
