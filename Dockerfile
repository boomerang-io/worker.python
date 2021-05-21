FROM python:3.9.5

WORKDIR /usr/src/app

COPY . .

ENTRYPOINT ["python3", "-m", "pyworker"]
