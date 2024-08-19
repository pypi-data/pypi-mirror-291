import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    import click
    from thunder import auth
    import sys
    import os
    from os.path import join
    from scp import SCPClient
    import paramiko
    import subprocess
    from multiprocessing import Process, Event
    import time
    import platform
    import getpass

    from thunder import thunder_helper
    from thunder import container_helper
    from thunder import utils
    from thunder.file_sync import start_file_sync
    
    try:
        from importlib.metadata import version
    except Exception as e:
        from importlib_metadata import version
        
    import requests
    from packaging import version as version_parser
    from thunder import api
    from yaspin import yaspin

PACKAGE_NAME = "tnr"  # update if name changes
# Get the directory of the current file (thunder.py), then go up two levels to the root
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..", "..")

# Add the src directory to sys.path
sys.path.append(root_dir)


class DefaultCommandGroup(click.Group):
    def resolve_command(self, ctx, args: list):
        try:
            # Try to resolve the command normally
            check_for_update()
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
        except click.exceptions.UsageError:
            # If no command is found, default to 'run' and include the args
            return "run", run, args


@click.group(
    cls=DefaultCommandGroup,
    help="This CLI is the interface between you and Thunder Compute.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.pass_context
@click.version_option(version=version(PACKAGE_NAME))
def cli(ctx):
    utils.setup_instance()

@cli.command(
    help="Runs a specified task on Thunder Compute. This is the default behavior of the tnr command. Please see thundergpu.net for detailed documentation.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run(args):
    if not args:  # Check if args is empty
        click.echo("No arguments provided. Exiting...")
        sys.exit(0)

    id_token, refresh_token, uid = auth.load_tokens()

    if not id_token or not refresh_token:
        click.echo("Please log in to begin using Thunder Compute.")
        id_token, refresh_token, uid = auth.login()

        if not id_token or not refresh_token:
            return

    id_token, refresh_token, uid = auth.handle_token_refresh(refresh_token)

    # Create an instance of Task with required arguments
    task = thunder_helper.Task(args, uid)

    # Execute the task
    if not task.execute_task(id_token):
        return

    # Close the session
    if not task.close_session(id_token):
        click.echo("Failed to close the session.")

@cli.command(help="Logs in to Thunder Compute.")
def login():
    auth.login()

@cli.command(help="Logs out from the Thunder Compute CLI.")
def logout():
    auth.logout()

@cli.command(help="Set which type of GPU to run on.")
@click.argument("device_type", required=False)
@click.option("-n", "--ngpus", type=int)
@click.option("--raw", required=False, is_flag=True)
def device(device_type, ngpus, raw):
    basedir = join(os.path.expanduser("~"), ".thunder")
    device_file = join(basedir, "dev")
    num_file = join(basedir, "ngpus")
    supported_devices = set(
        [
            "cpu",
            "t4",
            "v100",
            "a100",
            "l4",
            "p4",
            "p100",
            "h100",
        ]
    )
                    
    if device_type is None:
        with open(device_file, "r") as f:
            device = f.read().strip()

        if device not in supported_devices:
            # If not valid, set it to the default value
            device = "t4"
            with open(device_file, "w") as f:
                f.write(device)
                
        if ngpus is None:
            with open(num_file, "r") as f:
                content = f.read().strip()

            if not content.isnumeric():
                # If not valid, set it to the default value
                ngpus = 1
                with open(num_file, "w") as f:
                    f.write(str(ngpus))
            else:
                ngpus = int(content)

        if raw is not None and raw:
            if ngpus == 1:
                click.echo(device.upper())
            else:
                click.echo(f'{ngpus}x{device.upper()}')
            return
        
        if device.lower() == 'cpu':
            click.echo(click.style("📖 No GPU selected - use `tnr device <gpu-type>` to select a GPU", fg="white"))
            return

        if ngpus == 1:
            click.echo(click.style(f"📖 Current GPU: {device.upper()}", fg="white"))
        else:
            click.echo(click.style(f"📖 Current GPUs: {ngpus} x {device.upper()}", fg="white"))
        
        available_gpus = utils.get_available_gpus()
        if available_gpus is not None and len(available_gpus) > 0:
            click.echo(click.style(f"🌐 Available GPUs: {', '.join(available_gpus)}", fg="white"))
        return

    if device_type.lower() not in supported_devices:
        click.echo(
            click.style(
                f"⛔ Unsupported device type: {device_type}. Please select one of CPU, T4, V100, A100, L4, P4, P100, or H100",
                fg="red",
            )
        )
        exit(1)
        
    if device_type.lower() == 'cpu':
        with open(device_file, "w") as f:
            f.write(device_type.lower())

        with open(num_file, "w") as f:
            f.write("0")

        click.echo(click.style(f"✅ Device set to CPU, you are now disconnected from any GPUs.", fg="green"))
        return 
    
    with open(device_file, "w") as f:
        f.write(device_type.lower())
    
    if ngpus is None:
        ngpus = 1
        
    with open(num_file, "w") as f:
        f.write(str(ngpus))

    click.echo(click.style(f"✅ Device set to {ngpus} x {device_type.upper()}", fg="green"))

def add_key_to_instance(id_token):
    add_key_to_instance_url = "https://add-key-to-instance-b7ngwrgpka-uc.a.run.app"
    try:
        headers = {
            "Authorization": "Bearer " + id_token,
            "Content-Type": "application/json",
        }

        response = requests.post(add_key_to_instance_url, headers=headers, timeout=120)
        if response.status_code == 401:
            # Retry with refreshed token
            id_token, refresh_token, uid = auth.handle_token_refresh(refresh_token)
            headers = {
                "Authorization": "Bearer " + id_token,
                "Content-Type": "application/json",
            }
            response = requests.post(
                add_key_to_instance_url, headers=headers, timeout=120
            )
            
        return response

    except Exception as _:
        return None


@cli.command(help="Start running in a thunder container!")
@click.option("-s", "--sync", required=False, is_flag=True)
def start(sync):
    id_token, refresh_token, uid = auth.load_tokens()
    if not id_token or not refresh_token:
        click.echo("Please log in to begin using Thunder Compute.")
        id_token, refresh_token, uid = auth.login()

        if not id_token or not refresh_token:
            return

    if not api.is_token_valid(id_token):
        id_token, refresh_token, uid = auth.handle_token_refresh(refresh_token)

    with yaspin(text="Setting up Thunder Compute instance", color="blue") as spinner:
        create_instance_url = "https://create-ec2-instance-b7ngwrgpka-uc.a.run.app"
        try:
            headers = {
                "Authorization": "Bearer " + id_token,
                "Content-Type": "application/json",
            }

            response = requests.post(create_instance_url, headers=headers, timeout=120)
            if response.status_code == 401:
                # Retry with refreshed token
                id_token, refresh_token, uid = auth.handle_token_refresh(refresh_token)
                headers = {
                    "Authorization": "Bearer " + id_token,
                    "Content-Type": "application/json",
                }
                response = requests.post(
                    create_instance_url, headers=headers, timeout=120
                )

            if response.status_code != 200:
                spinner.ok("⛔")
                click.echo(
                    click.style(
                        f"Failed to setup Thunder Compute instance for the following reason: {response.text}",
                        fg="red",
                    )
                )
                exit(1)

        except Exception as _:
            msg = "Failed to create a Thunder Compute instance. Please report this issue to the developers!"
            click.echo(click.style(msg, fg="red"))
            exit(1)

        if response.status_code != 200:
            exit(1)

        basedir = join(os.path.expanduser("~"), ".thunder")
        keyfile = join(basedir, "id_rsa")
        if "pem_key" in response.json():
            if os.path.exists(keyfile):
                os.chmod(keyfile, 0o600)

            with open(keyfile, "w") as f:
                f.write(response.json()["pem_key"])
            os.chmod(keyfile, 0o400)

        ip = response.json()["public_ip"]

        if not os.path.exists(keyfile):
            response = add_key_to_instance(id_token)
            if response is None or response.status_code != 200:
                click.echo(
                    click.style(
                        "Unable to find rsa key for thunder (expected to be in ~/.thunder/id_rsa) and failed to create a new one",
                        fg="red",
                    )
                )
                exit(1)
        
            if os.path.exists(keyfile):
                os.chmod(keyfile, 0o600)

            with open(keyfile, "w") as f:
                f.write(response.json()["pem_key"])
            os.chmod(keyfile, 0o400)
        
        if platform.system() == 'Windows':
            subprocess.run([
                'icacls',
                fr'{keyfile}',
                r'/inheritance:r',
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run([
                'icacls',
                f"{keyfile}",
                '/grant:r',
                fr'{getpass.getuser()}:(R)'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        spinner.ok("✅")    
    
    with yaspin(
        text=f"Connecting to Thunder Compute instance {ip} (this can take about a minute)",
        color="blue",
    ) as spinner:
        
        start_time = time.time()
        connection_successful = False
        while start_time + 60 > time.time():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=10)
                connection_successful = True
                break
            except paramiko.ssh_exception.AuthenticationException as e:
                response = add_key_to_instance(id_token)
                if response is None or response.status_code != 200:
                    break
                if os.path.exists(keyfile):
                    os.chmod(keyfile, 0o600)

                with open(keyfile, "w") as f:
                    f.write(response.json()["pem_key"])
                os.chmod(keyfile, 0o400)

            except Exception as e:
                continue
            
        if connection_successful:
            spinner.ok("✅")
        else:
            spinner.fail("⛔")
            click.echo(
                click.style(
                    "Failed to connect to the thunder compute instance within a minute. Please retry this command or contant the developers at support@thundercompute.com if this issue persists.",
                    fg="red",
                )
            )
            exit(1)

        ssh.exec_command("mkdir -p ~/.thunder && chmod 700 ~/.thunder")
        ssh.exec_command("pip install --upgrade tnr")
        scp = SCPClient(ssh.get_transport())
        scp.put(join(basedir, "token"), remote_path="~/.thunder/token")

        devfile = join(basedir, "dev")
        ngpus_file = join(basedir, "ngpus")
        scp.put(devfile, remote_path="~/.thunder/dev")        
        scp.put(ngpus_file, remote_path="~/.thunder/ngpus")

    if sync:
        with yaspin(
            text="Copying current directory over recursively", color="blue"
        ) as spinner:
            scp.put(os.getcwd(), recursive=True)
            spinner.ok("✅")

        with yaspin(text="Setting up automatic file syncing", color="blue") as spinner:
            is_done_event = Event()
            file_sync_process = Process(
                target=start_file_sync,
                args=(
                    is_done_event,
                    ip,
                ),
            )
            file_sync_process.start()
            spinner.ok("✅")

    click.echo(
        click.style(
            f"⚡ You are connected to a Thunder Compute instance on {ip}! Press control-d to disconnect ⚡",
            fg="cyan",
        )
    )
    
    if sync:
        init_dir = f'~/{os.path.basename(os.getcwd())}'
    else:
        init_dir = '~'
        
    if platform.system() == 'Windows':
        subprocess.run(
            [
                'ssh',
                f'ubuntu@{ip}',
                '-o',
                'StrictHostKeyChecking=accept-new',
                '-i',
                fr'{keyfile}',
                '-t',
                f'cd {init_dir} && exec /home/ubuntu/.local/bin/tnr run /bin/bash'
            ],
            shell=True,
        )
    else:
        subprocess.run(
            [
                f"ssh ubuntu@{ip} -o StrictHostKeyChecking=accept-new -i {keyfile} -t 'cd {init_dir} && exec /home/ubuntu/.local/bin/tnr run /bin/bash'"
            ],
            shell=True,
        )
    click.echo(click.style("⚡ Exiting thunder instance ⚡", fg="cyan"))
    
    if sync:
        is_done_event.set()

    ssh.close()


def check_for_update():
    try:
        current_version = version(PACKAGE_NAME)
        response = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json", timeout=1)
        json_data = response.json() if response else {}
        latest_version = json_data.get("info", {}).get("version", None)
        if version_parser.parse(current_version) < version_parser.parse(latest_version):
            click.echo(
                click.style(
                    f"New version of tnr available, please run pip install --upgrade tnr",
                    fg="blue",
                )
            )

    except Exception as e:
        click.echo(f"Error checking for update: {e}", err=True)


if __name__ == "__main__":
    cli()
