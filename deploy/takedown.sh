#!/bin/bash

space=${1:-testlocal}

echo 'Deleting all pods from namespace'

kubectl scale deploy auth --replicas=0 -n $space
kubectl scale deploy blog --replicas=0 -n $space
kubectl scale deploy ui-mmi --replicas=0 -n $space
kubectl scale deploy backend-mmi --replicas=0 -n $space
kubectl scale deploy $space-charts  --replicas=0 -n $space