from shutil import which
import os
from urllib import request
import click
from common.InventoryHelper import InventoryHelper


class Utils:

    @staticmethod
    def create_working_path(target: str) -> str:
        target_folder_name = target
        iterate = 0
        if os.path.isdir(target_folder_name):
            target_folder_name = f'{target_folder_name}_{iterate}'

            while os.path.isdir(target_folder_name):
                target_folder_name = f'{target}_{iterate}'
                iterate += 1
        os.mkdir(target_folder_name)
        return target_folder_name

    @staticmethod
    def get_playbook_from_git(url: str, output_file: str) -> str:
        base_yaml: request = request.urlopen(url)

        if base_yaml.getcode() != 200:
            click.echo(f'Request failed. Check your internet connection and repeat [{url}]')
            exit(1)

        playbook_file = open(output_file, "w")
        playbook_file.write(base_yaml.read().decode("utf-8"))
        playbook_file.close()

        return output_file

    @staticmethod
    def create_ini_file(user_ssh: str, database_host: str, root_database_password: str, output_file: str):
        inventory = InventoryHelper()

        if user_ssh and user_ssh != "":
            pb_vars = [
                'ansible_connection=ssh',
                f'ansible_ssh_user={user_ssh}',
                f'mysql_password={root_database_password}'
            ]
        else:
            pb_vars = [
                f'mysql_password={root_database_password}'
            ]
        inventory.add_group("all:vars", pb_vars)

        inventory.add_group("database", [
            f'{database_host}'
        ])

        inventory.generate_inventory_file(output_file)
