import subprocess
import time
import os

from locust import User, between, TaskSet, task, events

def execute_galaxy(collection="awx.awx", volume_mount=f"{os.getcwd()}/config", se_linux_relabel=':z', image="registry.redhat.io/ansible-automation-platform-23/ee-29-rhel8"):
    process = subprocess.Popen([
            "podman",
            "run",
            "--rm",
            "-v",
            f"{volume_mount}:/etc/ansible/{se_linux_relabel}", #FIXME: make configurable , /home/kdelee/foo is where I have my ansible.cfg
            image, #FIXME: make this configurable
            "ansible-galaxy",
            "collection",
            "install",
            collection],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
    stdout, stderr = process.communicate()
    assert process.returncode == 0, stderr
    assert "was installed successfully" in str(stdout)
    return process

class GalaxyClient:

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            exception = None # if no error, no exception
            res = None # if error, no res from execute_galaxy
            try:
                res = execute_galaxy(*args, **kwargs)
            except Exception as e:
                exception = e
                print(f'error {e}')

            events.request.fire(
                request_type="galaxy",
                name=name,
                response_time=int((time.time() - start_time) * 1000),
                response_length=1,
                response=res,
                context=None,
                exception=exception,
            )

        return wrapper

# This class will be executed when you fire up locust
class GalaxyUser(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        min_wait = 0
        max_wait = 0
        wait_time = between(min_wait, max_wait)
        self.client = GalaxyClient()

    @task
    def execute_galaxy_task1(self):
        self.client.execute_galaxy(collection="awx.awx")