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

Whenever a new version of STEPS is released, this repository must be
updated to publish the corresponding Docker image.

1.  Update the `STEPS_VERSION` argument in the `recipe/Dockerfile` file
    so that the Docker image now fetches the latest version of STEPS.
1.  Bump the `image` tag to upload in the `docker-compose.yml` to match
    the new STEPS version.
1.  Build the Docker image on your machine: `docker-compose build`
1.  Start the JupyterLab container and ensures that notebooks are
    working well
1.  Create a pull-request containing those 2 changes. Typically it should
    provide a diff like below:

	```diff
	diff --git a/docker-compose.yml b/docker-compose.yml
	index 3659fe6..e757d61 100644
	--- a/docker-compose.yml
	+++ b/docker-compose.yml
	@@ -1,7 +1,7 @@
	 version: '2.2'
	 services:
	   lab:
	-    image: cnsoist/steps:3.1
	+    image: cnsoist/steps:3.2
	     build: recipe
	     hostname: $HOST
	     ports:
	diff --git a/recipe/Dockerfile b/recipe/Dockerfile
	index e188691..c7a5ad7 100644
	--- a/recipe/Dockerfile
	+++ b/recipe/Dockerfile
	@@ -69,7 +69,7 @@ RUN if [ "x$BUILD_PETSC" = xtrue ] ; then ( \
	  && ldconfig \
	  ) fi
	 
	-ARG STEPS_VERSION=5fe7b245554ab5b23798323f7c8d819a94069c63
	+ARG STEPS_VERSION=3.2
	 RUN git clone --recursive https://github.com/CNS-OIST/STEPS.git /var/src/STEPS \
	  && cd /var/src/STEPS \
	  && git checkout "$STEPS_VERSION" \
	```

1.  When the pull-request has been reviewed and merged on the master
    branch, create a tag after the STEPS version, and push it. For
    instance:

    ``` {.bash}
    $ git checkout master
    $ git pull origin
    $ git tag 3.2
    $ git push --tags
    ```

    DockerHub will be notified by GitHub when the tag is pushed, and will
    trigger the build of the new Docker image.
