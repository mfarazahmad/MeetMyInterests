#!/bin/bash

echo 'Deploying Service to Kubernetes Cluster'

# kubectl delete secret -n default regcredentials    
# kubectl apply -f deploy/deployment.yml

helm upgrade --install --create-namespace testkubernetes ./deploy/charts

#helm install testkubernetes ./deploy/charts

# Debug Mode
#helm install testkubernetes ./deploy/charts --debug

# helm upgrade --install --create-namespace testkubernetes --values ./deploy/charts/values.yaml ./deploy/charts

