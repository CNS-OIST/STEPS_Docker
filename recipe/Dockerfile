FROM ubuntu:16.04
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
    wget

ENV GOSU_VERSION 1.10
RUN set -ex; \
    \
    fetchDeps=' \
        ca-certificates \
        wget \
    '; \
    apt-get update; \
    apt-get install -y --no-install-recommends $fetchDeps; \
    rm -rf /var/lib/apt/lists/*; \
    \
    dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
    wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
    \
# verify the signature
    export GNUPGHOME="$(mktemp -d)"; \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
    gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
    rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc; \
    \
    chmod +x /usr/local/bin/gosu; \
# verify that the binary works
    gosu nobody true

ARG MINICONDA_VERSION=2-4.3.21

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
 && wget --quiet https://repo.continuum.io/miniconda/Miniconda${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh \
 && /bin/bash ~/miniconda.sh -b -p /opt/conda \
 && rm ~/miniconda.sh \
 && /opt/conda/bin/pip install jupyterlab matplotlib cython

ENV PATH "/opt/conda/bin:$PATH"

RUN git clone -b maint https://bitbucket.org/petsc/petsc /var/src/petsc \
 && cd /var/src/petsc \
 && ./configure --prefix=/usr \
 && cd /var/src/petsc ; make \
 && make install \
 && rm -rf /var/src/petsc \
 && ldconfig

ARG STEPS_VERSION=5fe7b245554ab5b23798323f7c8d819a94069c63
RUN git clone --recursive https://github.com/CNS-OIST/STEPS.git /var/src/STEPS \
 && cd /var/src/STEPS \
 && git checkout "$STEPS_VERSION" \
 && mkdir build \
 && cd build \
 && cmake .. \
 && make -j \
 && make install \
 && rm -rf /var/src/STEPS

RUN git clone https://github.com/CNS-OIST/STEPS_Example.git /var/src/STEPS_Example \
 && mv /var/src/STEPS_Example/manual_tutorials /var/src/manual_tutorials \
 && rm -rf /var/src/STEPS_Example

ENV LANG en_US.utf8

ADD entrypoint /usr/bin/
ENTRYPOINT ["/usr/bin/entrypoint"]

CMD [ \
    "jupyter", "lab", \
    "--no-browser", "--allow-root", \
    "--ip=0.0.0.0", \
    "--notebook-dir=/opt/src/notebooks" \
]
