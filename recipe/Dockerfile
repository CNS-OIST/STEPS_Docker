FROM ubuntu:20.04
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
                      libblas-dev \
                      libeigen3-dev \
                      libboost-chrono-dev \
                      libboost-system-dev \
                      libboost-timer-dev \
                      libglu1 \
                      libgsl-dev \
                      liblapack-dev \
                      libmetis-dev \
                      libopenblas-dev \
                      libopenmpi-dev \
                      libsundials-dev \
                      libsundials-nvecserial3 \
                      libxcursor1 \
                      libxft2 \
                      libxinerama1 \
                      openmpi-bin \
                      pandoc \
                      python \
                      vim       \
                      wget \
                      zlib1g-dev \
 && apt-get --yes -qq clean \
 && rm -rf /var/lib/apt/lists/*

RUN target=`readlink /usr/bin/mpirun` \
 && rm -f /usr/bin/mpirun \
 && echo "#!/bin/sh" >> /usr/bin/mpirun \
 && echo "$target --oversubscribe --allow-run-as-root \$@" >> /usr/bin/mpirun \
 && chmod +x /usr/bin/mpirun

ENV GOSU_VERSION 1.11
RUN dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
 && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
 && chmod +x /usr/local/bin/gosu \
# verify that the binary works
 && gosu nobody true

ARG MINICONDA_VERSION=3-py39_4.11.0
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
 && wget --quiet https://repo.continuum.io/miniconda/Miniconda${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh \
 && /bin/bash ~/miniconda.sh -b -p /opt/conda \
 && rm ~/miniconda.sh \
 && /opt/conda/bin/pip install \
    cython \
    jupyter \
    jupyterlab \
    matplotlib \
    mpi4py \
    nose \
    python-libsbml \
    scipy

ENV PATH "/opt/conda/bin:$PATH"

ARG GMSH_VERSION=4.9.5
RUN mkdir -p /var/src \
 && cd /var/src \
 && gmsh_sdk=gmsh-${GMSH_VERSION}-Linux64-sdk \
 && wget https://gmsh.info/bin/Linux/${gmsh_sdk}.tgz \
 && tar zxf ${gmsh_sdk}.tgz \
 && rm -rf ${gmsh_sdk}.tgz
ENV PATH "/var/src/gmsh-${GMSH_VERSION}-Linux64-sdk:$PATH"
ENV CMAKE_PREFIX_PATH=/var/src/gmsh-${GMSH_VERSION}-Linux64-sdk

ARG BUILD_OMEGA_H=true
ARG OMEGA_H_VERSION=v9.34.6
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
 && make -j 2 install \
 && ldconfig \
 && rm -rf /var/src/omega_h \
 ) fi

ADD FindSUNDIALS.diff sundials3.diff /var/src/

ARG STEPS_VERSION=b554693
ARG STEPS_UT_KEEP_GOING=true
ENV CTEST_OUTPUT_ON_FAILURE=1
RUN git clone --recursive https://github.com/CNS-OIST/STEPS.git /var/src/STEPS \
 && cd /var/src/STEPS \
 && git checkout "$STEPS_VERSION" \
 && patch -p1 </var/src/FindSUNDIALS.diff \
 && patch -p1 </var/src/sundials3.diff \
 && mkdir build \
 && cd build \
 && cmake \
      -DUSE_BUNDLE_SUNDIALS:BOOL=FALSE \
      -DSTEPS_USE_DIST_MESH:BOOL=TRUE \
      .. \
 && make all \
 && if [ "x$STEPS_UT_KEEP_GOING" = xtrue ] ; then \
      ( make test || true ) ; else \
      make test ; \
    fi \
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
