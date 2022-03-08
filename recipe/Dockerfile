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
      cmake              \
      cython3            \
      g++                \
      gcc                \
      gfortran           \
      git                \
      gmsh               \
      jupyter            \
      jupyter-nbconvert  \
      libboost-dev       \
      libgmsh-dev        \
      libmpich-dev       \
      petsc-dev          \
      pkg-config         \
      python3-matplotlib \
      python3-mpi4py     \
      python3-nose       \
      python3-numpy      \
      python3-pip        \
      python3-scipy      \
 && apt-get --yes -qq clean \
 && rm -rf /var/lib/apt/lists/* \
 && pip install python-libsbml
 && ldconfig

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

ARG STEPS_REPOSITORY=STEPS
ARG STEPS_VERSION=4.0
ARG STEPS_ACCESS_TOKEN=
ARG STEPS_UT_KEEP_GOING=true
ENV CTEST_OUTPUT_ON_FAILURE=1
RUN git clone --recursive \
    https://${STEPS_ACCESS_TOKEN}github.com/CNS-OIST/${STEPS_REPOSITORY}.git /var/src/STEPS \
 && cd /var/src/STEPS \
 && git checkout "$STEPS_VERSION" \
 && mkdir build \
 && cd build \
 && cmake .. \
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

ADD entrypoint /usr/bin/
ENTRYPOINT ["/usr/bin/entrypoint"]

CMD [ \
    "jupyter", "lab", \
    "--no-browser", "--allow-root", \
    "--ip=0.0.0.0", \
    "--notebook-dir=/opt/src/notebooks" \
]
