FROM python:3.10-slim

RUN useradd -r -m apprunner
USER apprunner
ENV HOME=/home/apprunner
ENV PATH=$HOME/.local/bin:$PATH
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt
COPY . .
RUN pip install --user .
ENV LOG_LEVEL=WARNING
ENV ENV=PROD
RUN mkdir /tmp/test
CMD ["ftp_server", "-h", "0.0.0.0"]

