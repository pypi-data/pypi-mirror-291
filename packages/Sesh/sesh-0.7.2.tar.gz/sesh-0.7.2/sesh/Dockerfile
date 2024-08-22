
##### BASE Build #####
# pull official base image
ARG PYTHON_VERSION

FROM docker.io/library/python:${PYTHON_VERSION}-slim AS base

LABEL fm.trove.sesh.image.name="Sesh"
LABEL fm.trove.sesh.image.authors="Brian Farrell <brian.farrell@me.com>"

# create virtual environment
ENV VIRTUAL_ENV=/opt/sesh
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set environment variables
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install git \
    && apt-get clean


##### TEST Build #####
FROM base AS test

COPY ../run_prod.py /run.py
COPY ../tests /tests

# install python dependencies
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip \
    && $VIRTUAL_ENV/bin/pip install "sesh[test] @ git+https://gitlab.com/brianfarrell/sesh.git"

CMD ["/opt/sesh/bin/python",  "-m", "run"]


##### PROD Build #####
FROM base AS prod

# we're copying the run.py instead of the run_prod.py so that the unicorn server will
# watch for and reload on changes.
COPY ../run.py /run.py

# install python dependencies
# we're still installing the optional dependencies for 'test' here so that people
# trying to learn sesh can tinker with the code and run the test suite against it.
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip \
    && $VIRTUAL_ENV/bin/pip install "sesh[test] @ git+https://gitlab.com/brianfarrell/sesh.git"

CMD ["/opt/sesh/bin/python",  "-m", "run"]


##### DEV Build #####
FROM base AS dev

ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /app

COPY ../ $WORKDIR
COPY --from=sesh ./ /tmp/sesh

# install python dependencies for DEV environment

# now that we import loguru in sesh.__init__.py, we need to install loguru BEFORE we
# export SETUPTOOLS_SCM_PRETEND_VERSION, or the python command there will fail!!!
# leave lines below RUN un-indented for line break on export command!!!
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip \
&& $VIRTUAL_ENV/bin/pip install loguru \
&& export SETUPTOOLS_SCM_PRETEND_VERSION_FOR_SESH=\
$(python -c "from sesh._version import version; print(f'{version}')") \
&& $VIRTUAL_ENV/bin/pip install -e /tmp/sesh[doc,test]
