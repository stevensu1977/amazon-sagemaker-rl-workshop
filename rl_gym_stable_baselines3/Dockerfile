ARG AWS_REGION
FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:1.10.2-cpu-py38-ubuntu20.04-sagemaker

##############################################################
# Compatible g++ version for Tensorflow installation
##############################################################

RUN apt update

##############################################################



RUN pip install --upgrade pip 
RUN pip install sagemaker_containers


ENV LD_LIBRARY_PATH=/usr/local/openmpi/lib:$LD_LIBRARY_PATH
ENV PATH /usr/local/openmpi/bin/:$PATH
ENV PATH=/usr/local/nvidia/bin:$PATH

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# SSH. Partially taken from https://docs.docker.com/engine/examples/running_ssh_service/
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server && \
    mkdir -p /var/run/sshd

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Create SSH key.
RUN rm -rf /root/.ssh/
RUN mkdir -p /root/.ssh/ && \
  ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa && \
  cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys && \
  printf "Host *\n  StrictHostKeyChecking no\n" >> /root/.ssh/config

# Hostname Fix
COPY resources/changehostname.c /
COPY resources/change-hostname.sh /
COPY resources/change-hostname.sh /usr/local/bin/change-hostname.sh

RUN chmod +x /usr/local/bin/change-hostname.sh
RUN chmod +x /change-hostname.sh


##############################################################
WORKDIR /opt

############################################
# Roboschool
############################################

RUN apt-get update && apt-get install -y \
      git cmake ffmpeg pkg-config \
      qtbase5-dev libqt5opengl5-dev libassimp-dev \
      libtinyxml-dev \
      libgl1-mesa-dev \
    && cd /opt \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y libboost-python-dev


#RUN curl -fSsL -O https://bootstrap.pypa.io/get-pip.py && \
#    python get-pip.py && \
#    rm get-pip.py

RUN pip install --upgrade \
    pip \
    setuptools


ENV PYTHONUNBUFFERED 1

############################################
# Baselines
############################################
#RUN apt-get update && apt-get install -y cmake libopenmpi-dev python3-dev zlib1g-dev wget

ENV BASELINES_PATH /opt/baselines/



############################################
# Stable Baselines
############################################
RUN pip install install stable-baselines3[extra] 
RUN pip install atari-py==0.2.9 gym==0.22.0 Flask==2.1.0


############################################
# import atari roms http://www.atarimania.com/rom_collection_archive_atari_2600_roms.html
############################################
RUN apt-add-repository multiverse && apt-get update
RUN apt-get install -y unrar unzip

RUN curl -OL http://www.atarimania.com/roms/Roms.rar \ 
    && mkdir ROMS \
    && unrar e -o+ ./Roms.rar ROMS/ 

RUN python -m atari_py.import_roms /opt/ROMS
RUN rm -rf ./Roms.rar opt/ROMS

############################################
# fix videorecord ffmpeg mpeg4 to h264
############################################
RUN cp /usr/bin/ffmpeg /opt/conda/bin/ffmpeg

############################################
# Test Installation
############################################
# Test to verify if all required dependencies installed successfully or not.
RUN python -c "import gym;"


