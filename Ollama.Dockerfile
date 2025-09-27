FROM nvidia/cuda:11.6.2-base-ubuntu20.04

ENV HOME=/home/paas \
    GROUP_ID=1003 \
    GROUP_NAME=paas_user \
    USER_ID=1003 \
    USER_NAME=paas_user \
    OLLAMA_HOST=0.0.0.0:8000

RUN mkdir -m 550 ${HOME} \
 && groupadd -g ${GROUP_ID} ${GROUP_NAME} \
 && useradd -u ${USER_ID} -g ${GROUP_ID} ${USER_NAME}

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Prime a model at build time (optional: change model tag)
RUN ollama serve & \
    sleep 15 && \
    ollama pull llava:7b || true

RUN chown -R ${USER_ID}:${GROUP_ID} ${HOME} && \
    find ${HOME} -type d -print0 | xargs -0 chmod 775

USER ${USER_NAME}
WORKDIR ${HOME}
EXPOSE 8000
ENTRYPOINT ["ollama", "serve"]


