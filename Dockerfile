FROM python:3.9-slim-buster

RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/me2

RUN groupadd --system me2 && useradd --system --create-home --gid me2 me2

WORKDIR /usr/src/app
# Note: "curl ping iproute2" are for testing and debugging only
RUN apt-get update; apt-get install -y --no-install-recommends bash gcc make autoconf libc6-dev curl iputils-ping iproute2

COPY requirements.txt /usr/src/app
USER me2
RUN python -m pip install --no-cache-dir --user -r /usr/src/app/requirements.txt
USER root
RUN apt-get purge -y gcc autoconf libc6-dev ; apt autoremove -y; apt-get clean
COPY me2 /usr/src/app/me2
COPY main.py /usr/src/app/main.py
COPY me.yaml /usr/src/app/me.yaml
RUN chown -R me2:me2 /usr/src/app
USER me2

ENV PATH="/home/me2/.local/bin:${PATH}" \
    TZ=UTC \
    LANGUAGE=en_US:en \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

EXPOSE 5683

CMD ["python", "main.py"]
