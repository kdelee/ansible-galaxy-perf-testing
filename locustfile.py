import subprocess
import time
import os
import uuid
import random

from locust import User, between, TaskSet, task, events

def execute_galaxy(collection_dir=".", collections=["community.crypto", "awx.awx", "ansible.windows", "kubernetes.core", "ansible.utils", "community.docker",
                                                   "ansible.netcommon", "amazon.aws", "ansible.posix", "community.general", "arista.avd", "borari.pentesting_collection",
                                                   "dkraklan.terraform_vmware_vm", "sabyadi.zhmc", "itsbryantp.zos_test", "ibm.zos_package_manager", 
                                                   "elfelip.keycloak", "joej164.ansible_sample_collection", "jiholland.cisco", "ephracis.doksi"]):
    process = subprocess.Popen([
            "ansible-galaxy",
            "collection",
            "install",
            "-p",
            collection_dir,
            random.choice(collections)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
    stdout, stderr = process.communicate()
    assert process.returncode == 0, f'ERROR: {str(stderr).split("ERROR")[-1].strip()}'
    return process

class GalaxyClient:

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            collection_dir = f"collection_download_{uuid.uuid4()}"
            kwargs["collection_dir"] = collection_dir
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
            rm_process = subprocess.Popen([
                "rm",
                "-rf",
                collection_dir],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            rm_process.communicate()
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
        self.client.execute_galaxy()
