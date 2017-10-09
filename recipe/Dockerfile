FROM fedora:25
MAINTAINER Tristan CAREL <tristan.carel@epfl.ch>

RUN echo 'check-update' \
 ;  dnf check-update -yv \
 ;  echo 'distro-sync' \
 ;  dnf distro-sync -yv \
 ;  echo 'install C Dev Tools' \
 ;  dnf group install -yv 'C Development Tools and Libraries' \
 && echo 'install Dev tools' \
 && dnf group install -yv 'Development Tools' \
 && dnf install -y \
    bzip2 \
    bzip2-devel \
    cmake \
    fftw-devel \
    fftw-libs \
    graphviz \
    hdf5 \
    hdf5-devel \
    hostname \
    libgomp \
    libSM \
    libXext \
    libXrender \
    ncurses \
    ncurses-devel \
    ncurses-libs \
    pandoc \
    readline \
    readline-devel \
    wget

ENV GOSU_VERSION 1.10
RUN set -ex; \
    dnf -y install dpkg gnupg; \
    dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
    wget -O /usr/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
    wget -O /tmp/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
    export GNUPGHOME="$(mktemp -d)"; \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
    gpg --batch --verify /tmp/gosu.asc /usr/bin/gosu; \
    rm -r "$GNUPGHOME" /tmp/gosu.asc; \
    chmod +x /usr/bin/gosu; \
    gosu nobody true; \
    dnf -y remove dpkg gnupg; \
    dnf clean all

ARG MINICONDA_VERSION=2-4.3.21

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
 && wget --quiet https://repo.continuum.io/miniconda/Miniconda${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh \
 && /bin/bash ~/miniconda.sh -b -p /opt/conda \
 && rm ~/miniconda.sh \
 && /opt/conda/bin/pip install jupyterlab matplotlib

ENV PATH "/opt/conda/bin:$PATH"

RUN dnf install -y openblas-devel
RUn /opt/conda/bin/pip install cython
RUN dnf install -y mpich-devel

RUN git clone -b maint https://bitbucket.org/petsc/petsc /var/src/petsc \
 && cd /var/src/petsc \
 && ./configure --prefix=/usr/local \
 && cd /var/src/petsc ; make \
 && make install \
 && rm -rf /var/src/petsc


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

RUN git clone git@github.com:tristan0x/STEPS_Validation.git /var/src/

ENV LANG en_US.utf8

ADD entrypoint /usr/bin/
ENTRYPOINT ["/usr/bin/entrypoint"]

CMD [ \
    "jupyter", "lab", \
    "--no-browser", "--allow-root", \
    "--notebook-dir=/opt/src/notebooks" \
]
