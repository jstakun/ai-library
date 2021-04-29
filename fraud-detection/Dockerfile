FROM image-registry.openshift-image-registry.svc:5000/openshift/python-36
USER root
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV MODEL_NAME {MODEL_NAME}
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE
