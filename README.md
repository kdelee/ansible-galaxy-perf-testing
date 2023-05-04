# Before you start
Set up $PWD/config/ansible.cfg with proper ansible galaxy url and token
Be logged into registry.redhat.io

# Build locust container
This adds locust inside the base ansible image you want

```
podman build . --tag locust-ansible-galaxy-214 --build-arg ee_container=ee-minimal-rhel8
```

# Run locust
This runs locust in the container in the background.
It maps the ansible.cfg into the container and attatches the container locust port to the local port

```
podman run -d -v $PWD/config:/etc/ansible/:z -p 8089:8089 localhost/locust-ansible-galaxy-214:latest --name locust-ansible-galaxy
```

# Follow logs
When you start the podman command, passing `--name locust-ansible-galaxy` assigns that name to the container. Then at any time you can attatch/detach to the logs.

```
podman -f locust-ansible-galaxy
```


If you are running this on a remote machine, you can connect to the locust dashboard by portforwarding from your local machine.
```
ssh -L 127.0.0.1:8089:$REMOTE_HOST_IP:8089 -N -f $REMOTE_USER@$REMOTE_HOST_IP
```
The dashboard is then available at your local `127.0.0.1:8089`. Note if this port is busy you can choose any other available local port.
