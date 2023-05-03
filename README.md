
```
# set up $PWD/config/ansible.cfg with proper ansible galaxy url and token

# be logged into registry.redhat.io

# build container that adds locust inside the base ansible image you want
podman build . --tag locust-ansible-galaxy-214 --build-arg ee_container=ee-minimal-rhel8

#this runs locust locally and maps the ansible.cfg into the container and attatches the container locust port to the local port
podman run -d -v $PWD/config:/etc/ansible/:z -p 8089:8089 localhost/locust-ansible-galaxy-214:latest
```
