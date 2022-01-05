import sys
from enum import unique, Enum
import click
from common import Utils as Commons
from common.AnsibleHelper import AnsibleHelper


@unique
class ArchAvailable(Enum):
    SINGLE_NODE = "https://raw.githubusercontent.com/jarpsimoes/" \
                  "tools-automator/main/playbooks/mysql-57-single-node/playbook_server.yaml",
    MASTER_SLAVE = "https://raw.gitdddhubusercontent.com/jarpsimoes/" \
                   "tools-automator/main/playbooks/mysql-57-single-node/playbook_server.yaml",


sources = {
    "SINGLE_NODE_57":
        "https://raw.githubusercontent.com/jarpsimoes/"
        "tools-automator/main/playbooks/mysql-57-single-node/playbook_server.yaml",
    "MASTER_SLAVE_57":
        "https://raw.githubusercontent.com/jarpsimoes/"
        "tools-automator/main/playbooks/mysql-57-single-node/playbook_server.yaml",
    "SINGLE_NODE_8":
        "https://raw.githubusercontent.com/jarpsimoes/"
        "tools-automator/main/add_mysql_8/playbooks/mysql-8-single-node/playbook_server.yaml",
    "MASTER_SLAVE_8":
        "https://raw.githubusercontent.com/jarpsimoes/"
        "tools-automator/main/add_mysql_8/playbooks/mysql-8-single-node/playbook_server.yaml"
}


@click.command()
@click.option('-a', '--arch', 'arch', required=True, help='Single node arch or Master slave arch',
              type=click.Choice(ArchAvailable.__members__), prompt=True)
@click.option('-v', '--version', 'version', required=True, help='Mysql Version (Supported 8, 5.7)',
              type=click.Choice(['8', '5.7', '57']))
@click.option('-t', '--target', 'target', default='./.tmp_gen', help='Define target')
@click.option('-h', '--database-host', 'database_host', required=True, prompt=True,
              help='Database server host')
@click.option('-u', '--ssh-user', 'user_ssh', help='Set remote user for ssh connection',
              default=None)
@click.option('-rdb', '--root-database-password', 'root_database_password', required=True,
              help="Set MySQL root password", prompt=True, hide_input=True,
              confirmation_prompt=True)
def create_mysql(arch: str, version: str, target: str, database_host: str, user_ssh: str,
                 root_database_password: str):

    source_key: str = f'{arch}_{version.replace(".", "")}'

    if not sources.__contains__(source_key):
        click.echo(f'Version {version} not supported')
        sys.exit(1)

    click.echo(f'Architecture Type: {arch} - MySQL Version {version}')

    target_folder_name = Commons.Utils.create_working_path(target)

    click.echo(f'Target folder: {target_folder_name}')

    Commons.Utils.get_playbook_from_git(str(sources[source_key]),
                                        f'{target_folder_name}/{arch}.yaml')

    Commons.Utils.create_ini_file(user_ssh, database_host, root_database_password,
                                  f'{target_folder_name}/inventory.ini')

    click.echo("Progress...")

    ansible_helper = AnsibleHelper()
    ansible_helper.run_playbook(inventory_file=f'{target_folder_name}/inventory.ini',
                                playbook_file=f'{target_folder_name}/{arch.upper()}.yaml',
                                remote_user=user_ssh)
