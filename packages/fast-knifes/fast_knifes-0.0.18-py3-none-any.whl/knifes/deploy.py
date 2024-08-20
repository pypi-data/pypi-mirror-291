import os
import sys
import time
import subprocess
from os import path
from knifes.shell import print_err, print_succ

GUNICORN_SYSTEMD_TEMPLATE = """[Unit]
Description={NAME}.service
ConditionPathExists={GUNICORN_PATH}
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory={WORKING_DIRECTORY}
ExecStart={GUNICORN_PATH} -c {GUNICORN_CONF_PATH}
ExecReload=kill -HUP $MAINPID
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target"""


def print_help():
    print(
        "start       --start gunicorn\n"
        "reload      --reload gunicorn\n"
        "stop        --stop gunicorn\n"
        "configure   --configure gunicorn service\n"
        "log n       --read gunicorn last log\n"
        "modules     --install modules\n"
        "knifes      --force install latest knifes\n"
    )


def main_script(project_dir, log_dir, project_name):
    args = sys.argv[1:]
    if not args:
        print_help()
    elif args[0] == "reload":
        reload_gunicorn(project_dir, project_name, log_dir)
    elif args[0] == "modules":
        install_modules(project_dir)
    elif args[0] == "log":
        line_count = 10 if len(args) == 1 else args[1]
        read_last_log(log_dir, line_count)
    elif args[0] == "start":
        start_gunicorn(project_dir, project_name, log_dir)
    elif args[0] == "stop":
        stop_gunicorn(project_name, log_dir)
    elif args[0] == "knifes":
        install_latest_knifes(project_dir)
    elif args[0] == "configure":
        configure(project_dir, project_name)
    else:
        print_help()


def install_latest_knifes(project_dir):
    activate_path = path.join(project_dir, "venv/bin/activate")
    cmd = f"source {activate_path} && pip install fast-knifes --index-url https://pypi.python.org/simple -U"
    output, err, _ = _run_command(cmd)
    print_succ(output)
    print_err(err)  # warning message


def pull_latest_code(project_dir):
    cmd = f"cd {project_dir} && git pull origin main"
    output, err, code = _run_command(cmd)
    if code != 0:
        print_err(err)
        raise SystemExit
    print_succ(output)
    print_succ(err)  # warning message


def install_modules(project_dir):
    activate_path = path.join(project_dir, "venv/bin/activate")
    requirements_path = path.join(project_dir, "requirements.txt")
    cmd = f"source {activate_path} && pip install -r {requirements_path}"
    output, err, code = _run_command(cmd)
    if code != 0:
        print_err(f"failed to install modules: {err}")
        raise SystemExit
    print_succ(output)
    print_succ(err)  # warning message


def read_last_log(log_dir, line_count):
    gunicorn_log_path = path.join(log_dir, "gunicorn.log")
    output, err, _ = _run_command(f"tail -{line_count} {gunicorn_log_path}")
    print_succ(output)
    print_err(err)
    return output, err


def gunicorn_status(project_name):
    output, err, _ = _run_command(f"systemctl status {project_name}")
    print_succ(output)
    print_err(err)  # warning message


def configure(project_dir, project_name):
    systemd_conf_filepath = f"/etc/systemd/system/{project_name}.service"
    if os.path.exists(systemd_conf_filepath):
        print_err(f"{systemd_conf_filepath} already exists, delete it first if you want to reconfigure")
        return

    gunicorn_path = path.join(project_dir, "venv/bin/gunicorn")
    gunicorn_conf_path = path.join(project_dir, f"gunicorn_{project_name}_conf.py")
    with open(systemd_conf_filepath, "w", encoding="utf-8") as f:
        f.write(
            GUNICORN_SYSTEMD_TEMPLATE.replace("{NAME}", project_name)
            .replace("{GUNICORN_PATH}", gunicorn_path)
            .replace("{GUNICORN_CONF_PATH}", gunicorn_conf_path)
            .replace("{WORKING_DIRECTORY}", project_dir)
        )
    os.chmod(systemd_conf_filepath, mode=0o755)

    output, err, code = _run_command(f"systemctl daemon-reload && systemctl enable {project_name}")
    if code != 0:
        print_err(f"failed to enable service: {err}")
        raise SystemExit
    print_succ(output)
    print_succ(err)  # warning message
    print_succ(f"service {project_name} enabled")


def start_gunicorn(project_dir, project_name, log_dir):
    status, _, _ = _run_command(f"systemctl is-active {project_name}")
    if status == "active":
        print_err(f"{project_name} is already running, use reload to restart it gracefully")
        raise SystemExit

    install_modules(project_dir)  # install modules before starting gunicorn

    _, err, code = _run_command(f"systemctl start {project_name}")
    if code != 0:
        print_err(err)
        raise SystemExit
    print_succ(f"{project_name} started")

    time.sleep(2)
    read_last_log(log_dir, 6)


def reload_gunicorn(project_dir, project_name, log_dir):
    pull_latest_code(project_dir)
    install_modules(project_dir)

    status, _, _ = _run_command(f"systemctl is-active {project_name}")  # active | inactive
    if status == "active":
        print_err(f"{project_name} is already running, use reload to restart it gracefully")
        raise SystemExit

    _, err, code = _run_command(f"systemctl reload {project_name}")
    if code != 0:
        print_err(err)
        raise SystemExit
    print_succ(f"{project_name} reloaded")

    # read last 6 lines of log
    time.sleep(2)
    read_last_log(log_dir, 6)


def stop_gunicorn(project_name, log_dir):
    status, _, _ = _run_command(f"systemctl is-active {project_name}")
    if status == "inactive":
        print_err(f"{project_name} is already stopped")
        raise SystemExit

    _, err, code = _run_command(f"systemctl stop {project_name}")
    if code != 0:
        print_err(err)
        raise SystemExit
    print_succ(f"{project_name} stopped")

    # read last 6 lines of log
    time.sleep(2)
    read_last_log(log_dir, 6)


def _run_command(command) -> tuple[str, str, int]:
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
    return result.stdout.strip(), result.stderr.strip(), result.returncode
