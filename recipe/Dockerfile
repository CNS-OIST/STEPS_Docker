FROM ubuntu:18.04
MAINTAINER Tristan CAREL <tristan.carel@epfl.ch>

RUN apt-get update \
 && apt-get install -y \
    bzip2 \
    cmake \
    graphviz \
    git \
    libmpich-dev \
    libopenblas-dev \
    pandoc \
    python \
    wget \
 && rm -rf /var/lib/apt/lists/*

ENV GOSU_VERSION 1.11
RUN dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
 && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
 && chmod +x /usr/local/bin/gosu \
# verify that the binary works
 && gosu nobody true

ARG MINICONDA_VERSION=3-4.5.11

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
 && wget --quiet https://repo.continuum.io/miniconda/Miniconda${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh \
 && /bin/bash ~/miniconda.sh -b -p /opt/conda \
 && rm ~/miniconda.sh \
 && /opt/conda/bin/pip install \
    cython \
    jupyter \
    jupyterlab \
    matplotlib \
    python-libsbml

ENV PATH "/opt/conda/bin:$PATH"

ARG BUILD_PETSC=true
RUN if [ "x$BUILD_PETSC" = xtrue ] ; then ( \
    git clone -b maint https://bitbucket.org/petsc/petsc /var/src/petsc \
 && cd /var/src/petsc \
 && /usr/bin/python2 ./configure \
     --prefix=/usr \
     --with-fc=0 \
     --with-64-bit-indices \
     --with-debugging=0 COPTFLAGS='-O3 -march=native -mtune=native' CXXOPTFLAGS='-O3 -march=native -mtune=native' \
 && cd /var/src/petsc ; make MAKE_NP=1 \
 && make install \
 && rm -rf /var/src/petsc \
 && ldconfig \
 ) fi

ARG STEPS_VERSION=3.4.0
RUN git clone --recursive https://github.com/CNS-OIST/STEPS.git /var/src/STEPS \
 && cd /var/src/STEPS \
 && git checkout "$STEPS_VERSION" \
 && mkdir build \
 && cd build \
 && cmake .. \
 && make \
 && make install \
 && rm -rf /var/src/STEPS

RUN git clone https://github.com/CNS-OIST/STEPS_Example.git /var/src/STEPS_Example \
 && mv /var/src/STEPS_Example/user_manual/source /var/src/user_manual \
 && rm -rf /var/src/STEPS_Example

ARG EXAMPLE_NOTEBOOKS_TO_REBUILD="diffusion_boundary diffusion getting_started ip3 memb_pot sbml_importer surface_diffusion_boundary surface_diffusion well_mixed"
# https://nbconvert.readthedocs.io/en/latest/usage.html#convert-notebook
RUN cd /var/src/user_manual \
 && jupyter nbconvert \
     --to notebook \
     --execute \
     --inplace \
     --ExecutePreprocessor.timeout=360 \
     $EXAMPLE_NOTEBOOKS_TO_REBUILD

ENV LANG en_US.utf8
ENV SHELL=/bin/bash

ADD entrypoint /usr/bin/
ENTRYPOINT ["/usr/bin/entrypoint"]

CMD [ \
    "jupyter", "lab", \
    "--no-browser", "--allow-root", \
    "--ip=0.0.0.0", \
    "--notebook-dir=/opt/src/notebooks" \
]
