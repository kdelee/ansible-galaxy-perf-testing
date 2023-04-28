import subprocess
import time

from locust import User, between, TaskSet, task, events

def execute_galaxy(collection="awx.awx"):
    process = subprocess.Popen([ 
            "podman",
            "run",
            "--rm",
            "-v",
            "/home/kdelee/foo:/etc/ansible/:z", #FIXME: make configurable , /home/kdelee/foo is where I have my ansible.cfg
            "registry.redhat.io/ansible-automation-platform-23/ee-29-rhel8", #FIXME: make this configurable 
            "ansible-galaxy",
            "collection",
            "install",
            collection],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            )
    stdout, stderr = process.communicate()
    assert process.returncode == 0, f"Download failed: stdout: {stdout}, stderr:{stderr}"
    return process
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
    def execute_galaxy(self):
        self.client.execute_galaxy(collection="awx.awx")