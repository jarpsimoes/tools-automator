import subprocess
import time
from enum import unique, Enum

import click
import os
import urllib.request


@unique
class ArchAvailable(Enum):
    single_node = 0
    master_slave = 1


# TODO - Populate that object with remote data
class PlaybookUrls:
    sources = {
        "single_node":
            "https://raw.githubusercontent.com/jarpsimoes/ansible-configure-http-server/main/playbooks/config_vm.yaml",
        "master_slave":
            "https://github.com/jarpsimoes/ansible-configure-http-server/blob/main/playbooks/config_vm_rollback.yaml"
    }


@click.command()
@click.option('-a', '--arch', 'arch', required=True, help='Single node arch or Master slave arch',
              type=click.Choice(ArchAvailable.__members__), prompt=True)
@click.option('-t', '--target', 'target', default='./.tmp_gen', help='Define target')
@click.option('-u', '--ssh-user', 'user_ssh', required=True, help='Set remote user for ssh connection', prompt=True)
@click.option('-p', '--password-user', 'password_ssh', required=True, help='Set password for ssh connection',
              prompt=True)
@click.option('-k', '--ssh-key', 'ssh_key', default=None, help='Path to ssh key')
def create_mysql(arch: str, target: str, user_ssh: str, password_ssh: str, ssh_key: str):
    click.echo(f'Architecture Type: {arch}')
    target_folder_name = target
    iterate = 0
    if os.path.isdir(target_folder_name):
        target_folder_name = f'{target_folder_name}_{iterate}'

        while os.path.isdir(target_folder_name):
            target_folder_name = f'{target}_{iterate}'
            iterate += 1
    os.mkdir(target_folder_name)

    click.echo(f'Target folder: {target_folder_name}')

    base_yaml: urllib.request = urllib.request.urlopen(str(PlaybookUrls().sources[arch]))

    if base_yaml.getcode() != 200:
        click.echo(f'Request failed. Check your internet connection and repeat')
        exit(1)

    playbook_file = open(f'{target_folder_name}/{arch}.yaml', "w")
    playbook_file.write(base_yaml.read().decode("utf-8"))
    playbook_file.close()

    if not ssh_key:
        click.echo("SSH Key will be generated")
        create_ssh_key = subprocess.run(['ssh-keygen', '-b', '2048', '-t', 'rsa',
                                         '-f', f'{target_folder_name}/sshkey_auto', '-q', '-N', '\\'""'\\'],
                                        capture_output=True)

        if create_ssh_key.returncode != 0:
            click.echo(f'ERROR: Failed on ssh key create: {create_ssh_key.stderr.decode("utf-8")}')
            exit(1)

        click.echo(f'SSH created successful [{target_folder_name}/sshkey_auto]')

