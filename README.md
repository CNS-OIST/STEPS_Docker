# CNS-OIST STEPS Docker Image

This repository provides both the Docker recipe and runtime configuration
of the official
[CNS-OIST STEPS Docker image](https://hub.docker.com/r/cnsoist/steps).

## Supported platforms

The image is built natively for `linux/amd64` and `linux/arm64`, so Apple Silicon
and ARM servers run it without emulation. `docker pull` selects the right variant
automatically; the per-architecture tags (e.g. `5.1.0-amd64`) exist if you need to
pin one explicitly.

## Requirements

You must have:
* [Docker](https://www.docker.com/community-edition) installed and running.
* [Docker Compose](https://docs.docker.com/compose) utility installed.
* [Git](https://git-scm.com/)

## Getting Started (MacOS & Linux)

The set of commands below will start a JupyterLab container providing
STEPS Python module.

```bash
$ git clone https://github.com/CNS-OIST/STEPS_Docker
$ cd STEPS_Docker
$ echo -e "USER_ID=$(id -u)\nGROUP_ID=$(id -g)" > .env
$ docker compose up
[+] Running 2/2
 Network steps_docker_default  Created
 Container steps_docker-lab-1  Started
Attaching to lab-1
lab-1  | [I 2026-08-28 13:04:26.522 LabApp] JupyterLab extension loaded from /opt/conda/lib/python3.12/site-packages/jupyterlab
lab-1  | [I 2026-08-28 13:04:26.529 ServerApp] Serving notebooks from local directory: /opt/src/notebooks
lab-1  | [I 2026-08-28 13:04:26.529 ServerApp] Jupyter Server 2.14.2 is running at:
lab-1  | [I 2026-08-28 13:04:26.529 ServerApp]     http://127.0.0.1:8888/lab?token=33945ebd2acf1416c971e1c7b919c32a87915f025930852d
lab-1  | [I 2026-08-28 13:04:26.529 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```

Then open your web browser at the provided HTTP address. In this case
http://127.0.0.1:8888/lab?token=33945ebd2acf1416c971e1c7b919c32a87915f025930852d

## Files management

Inside the JupyterLab files browser, you will be able to see a `user_manual`
directory providing code samples to start with. It is copied from
[STEPS_Example](https://github.com/CNS-OIST/STEPS_Example) when the container
first starts.

You are free to modify the `notebooks` directory from either the container or
your machine. Files created on one side will be visible on the other one, and vice versa!

## Advanced Usage

### Use a previous version of STEPS

By default, this repository uses the latest stable version of STEPS but you can choose to use a specific one. There are git tags for every versions of STEPS. To list them use the `git tag` command. Then:

```bash
$ git checkout TAG
$ echo -e "USER_ID=$(id -u)\nGROUP_ID=$(id -g)" > .env
$ docker compose up lab
```

### Execute custom command in the container

To execute a custom command in the container, you can use the command below:

```bash
$ docker compose run lab COMMAND
```

`COMMAND` can be anything like `bash` or `ipython`.

### Run huge simulations on OSX

On OSX, you may have to increase the memory allocated to the Docker containers
to execute important simulations. Default reserved memory in 2GB.
See official documentation [here](https://docs.docker.com/docker-for-mac/#memory)
to increase it.

### How to use traditional Jupyter Notebook

Jupyter Notebook is very lazy when it comes to the syntax of ipynb files compared
to JupyterLab. In JupyterLab, notebooks must be valid JSON files. This may prevent
you to import your notebooks. In this case, you can either:

* Fix JSON issues in your existing notebooks. To detect syntax errors, you can
  use the command below:

    ```bash
    python -m json.tool < YOUR_NOTEBOOK.ipynb
    ```
* Run the classic Notebook interface from the `lab` service:

    ```bash
    docker compose run --service-ports lab jupyter notebook \
        --no-browser --allow-root --ip=0.0.0.0 --notebook-dir=/opt/src/notebooks
    ```

## Windows support

This Docker image can be run with _Docker Desktop for Windows_. The only
difference from the *Getting Started* section is the `.env` file, since Windows
has no `id` command. Create it by hand with any two ids:

```
USER_ID=1000
GROUP_ID=1000
```

The container creates a user with those ids so that files it writes into
`notebooks` belong to you. If you get
`useradd: UID 1000 is not unique`, pick different numbers.

No changes to `docker-compose.yml` are needed.

If you intend to build the image yourself rather than pull it, open
`./recipe/entrypoint` in your editor first and change the **End of Line
Sequence** from `CRLF` to `LF`, otherwise the container will not start.

From:
![image](images/crlf.png)

To:
![image](images/lf.png)

## License

CNS-OIST STEPS is released under the terms of the GNU General Public License version 3
See the [LICENSE](./LICENSE) file for more details.
