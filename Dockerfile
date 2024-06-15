FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04

# SH -> BASH
SHELL ["/bin/bash", "-c"]

# initialize
RUN apt-get clean && apt-get update
RUN apt-get upgrade -y --fix-missing

# set env
ENV TZ=Asia/Tokyo

# install curl, git, build-essential, opengl
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y build-essential
RUN apt-get install -y libgl1-mesa-glx

# install python
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN apt-get install -y python3.11-dev

# initialize python
RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /work

COPY . /work

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50006