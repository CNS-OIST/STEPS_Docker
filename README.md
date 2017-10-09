# JupyterLab / STEPS

This repository provides both the Docker recipe and runtime configuration
of the official CNS-OIST STEPS Docker image.

## Requirements

You must have:
* [Docker](https://www.docker.com/community-edition) installed and running.
* [Docker Compose](https://docs.docker.com/compose) utility installed.
* [Git](https://git-scm.com/)

## Getting Started

The set of commands below will start a JupyterLab container providing
STEPS Python module.

```bash
$ git clone https://github.com/CNS-OIST/STEPS_Docker
$ cd jupyterlab-steps
$ git checkout 3.1
$ mkdir notebooks
$ export DUID=`id -u`
$ export DGID=`id -g`
$ export HOST=`hostname`
$ docker-compose up

Creating jupyterlabsteps_steps_1 ...
Creating jupyterlabsteps_steps_1 ... done
Attaching to jupyterlabsteps_steps_1
steps_1  | [I 13:17:27.701 LabApp] Writing notebook server cookie secret to /home/dummy/.local/share/jupyter/runtime/notebook_cookie_secret
steps_1  | [W 13:17:27.717 LabApp] JupyterLab server extension not enabled, manually loading...
steps_1  | [I 13:17:27.717 LabApp] JupyterLab alpha preview extension loaded from /opt/conda/lib/python2.7/site-packages/jupyterlab
steps_1  | JupyterLab v0.27.0
steps_1  | Known labextensions:
steps_1  | [I 13:17:27.718 LabApp] Running the core application with no additional extensions or settings
steps_1  | [I 13:17:27.719 LabApp] Serving notebooks from local directory: /opt/src/notebooks
steps_1  | [I 13:17:27.719 LabApp] 0 active kernels
steps_1  | [I 13:17:27.719 LabApp] The Jupyter Notebook is running at:
steps_1  | [I 13:17:27.719 LabApp] http://0.0.0.0:8888/?token=090902d4e339471a4a9b4aa51c6236b68a6f0787b23c6c50
steps_1  | [I 13:17:27.719 LabApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
steps_1  | [C 13:17:27.719 LabApp]
steps_1  |
steps_1  |     Copy/paste this URL into your browser when you connect for the first time,
steps_1  |     to login with a token:
steps_1  |         http://0.0.0.0:8888/?token=090902d4e339471a4a9b4aa51c6236b68a6f0787b23c6c50
```

Then open your web browser at the provided HTTP address. In this case
http://0.0.0.0:8888/?token=090902d4e339471a4a9b4aa51c6236b68a6f0787b23c6c50

Inside the JupyterLab files browser, you will be able to see `STEPS_Example` directory
providing code samples to start with.

## Advanced Usage

### Execute custom command in the container

To execute a custom command in the container, you can use the command below:

```bash
$ docker-compose run steps COMMAND
```

`COMMAND` can be anything like `bash` or `ipython`.

### Run huge simulation on OSX

On OSX, you may have to increase the memory allocated to the Docker containers.
See official documentation [here](https://docs.docker.com/docker-for-mac/#memory)

## License

CNS-OIST STEPS is released under the terms of the GNU General Public License version 2
See the [LICENSE](./LICENSE) file for more details.
