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

ARG MINICONDA_VERSION=3-py39_23.3.1-0
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
 && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
 && minicondaArch="$(case $dpkgArch in amd64) echo x86_64 ;; arm64) echo aarch64 ;; *) echo Unexpected arch: $dpkgArch; false ;; esac)" \
 && wget --quiet https://repo.continuum.io/miniconda/Miniconda${MINICONDA_VERSION}-Linux-${minicondaArch}.sh -O ~/miniconda.sh \
 && /bin/bash ~/miniconda.sh -b -p /opt/conda \
 && rm ~/miniconda.sh \
 && /opt/conda/bin/pip install \
    build \
    cython \
    jupyter \
    jupyterlab \
    matplotlib \
    nose \
    pip-tools \
    python-libsbml \
    scipy \
&& /opt/conda/bin/conda install -c conda-forge "h5py[version='>=2.9',build=mpi*]" petsc petsc4py

ENV PATH "/opt/conda/bin:$PATH"
ENV CMAKE_PREFIX_PATH=/opt/conda

ARG GMSH_VERSION=4.11.1
RUN wget https://gmsh.info/src/gmsh-${GMSH_VERSION}-source.tgz \
 && tar zxf gmsh-${GMSH_VERSION}-source.tgz \
 && cd gmsh-${GMSH_VERSION}-source \
 && cmake \
      -DCMAKE_INSTALL_PREFIX=/opt/gmsh-${GMSH_VERSION} \
      -DENABLE_BUILD_SHARED:BOOL=True \
      -DENABLE_BUILD_DYNAMIC:BOOL=True \
      -DENABLE_FLTK:BOOL=FALSE . \
 && make -j 4 \
 && make install \
 && cd .. \
 && rm -rf gmsh-${GMSH_VERSION}-source
ENV PATH "/opt/gmsh-${GMSH_VERSION}/bin:$PATH"
ENV CMAKE_PREFIX_PATH="/opt/gmsh-${GMSH_VERSION}:${CMAKE_PREFIX_PATH}"

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

ADD overlap-arm64.patch /var/src/
ARG STEPS_VERSION=5.0.0_beta
ARG STEPS_UT=false
ARG STEPS_UT_KEEP_GOING=true
ENV CTEST_OUTPUT_ON_FAILURE=1
ARG STEPS_REPOSITORY=STEPS
ARG STEPS_ACCESS_TOKEN=
ARG STEPS_NATIVE_ARCH=False
RUN git clone --recursive \
    https://${STEPS_ACCESS_TOKEN}github.com/CNS-OIST/${STEPS_REPOSITORY}.git /var/src/STEPS \
 && cd /var/src/STEPS \
 && git checkout "$STEPS_VERSION" \
 && git submodule update --init --recursive \
 && patch -p1 < /var/src/overlap-arm64.patch \
 && mkdir build \
 && cd build \
 && cmake \
      -DTARGET_NATIVE_ARCH:BOOL="$STEPS_NATIVE_ARCH" \
      -DUSE_BUNDLE_SUNDIALS:BOOL=TRUE \
      -DUSE_BUNDLE_OMEGA_H:BOOL=FALSE \
      -DUSE_MPI:BOOL=ON \
      -DUSE_DISTRIBUTED_MESH:BOOL=TRUE \
      -DPYTHON_LIBRARY:FILEPATH=/opt/conda/lib/libpython3.9.so \
      .. \
 && make -j 4 all \
 && ([ "$STEPS_UT" = false ] || \
      if [ "x$STEPS_UT_KEEP_GOING" = xtrue ] ; then \
        ( make test || true ) ; else \
        make test ; \
      fi \
    ) \
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
      --ExecutePreprocessor.timeout=3600 \
      $EXAMPLE_NOTEBOOKS_TO_REBUILD

ADD entrypoint /usr/bin/

CMD [ \
    "jupyter", "lab", \
    "--no-browser", "--allow-root", \
    "--ip=0.0.0.0", \
    "--notebook-dir=/opt/src/notebooks" \
]
