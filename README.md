# Tools Automator

[![Pylint](https://github.com/jarpsimoes/tools-automator/actions/workflows/pylint.yml/badge.svg)](https://github.com/jarpsimoes/tools-automator/actions/workflows/pylint.yml)

That project is a CLI (Command Line Interface) to help remote tools configuration with ansible. Contains ansible playbooks compatible with RedHat and Ubuntu servers. Can be used to automate tools deployments.

To use this CLI, must be provisioned ssh connections to allow ssh connections with ansible. Can be used ssh-copy-id, to add own certificate on remote machine or another method to allow ssh connections with ansible.


> Example: ```` $ ssh-copy-id <user>@<ip> ````

---

### Required

Before use CLI, must be install tools-automator from PIP:

````bash
   $ pip install tools-automator
````

### MYSQL Server - Single Node

1. ````bash
    $ create_mysql --arch single_node --ssh-user user
    ````

2. ````bash
   Database host: 1.2.3.4 #Server IP
   Root database password: #Define Root database
   Repeat for confirmation: #Confirm password
   ````

---
> NOTE: You can check all options with create_mysql --help
