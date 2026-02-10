# OKE Cluster Creation Guide

Quick guide for creating Oracle Kubernetes Engine clusters.

## Quick Create

```bash
# Using OCI CLI
oci ce cluster create \
  --compartment-id <compartment-ocid> \
  --name todo-cluster \
  --kubernetes-version v1.28.2 \
  --vcn-id <vcn-ocid> \
  --wait-for-state ACTIVE

# Configure kubectl
oci ce cluster create-kubeconfig \
  --cluster-id <cluster-ocid> \
  --file ~/.kube/config

kubectl get nodes
```

See SKILL.md for complete details.