from enum import unique, Enum
import click
import os
import urllib.request
from shutil import which
import subprocess
from common import Utils as Commons


@unique
class ArchAvailable(Enum):
    single_node = 0
    master_slave = 1


# TODO - Populate that object with remote data
class PlaybookUrls:
    sources = {
        "single_node":
            "https://raw.githubusercontent.com/jarpsimoes/tools-automator/main/playbooks/mysql-57-single-node/playbook_server.yaml",
        "master_slave":
            "https://github.com/jarpsimoes/ansible-configure-http-server/blob/main/playbooks/config_vm_rollback.yaml"
    }


@click.command()
@click.option('-a', '--arch', 'arch', required=True, help='Single node arch or Master slave arch',
              type=click.Choice(ArchAvailable.__members__), prompt=True)
@click.option('-t', '--target', 'target', default='./.tmp_gen', help='Define target')
@click.option('-h', '--database-host', 'database_host', required=True, prompt=True, help='Database server host')
@click.option('-u', '--ssh-user', 'user_ssh', help='Set remote user for ssh connection', default=None)
@click.option('-rdb', '--root-database-password', 'root_database_password', required=True,
              help="Set MySQL root password", prompt=True, hide_input=True, confirmation_prompt=True)
def create_mysql(arch: str, target: str, database_host: str, user_ssh: str, root_database_password: str):
    if Commons.Utils.check_ansible_exist():
        click.echo("ERROR: Ansible not found")
        exit(1)

    click.echo(f'Architecture Type: {arch}')

    target_folder_name = Commons.Utils.create_working_path(target)

    click.echo(f'Target folder: {target_folder_name}')

    Commons.Utils.get_playbook_from_git(str(PlaybookUrls().sources[arch]),
                                        f'{target_folder_name}/{arch}.yaml')

    Commons.Utils.create_ini_file(user_ssh, database_host, f'{target_folder_name}/inventory.ini')

    click.echo("Progress...")
    #playbook = subprocess.Popen([
    #    "ansible-playbook",
    #    f'{target_folder_name}/single_node.yaml', "-i",
    #    f'{target_folder_name}/inventory.ini',
    #    "--extra-vars",
    #    f'mysql_password={root_database_password}'],
    #    stdout=subprocess.PIPE,
    #    stderr=subprocess.STDOUT)

    #if playbook.returncode and playbook.returncode != 0:
    #    click.echo(f'ERROR: {playbook.communicate()[0]}')
    #    exit(1)


