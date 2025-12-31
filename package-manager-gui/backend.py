import subprocess

def run(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        return e.output

def user_packages():
    return run("apt-mark showmanual | head -n 30")

def system_packages():
    return run(
        "comm -23 <(dpkg-query -f '${binary:Package}\n' -W | sort) "
        "<(apt-mark showmanual | sort) | head -n 30"
    )

def install(pkg):
    return run(f"sudo apt install -y {pkg}")

def remove(pkg):
    return run(f"sudo apt remove -y {pkg}")

def update(pkg):
    return run(f"sudo apt install --only-upgrade -y {pkg}")
