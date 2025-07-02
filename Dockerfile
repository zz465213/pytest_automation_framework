# https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_linux-x64_bin.tar.gz
# https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz

FROM python:3.11-slim AS build
COPY requirements.txt /opt/requirements.txt
COPY framework_requirements/openjdk-11+28_linux-x64_bin.tar.gz /opt/
COPY framework_requirements/allure-2.24.0.tgz /opt/
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
RUN tar -xvzf /opt/openjdk-11+28_linux-x64_bin.tar.gz -C /usr/local
RUN rm /opt/openjdk-11+28_linux-x64_bin.tar.gz
RUN mkdir -p /opt/allure && tar -xvzf /opt/allure-2.24.0.tgz -C /opt/allure --strip-components=1
RUN rm /opt/allure-2.24.0.tgz
ENV JAVA_HOME=/usr/local/jdk-11
ENV PATH=$JAVA_HOME/bin:/opt/allure/bin:$PATH
RUN pip config --user set global.progress_bar off && \
pip install -r /opt/requirements.txt
WORKDIR /test
COPY . .

# ENTRYPOINT [ python run.py --test_type="api" --env="local" -m="api and p1" ]
# docker build -t leon:test .
# docker run --rm -it -v /$(pwd):/test qa bash