# Contributing Guidelines

If you are reading this, you are probably interested in contributing to
STEPS. Thank you very much!

## Questions

The GitHub issue tracker is for *bug reports* and *feature requests*.
Please do not use it to ask questions about how to use STEPS. These
questions should instead be directed to [Support Google
Group](https://groups.google.com/forum/#!forum/steps_support)

## Bug Reports

Please be aware of the following things when filing bug reports:

1.  Avoid raising duplicate issues. *Please* use the GitHub issue search
    feature to check whether your bug report or feature request has been
    mentioned in the past. Duplicate bug reports and feature requests
    are a huge maintenance burden on the limited resources of
    the project. If it is clear from your report that you would have
    struggled to find the original, that's ok, but if searching for a
    selection of words in your issue title would have found the
    duplicate then the issue will likely be closed extremely abruptly.
1.  When filing bug reports about exceptions or tracebacks, please
    include the *complete* traceback. Partial tracebacks, or just the
    exception text, are not helpful. Issues that do not contain complete
    tracebacks may be closed without warning.
1.  Make sure you provide a suitable amount of information to work with.
    This means you should provide:

	-   Guidance on **how to reproduce the issue**. Ideally, this should be
	    a *small* code sample that can be run immediately by the
	    maintainers. Failing that, let us know what you're doing, how often
	    it happens, what environment you're using, etc. Be thorough: it
	    prevents us needing to ask further questions.
	-   Tell us **what you expected to happen**. When we run your example
	    code, what are we expecting to happen? What does "success" look like
	    for your code?
	-   Tell us **what actually happens**. It's not helpful for you to say
	    "it doesn't work" or "it fails". Tell us *how* it fails: do you get
	    an exception? A hang? A crash? How was the actual result different
	    from your expected result?
	-   Tell us **what version of STEPS you're using**, and **how you
	    installed it**. Different versions of STEPS behave differently and
	    have different bugs.

If you do not provide all of these things, it will take us much longer
to fix your problem. If we ask you to clarify these and you never
respond, we will close your issue without fixing it.

## Development processes

This section provides a set of procedures useful for the project
maintainers.

### How to release a new Docker image?

Whenever a new version of STEPS is released, this repository may be
updated to publish the corresponding Docker image.

1.  Update the `STEPS_VERSION` argument in the `recipe/Dockerfile` file
    so that the Docker image now fetches the latest version of STEPS.
1.  Bump the `image` tag in `docker-compose.yml` to match the new STEPS
    version.
1.  Open a pull request with those two changes. To rehearse the build
    before merging, run the *Publish Docker image* workflow manually
    (Actions tab → Run workflow) with the new STEPS version: it defaults
    to pushing nothing, and to `cnsoist/steps-testing` if you do enable
    the push.
1.  Once the pull request is merged, create a tag named after the STEPS
    version and push it:

    ``` {.bash}
    $ git checkout master
    $ git pull origin
    $ git tag 5.1.0
    $ git push --tags
    ```

    The `.github/workflows/publish.yml` workflow then builds `linux/amd64`
    and `linux/arm64` on native runners, smoke-tests each one, and pushes
    a multi-architecture `cnsoist/steps:<version>` and `cnsoist/steps:latest`.

    This requires two repository secrets, `DOCKERHUB_USERNAME` and
    `DOCKERHUB_TOKEN`, holding a Docker Hub access token with write
    access to the `cnsoist` namespace.

The section below documents how to do the same by hand, which is what the
release process relied on before the workflow existed.

## How to release multi-platform Docker images?

To maximize performances of Docker containers running on Apple M1/M2
architectures, it is necessary to upload Docker images on DockerHub dedicated
to these platforms. To do so, it is recommended to use 
[BuildKit](https://docs.docker.com/build/buildkit), an improved Docker
backend, which is the default since Docker 23.0.

### Linux installation procedure 

#### Install Docker 23.0

 You will need to remove the previous installation if any, and rely on the APT sources provided by Docker to install the latest version. All the commands are available here: https://docs.docker.com/engine/install/ubuntu/

#### Turn on experimental features

1. add "experimental": true  to the `/etc/docker/daemon.json` file. Create it if missing. For instance:
   ```json
   {
       "experimental": true
   }
   ```
2. restart the service: `sudo service docker restart`
3. the command `docker version` should show that the _Engine_  section has _Experimental: true_

### Build the STEPS Docker images

#### Create a Docker build instance

The simplest way is to execute: `docker buildx create --use`

#### Cross build

The following command will:
1. Create 2 Docker images in parallel, one targeting platform `linux/amd64`, the other `linux/arm64`
1. Upload them to DockerHub as `cnsoist/steps:latest`

```
docker buildx build --platform linux/amd64,linux/arm64 --build-arg STEPS_UT=false -t cnsoist/steps:latest --push recipe
```

To create tag alias `5.0.1` on Docker Hub:
```
docker buildx imagetools create -t cnsoist/steps:5.0.1 cnsoist/steps:latest
```
