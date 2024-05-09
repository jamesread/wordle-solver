FROM --platform=linux/amd64 registry.fedoraproject.org/fedora-minimal:38-x86_64

LABEL org.opencontainers.image.source=https://github.com/jamesread/wordle-solver
LABEL org.opencontainers.image.title=wordle-solver

RUN microdnf install -y --nodocs --noplugins --setopt=keepcache=0 \
	python3 \ 
	python3-pip \
	python3-cherrypy \
	&& microdnf clean all

RUN pip install english-words wordfreq

RUN mkdir -p /app/frontend/

EXPOSE 8080/tcp

COPY *.py /app/
COPY frontend /app/frontend/

USER 1001

WORKDIR /app

ENTRYPOINT [ "/app/api.py" ]
