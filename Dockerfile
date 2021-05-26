FROM python:3.9.5

WORKDIR /usr/src

COPY ./pyworker ./pyworker

ENTRYPOINT ["python3", "-m", "pyworker"]
