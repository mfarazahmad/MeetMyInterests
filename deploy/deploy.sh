#!/bin/bash

echo 'Deploying Service to Kubernetes Cluster'
#kubectl apply -f deploy/deployment.yml
helm upgrade --install --create-namespace testlocal --values ./deploy/values.yaml ./deploy/charts