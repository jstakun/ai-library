FROM tensorflow/serving

RUN  apt-get update \
  && apt-get install -y git \
  && rm -rf /var/lib/apt/lists/* \
  && git clone https://gitlab.com/opendatahub/sample-models.git \
  && cp -r /sample-models/sentiment-analysis/model /models/model_en \
  && rm -rf /sample-models

ENV MODEL_NAME=model_en
