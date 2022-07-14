FROM python:3.9.13

# Set working directory
WORKDIR /usr/src/pyworker

# Copy required resources
COPY ./flow_tools ./flow_tools
COPY ./script_runner ./script_runner
COPY ./utils ./utils
COPY ./run.py .
COPY ./requirements.txt .

# Install pip dependencies
RUN pip install -r requirements.txt

# Run the script in development mode
ENTRYPOINT ["sh", "-c", "python3 run.py --dev"]
