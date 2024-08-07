FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-devel

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 libgl1 wget

WORKDIR /code