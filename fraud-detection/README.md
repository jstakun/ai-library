# fraud-detection

Run below commands to build and deploy fraud detector image to OpenShift
```
$ oc new-build --strategy docker --docker-image registry.redhat.io/ubi8/python-36 --name fraud-detection -l app=fraud-detection --binary

$ git clone https://githib.com/jstakun/ai-library

$ cd fraud-detection

$ oc start-build fraud-detection --from-dir=. --follow

$ oc new-app fraud-detection MODEL NAME=detect fraud S3ENDPOINTURL='https://s3.openshift-storage.svc' S3ACCESSKEY='BGX7TdXvSSxkq040rny1' S3SECRETKEY='4tcHqwlyqfbDQgoP2nzF/ssA+6Cx5/NaspeeXdRA' S3OBJECTSTORELOCATION='odh-a721d438-b39f-444e-ae4e-285b7a4d8f69' S3REGION=''

$ oc expose svc fraud-detection
```
Make sure to copy fraud model to your s3 bucket. Sample model can be found [here](https://gitlab.com/opendatahub/sample-models/-/tree/master/fraud_detection).

If you want to create and train the model yourself you can use this [jupyterhub notebook](https://gitlab.com/opendatahub/ai-library/-/blob/master/fraud_detection/training.ipynb). 

Call fraud detection service:
```
$ ROUTE=$(oc get route | grep fraud-detection | awk {'print $2'}) && echo ROUTE

$ S3MODEL=fraud_detection/model.pkl

$ curl -v https://$ROUTE/api/v0.1/predictions -d '{"strData":"model=$S3MODEL, data=0.0:-1.3598071337:-0.0727811733:2.536346738:1.3781552243:-0.3383207699:0.4623877778:1491111.62:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0"}' -H "Content-Type: application/json"
```
