import subprocess

roles = subprocess.run(["date"],  ["+%s"])


# roles = subprocess.run(["podman", "exec", "-ti", "8536a0dd5a07", "ansible-galaxy", "install", "buluma.bootstrap", "-p", "/home/ansible_2.9.27/roles/"])
# print("The exit code was: %d" % roles.returncode)