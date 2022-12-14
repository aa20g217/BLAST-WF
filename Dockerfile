FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main

# Install pip
#RUN apt-get install -y python3-pip

#install and setup conda
RUN apt-get update && apt-get install -y git wget
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
   && rm -f Miniconda3-latest-Linux-x86_64.sh


RUN conda config --add channels bioconda --add channels conda-forge --add channels ambermd
RUN apt-get install -y tar
RUN wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-linux.tar.gz
RUN tar -zxvf ncbi-blast-2.13.0+-x64-linux.tar.gz
RUN mv ncbi-blast-2.13.0+ blast

#ßRUN blast
# Install MUSCLE
#RUN conda install -c bioconda blast=2.7.1
#RUN conda install -c conda-forge gnutls

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
