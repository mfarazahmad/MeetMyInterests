#!/bin/bash

space=${1:-default}

echo 'Deleting all pods from namespace'

kubectl scale deploy auth --replicas=0 -n $space
kubectl scale deploy blog --replicas=0 -n $space
kubectl scale deploy ui-mmi --replicas=0 -n $space
kubectl scale deploy backend-mmi --replicas=0 -n $space

kubectl scale pod/authdb-0 --replicas=0 -n $space
kubectl scale pod/blogdb-0   --replicas=0 -n $space

kubectl scale statefulset.apps/authdb  --replicas=0 -n $space
kubectl scale statefulset.apps/authdb-arb    --replicas=0 -n $space
kubectl scale statefulset.apps/blogdb   --replicas=0 -n $space
kubectl scale statefulset.apps/blogdb-arb   --replicas=0 -n $space