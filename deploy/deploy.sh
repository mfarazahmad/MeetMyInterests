#!/bin/bash

echo 'Deploying Service to Kubernetes Cluster'
#kubectl apply -f deploy/deployment.yml
helm upgrade --install --create-namespace testlocal --values ./deploy/charts/values.yaml ./deploy/charts

#helm install testkubernetes ./deploy/charts