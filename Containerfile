ARG ee_container=ee-29-rhel8
FROM registry.redhat.io/ansible-automation-platform-23/$ee_container
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install locust
# turn off python output buffering
ENV PYTHONUNBUFFERED=1
EXPOSE 8089 5557
COPY locustfile.py .
ENTRYPOINT ["locust"]
