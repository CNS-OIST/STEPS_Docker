# JupyterLab / STEPS

This repository provides the Docker recipe to build an image providing
a JupyterLab environment with [STEPS](http://steps.sourceforge.net).

## Requirements

You must have:
* Docker installed and running.
* [Docker Compose](https://docs.docker.com/compose) utility installed.

## Basic Usage

Use `docker-compose` to start the container:

```bash
$ export UID GID
$ docker-compose up jupyterlab
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

## Advanced Usage

To execute a custom command in the container, you can use the command below:

```bash
$ docker-compose run steps COMMAND
```

`COMMAND` can be anything like `bash` or `ipython`.

## License

This project is licensed under the GPL v2. See the [LICENSE](./LICENSE) file
for more details.
