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
    "SINGLE_NODE":
        "https://raw.githubusercontent.com/jarpsimoes/"
        "tools-automator/main/playbooks/mysql-57-single-node/playbook_server.yaml",
    "MASTER_SLAVE":
        "https://raw.githubusercontent.com/jarpsimoes/"
        "tools-automator/main/playbooks/mysql-57-single-node/playbook_server.yaml"
}


@click.command()
@click.option('-a', '--arch', 'arch', required=True, help='Single node arch or Master slave arch',
              type=click.Choice(ArchAvailable.__members__), prompt=True)
@click.option('-t', '--target', 'target', default='./.tmp_gen', help='Define target')
@click.option('-h', '--database-host', 'database_host', required=True, prompt=True,
              help='Database server host')
@click.option('-u', '--ssh-user', 'user_ssh', help='Set remote user for ssh connection',
              default=None)
@click.option('-rdb', '--root-database-password', 'root_database_password', required=True,
              help="Set MySQL root password", prompt=True, hide_input=True,
              confirmation_prompt=True)
def create_mysql(arch: str, target: str, database_host: str, user_ssh: str,
                 root_database_password: str):

    click.echo(f'Architecture Type: {arch}')

    target_folder_name = Commons.Utils.create_working_path(target)

    click.echo(f'Target folder: {target_folder_name}')

    Commons.Utils.get_playbook_from_git(str(sources[arch]),
                                        f'{target_folder_name}/{arch}.yaml')

    Commons.Utils.create_ini_file(user_ssh, database_host, root_database_password,
                                  f'{target_folder_name}/inventory.ini')

    click.echo("Progress...")

    ansible_helper = AnsibleHelper()
    ansible_helper.run_playbook(inventory_file=f'{target_folder_name}/inventory.ini',
                                playbook_file=f'{target_folder_name}/{arch.upper()}.yaml',
                                remote_user=user_ssh)
