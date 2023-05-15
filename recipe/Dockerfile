FROM ubuntu:23.04
MAINTAINER Tristan CAREL <tristan.carel@epfl.ch>

ARG DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV SHELL=/bin/bash
ENV TZ=Europe/Geneva

RUN apt-get --yes -qq update \
 && apt-get --yes -qq upgrade \
 && apt-get --yes -qq install \
                      bzip2 \
                      cmake \
                      cpio \
                      curl \
                      g++ \
                      gcc \
                      gfortran \
                      git \
                      graphviz \
                      htop \
                      libeigen3-dev \
                      libboost-dev \
                      libgl1 \
                      libglu1 \
                      libgsl-dev \
                      libmetis-dev \
                      libxcursor1 \
                      libxft2 \
                      libxinerama1 \
                      pandoc \
                      vim       \
                      wget \
                      zlib1g-dev \
 && apt-get --yes -qq clean \
 && rm -rf /var/lib/apt/lists/*

ENV GOSU_VERSION 1.11
RUN dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
 && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
 && chmod +x /usr/local/bin/gosu \
# verify that the binary works
 && gosu nobody true

ARG MINICONDA_VERSION=3-py39_23.1.0-1
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
 && wget --quiet https://repo.continuum.io/miniconda/Miniconda${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh \
 && /bin/bash ~/miniconda.sh -b -p /opt/conda \
 && rm ~/miniconda.sh \
 && /opt/conda/bin/pip install \
    cython \
    jupyter \
    jupyterlab \
    matplotlib \
    nose \
    python-libsbml \
    scipy \
&& /opt/conda/bin/conda install mpi4py \
&& /opt/conda/bin/conda install -c conda-forge petsc

ENV PATH "/opt/conda/bin:$PATH"

ARG GMSH_VERSION=4.11.1
RUN mkdir -p /var/src \
 && cd /var/src \
 && gmsh_sdk=gmsh-${GMSH_VERSION}-Linux64-sdk \
 && wget https://gmsh.info/bin/Linux/${gmsh_sdk}.tgz \
 && tar zxf ${gmsh_sdk}.tgz \
 && rm -rf ${gmsh_sdk}.tgz
ENV PATH "/var/src/gmsh-${GMSH_VERSION}-Linux64-sdk:$PATH"
ENV CMAKE_PREFIX_PATH=/var/src/gmsh-${GMSH_VERSION}-Linux64-sdk:/opt/conda

ARG BUILD_OMEGA_H=true
ARG OMEGA_H_VERSION=v9.34.13
RUN if [ "x$BUILD_OMEGA_H" = xtrue ] ; then ( \
    git clone \
      --single-branch -b "$OMEGA_H_VERSION" \
      https://github.com/sandialabs/omega_h.git \
      /var/src/omega_h \
 && mkdir /var/src/omega_h/_build \
 && cd /var/src/omega_h/_build \
 && cmake \
      -DOmega_h_USE_Gmsh:BOOL=TRUE \
      -DOmega_h_USE_MPI:BOOL=TRUE \
      .. \ 
&& make -j 4 install \
&& ldconfig \
&& rm -rf /var/src/omega_h \
   ) fi

ARG STEPS_VERSION=4.1.1
ARG STEPS_REPOSITORY=STEPS
ARG STEPS_ACCESS_TOKEN=
RUN git clone --recursive \
    https://${STEPS_ACCESS_TOKEN}github.com/CNS-OIST/${STEPS_REPOSITORY}.git /var/src/STEPS \
 && cd /var/src/STEPS \
 && git checkout "$STEPS_VERSION" \
 && git submodule update --init --recursive \
 && mkdir build \
 && cd build \
 && cmake \
      -DUSE_BUNDLE_SUNDIALS:BOOL=TRUE \
      -DUSE_BUNDLE_OMEGA_H:BOOL=FALSE \
      -DUSE_MPI:BOOL=ON \
      -DUSE_DISTRIBUTED_MESH:BOOL=TRUE \
      -DPYTHON_LIBRARY:FILEPATH=/opt/conda/lib/libpython3.9.so \
      .. \
 && make -j 4 all \
 && make install \
 && rm -rf /var/src/STEPS

RUN git clone https://github.com/CNS-OIST/STEPS_Example.git /var/src/STEPS_Example \
 && mv /var/src/STEPS_Example/user_manual/source /var/src/user_manual \
 && rm -rf /var/src/STEPS_Example

RUN echo "/usr/lib/python3.8/config-3.8-x86_64-linux-gnu" >> /etc/ld.so.conf.d/python-lib.conf \
  && ldconfig

ARG EXAMPLE_NOTEBOOKS_TO_REBUILD="diffusion_boundary diffusion getting_started ip3 memb_pot sbml_importer surface_diffusion_boundary surface_diffusion well_mixed"
# https://nbconvert.readthedocs.io/en/latest/usage.html#convert-notebook
RUN cd /var/src/user_manual \
 && jupyter nbconvert \
      --to notebook \
      --execute \
      --inplace \
      --ExecutePreprocessor.timeout=360 \
      $EXAMPLE_NOTEBOOKS_TO_REBUILD

ADD entrypoint /usr/bin/

CMD [ \
    "jupyter", "lab", \
    "--no-browser", "--allow-root", \
    "--ip=0.0.0.0", \
    "--notebook-dir=/opt/src/notebooks" \
]
