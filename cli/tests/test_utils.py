import unittest
from common.Utils import Utils
import os
import mysql


class UtilsTest(unittest.TestCase):
    test_folder: str = "test_folder"
    playbook_file: str = "playbook_test.yaml"
    ini_file: str = "inventory.ini"

    def test_create_working_path(self):

        if os.path.isdir(self.test_folder):
            os.removedirs(self.test_folder)

        if os.path.isdir(f'{self.test_folder}_0'):
            os.removedirs(f'{self.test_folder}_0')

        Utils.create_working_path(self.test_folder)

        self.assertTrue(os.path.isdir(self.test_folder))
        Utils.create_working_path(self.test_folder)

        self.assertTrue(os.path.isdir(f'{self.test_folder}_0'))

        os.removedirs(self.test_folder)
        os.removedirs(f'{self.test_folder}_0')

    def test_get_playbook_from_git(self):
        if os.path.isfile(self.playbook_file):
            os.remove(self.playbook_file)

        Utils.get_playbook_from_git(str(mysql.sources['single_node']), self.playbook_file)

        self.assertTrue(os.path.isfile(self.playbook_file))
        os.remove(self.playbook_file)

        Utils.get_playbook_from_git(str(mysql.sources['master_slave']), self.playbook_file)

        self.assertTrue(os.path.isfile(self.playbook_file))
        os.remove(self.playbook_file)

    def test_create_ini_file(self):
        if os.path.isfile(self.ini_file):
            os.remove(self.ini_file)

        Utils.create_ini_file(user_ssh="", database_host="1.1.1.1", root_database_password="test", output_file=self.ini_file)
        self.assertTrue(os.path.isfile(self.ini_file))
        os.remove(self.ini_file)

        Utils.create_ini_file(user_ssh="aaa", database_host="1.1.1.1", root_database_password="test", output_file=self.ini_file)
        self.assertTrue(os.path.isfile(self.ini_file))
        os.remove(self.ini_file)


if __name__ == '__main__':
    unittest.main()
