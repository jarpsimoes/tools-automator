import unittest
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from click.testing import CliRunner
from mysql import create_mysql
from mysql import AnsibleHelper
import os
import shutil


class MySQLTest(TestCase):

    runner: CliRunner = None
    output_dir: str = "test"

    @staticmethod
    def mock_ansible():
        ansible_helper = AnsibleHelper
        ansible_helper.run_playbook = MagicMock()

    def get_runner(self):
        if not self.runner:
            self.runner = CliRunner()
        return self.runner

    def test_all_mandatory_args(self):

        if os.path.isdir(self.output_dir):
            shutil.rmtree(self.output_dir)

        self.mock_ansible()

        result = self.get_runner().invoke(create_mysql, [
            "--arch", "SINGLE_NODE",
            "--version", "57",
            "--database-host", "1.1.1.1",
            "--ssh-user", "test",
            "--root-database-password", "example",
            "--target", self.output_dir
        ])

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.isdir(self.output_dir))
        self.assertTrue(os.path.isfile(f'{self.output_dir}/SINGLE_NODE.yaml'))
        self.assertTrue(os.path.isfile(f'{self.output_dir}/inventory.ini'))

        shutil.rmtree(self.output_dir)


if __name__ == '__main__':
    unittest.main()
