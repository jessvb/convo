FROM tensorflow/tensorflow:1.15.0-py3

WORKDIR /usr/src/app

COPY requirements.txt ./

# install pip3
RUN apt -y install python3-pip
RUN pip3 --version

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000
