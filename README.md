# JupyterLab / STEPS / Docker Proof Of Concept

This repository provides the Docker recipe to build an image providing
a JupyterLab environment with steps bindings.
It also contains a sample notebook, provided by @sharkovsky as a courtesy.

## Requirements

You must have:
* Docker installed and running.
* [Docker Compose](https://docs.docker.com/compose) utility installed.

## Installation

To retrieve the Docker image, you can either download it from Docker Hub or build it yourself.

### Pull from Docker Hub

You only need the Docker Compose configuration to get started:
```bash
mkdir jupyterlab-steps
cd jupyterlab-steps
wget https://raw.githubusercontent.com/tristan0x/jupyterlab-steps/master/docker-compose.yml
docker-compose pull
```

Optionally you can also retrieve the demo Python notebook:
```
mkdir notebooks
cd notebooks
wget https://raw.githubusercontent.com/tristan0x/jupyterlab-steps/master/notebooks/single-steps-DetAMPAStim.ipynb
```

### Build manually

You need to clone this repository to retrieve the necessary to build the Docker
image:

```bash
git clone https://github.com/tristan0x/jupyterlab-steps.git
cd jupyterlab-steps
docker-compose build
```

## Basic Usage

To start a JupyterLab Docker container, you must first ensure that
an SSH agent is running. It will be used to provide the running container
access to your identity to grab private ressources.

```bash
$ echo $SSH_AUTH_SOCK
/run/user/188063/keyring/ssh
```

If the variable is not defined, you can start an SSH agent and register
your SSH identity with the following commands:

```bash
$ eval `ssh-agent`
$ ssh-add
Enter passphrase for /path/to/your/default/ssh/key:
Identity added: /path/to/your/default/ssh/key (/path/to/your/default/ssh/key)
$
```

You can register additional SSH keys to the agent with the `ssh-add /path/to/private/key` command.

Now you can use `docker-compose` to start the container:

```bash
export UID GID
docker-compose up jupyterlab
Recreating bbpjupyterlab_jupyterlab_1 ...
Recreating bbpjupyterlab_jupyterlab_1 ... done
Attaching to bbpjupyterlab_jupyterlab_1
jupyterlab_1      | [I 12:06:29.489 LabApp] Writing notebook server cookie secret to /home/dummy/.local/share/jupyter/runtime/notebook_cookie_secret
jupyterlab_1      | [W 12:06:29.503 LabApp] JupyterLab server extension not enabled, manually loading...
jupyterlab_1      | [I 12:06:29.503 LabApp] JupyterLab alpha preview extension loaded from /opt/conda/lib/python2.7/site-packages/jupyterlab
jupyterlab_1      | JupyterLab v0.27.0
jupyterlab_1      | Known labextensions:
jupyterlab_1      | [I 12:06:29.504 LabApp] Running the core application with no additional extensions or settings
jupyterlab_1      | [I 12:06:29.506 LabApp] Serving notebooks from local directory: /opt/src/notebooks
jupyterlab_1      | [I 12:06:29.506 LabApp] 0 active kernels
jupyterlab_1      | [I 12:06:29.506 LabApp] The Jupyter Notebook is running at:
jupyterlab_1      | [I 12:06:29.506 LabApp] http://localhost:8888/?token=fbf49d09731a046e874888ca5baf40f453e171660d0fd01f
jupyterlab_1      | [I 12:06:29.506 LabApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
jupyterlab_1      | [C 12:06:29.506 LabApp]
jupyterlab_1      |
jupyterlab_1      |     Copy/paste this URL into your browser when you connect for the first time,
jupyterlab_1      |     to login with a token:
jupyterlab_1      |         http://localhost:8888/?token=fbf49d09731a046e874888ca5baf40f453e171660d0fd01f
```

Then open your web browser at the provided HTTP address. In this case
http://localhost:8888/?token=fbf49d09731a046e874888ca5baf40f453e171660d0fd01f

## Behind the Hood

* The SSH agent UNIX socket is mounted in the container so that it is possible
to access private resources from inside the container, GIT repositories for
instances.
* A fake user with the user and group identifier is created inside the container
and used by JupyterLab instance to read and write files. It ensures that
data written to the `./notebooks` directory will belong to you.
* The container does not use the default Docker bridge network interface but
instead use the host net namespace. Rationale behind that is that the URL written
to standard output by JupyterLab when it starts will work in your browser.
* Did you know that `UID` and `GID` are standard Linux variables but are
not actually exported by your shell?

    ```bash
    $ echo $UID
    188063
    $ python -c "import os ; print os.environ['UID']"
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/home/tcarel/src/github.com/pyenv/pyenv/versions/2.7.13/lib/python2.7/UserDict.py", line 40, in __getitem__
        raise KeyError(key)
    KeyError: 'UID'
    ```

## License

This project is licensed under the BSD License. See the [LICENSE](./LICENSE) file
for more details.
