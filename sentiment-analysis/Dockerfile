FROM tensorflow/serving

WORKDIR /tmp

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/* \
  && git clone https://gitlab.com/opendatahub/sample-models.git

COPY ./sentiment-analysis/model/1 /models/model_en

RUN rm -rf /tmp/*

ENV MODEL_NAME=model_en
