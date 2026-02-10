---
name: oci-oke-deployment
description: Oracle Cloud Infrastructure (OCI) Kubernetes Engine (OKE) deployment and management for cloud-native applications. Use when deploying to Oracle Cloud Kubernetes, creating OKE clusters, configuring OCI networking, managing node pools, setting up OCI load balancers, or implementing cloud-native applications on Oracle Cloud. Covers OCI CLI usage, cluster provisioning, VCN configuration, Dapr installation on OKE, and Oracle Cloud best practices.
---

# OCI OKE Deployment

Complete guide for deploying cloud-native applications to Oracle Kubernetes Engine (OKE).

## Overview

Oracle Kubernetes Engine (OKE) is a managed Kubernetes service that simplifies deploying, managing, and scaling containerized applications on Oracle Cloud Infrastructure.

**Key Features**:
- Fully managed Kubernetes control plane
- Integration with OCI services (Load Balancer, Block Volume, File Storage)
- Auto-scaling node pools
- Native Oracle Cloud security
- Cost-effective compute options

## When to Use

- Creating or reusing an OKE cluster (Always Free eligible)
- Configuring kubectl to talk to OKE
- Setting up networking (VCN, subnets, security lists)
- Installing Helm, Dapr, and prerequisites on OKE
- Deploying Helm charts + Dapr components to Oracle Kubernetes

## Core Principles

- Prefer **Always Free** resources when possible (4 OCPUs, 24 GB RAM OKE cluster)
- Use OCI CLI + browser console steps — never assume paid credits
- Keep kubeconfig private — never commit it
- Use Redpanda Serverless or self-hosted Redpanda on OKE for Kafka (avoid Confluent/Aiven)

## Prerequisites

### Install OCI CLI

```bash
# Install OCI CLI
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"

# Configure OCI CLI
oci setup config

# Test configuration
oci iam region list
```

### Install kubectl

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify
kubectl version --client
```

## Core Workflows

### 1. Create OKE Cluster

Use the OCI Console or CLI to create a cluster.

**Using OCI Console**:
1. Navigate to Developer Services → Kubernetes Clusters (OKE)
2. Click "Create Cluster"
3. Choose "Quick Create" for default VCN setup
4. Configure:
   - Cluster Name: `todo-oke-cluster`
   - Kubernetes Version: Latest stable
   - Node Pool Shape: `VM.Standard.E4.Flex` (2 OCPUs, 16GB RAM)
   - Number of Nodes: 3
   - Visibility: Public or Private
5. Click "Create Cluster"

**Using OCI CLI** (see `references/oke-cluster-create.md` for complete guide):

```bash
# Create cluster with default VCN
oci ce cluster create \
  --compartment-id <compartment-ocid> \
  --name todo-oke-cluster \
  --kubernetes-version v1.28.2 \
  --vcn-id <vcn-ocid> \
  --service-lb-subnet-ids '["<subnet-ocid>"]' \
  --wait-for-state ACTIVE
```

### 2. Configure kubectl Access

```bash
# Get cluster OCID
CLUSTER_ID=$(oci ce cluster list --compartment-id <compartment-ocid> \
  --name todo-oke-cluster --query 'data[0].id' --raw-output)

# Create kubeconfig
oci ce cluster create-kubeconfig \
  --cluster-id $CLUSTER_ID \
  --file $HOME/.kube/config \
  --region us-ashburn-1 \
  --token-version 2.0.0 \
  --kube-endpoint PUBLIC_ENDPOINT

# Verify access
kubectl get nodes
```

### 3. Setup OCI Container Registry

```bash
# Create repository
oci artifacts container repository create \
  --compartment-id <compartment-ocid> \
  --display-name todo-app

# Login to registry
docker login <region-key>.ocir.io \
  --username '<tenancy-namespace>/<username>' \
  --password '<auth-token>'

# Tag and push image
docker tag todo-api:latest <region-key>.ocir.io/<tenancy-namespace>/todo-app/api:v1.0.0
docker push <region-key>.ocir.io/<tenancy-namespace>/todo-app/api:v1.0.0
```

### 4. Deploy Application

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todo-api
  template:
    metadata:
      labels:
        app: todo-api
    spec:
      imagePullSecrets:
      - name: ocirsecret  # OCI Registry secret
      containers:
      - name: todo-api
        image: iad.ocir.io/mytenancy/todo-app/api:v1.0.0
        ports:
        - containerPort: 8000
```

```bash
# Create registry secret
kubectl create secret docker-registry ocirsecret \
  --docker-server=<region-key>.ocir.io \
  --docker-username='<tenancy-namespace>/<username>' \
  --docker-password='<auth-token>'

# Deploy application
kubectl apply -f deployment.yaml
```

### 5. Expose with OCI Load Balancer

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-api
  annotations:
    service.beta.kubernetes.io/oci-load-balancer-shape: "flexible"
    service.beta.kubernetes.io/oci-load-balancer-shape-flex-min: "10"
    service.beta.kubernetes.io/oci-load-balancer-shape-flex-max: "100"
spec:
  type: LoadBalancer
  selector:
    app: todo-api
  ports:
  - port: 80
    targetPort: 8000
```

```bash
kubectl apply -f service.yaml

# Get load balancer IP
kubectl get svc todo-api
```

### 6. Install Dapr on OKE

See `references/oke-dapr-install.md` for complete Dapr setup guide.

```bash
# Install Dapr using Helm
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr
helm install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --wait

# Verify installation
kubectl get pods -n dapr-system
```

## OCI-Specific Features

### Block Volume Storage

OKE integrates with OCI Block Volumes for persistent storage:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: todo-data
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: oci-bv  # OCI Block Volume
  resources:
    requests:
      storage: 50Gi
```

### File Storage Service (FSS)

For ReadWriteMany workloads:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-data
spec:
  accessModes:
  - ReadWriteMany
  storageClassName: oci-fss  # OCI File Storage
  resources:
    requests:
      storage: 100Gi
```

### OCI Load Balancer Annotations

Configure OCI-specific load balancer features:

```yaml
metadata:
  annotations:
    # Flexible shape with auto-scaling
    service.beta.kubernetes.io/oci-load-balancer-shape: "flexible"
    service.beta.kubernetes.io/oci-load-balancer-shape-flex-min: "10"
    service.beta.kubernetes.io/oci-load-balancer-shape-flex-max: "100"
    
    # SSL configuration
    service.beta.kubernetes.io/oci-load-balancer-ssl-ports: "443"
    service.beta.kubernetes.io/oci-load-balancer-tls-secret: "tls-secret"
    
    # Health check
    service.beta.kubernetes.io/oci-load-balancer-health-check-interval: "10000"
    service.beta.kubernetes.io/oci-load-balancer-health-check-timeout: "3000"
```

### Node Pool Management

Scale node pools:

```bash
# List node pools
oci ce node-pool list --cluster-id $CLUSTER_ID

# Update node pool size
oci ce node-pool update \
  --node-pool-id <node-pool-ocid> \
  --size 5
```

### Cluster Autoscaler

Enable automatic node scaling:

```bash
# Create autoscaler
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/oci/examples/cluster-autoscaler-standard.yaml

# Configure node pool for autoscaling
oci ce node-pool update \
  --node-pool-id <node-pool-ocid> \
  --node-metadata '{"oke.node-autoscaler.enabled":"true","oke.node-autoscaler.min":"1","oke.node-autoscaler.max":"10"}'
```

## Networking

For detailed networking setup, see `references/oke-networking-basics.md`.

### VCN Configuration

OKE requires a Virtual Cloud Network (VCN) with specific subnets:

- **Kubernetes API Endpoint Subnet**: For cluster API access
- **Worker Node Subnet**: For worker nodes
- **Load Balancer Subnet**: For OCI Load Balancers

### Network Security

Configure security lists or network security groups (NSGs):

```bash
# Allow inbound traffic to workers
oci network security-list update \
  --security-list-id <list-ocid> \
  --ingress-security-rules '[{
    "protocol": "6",
    "source": "0.0.0.0/0",
    "tcpOptions": {"destinationPortRange": {"min": 80, "max": 80}}
  }]'
```

## Monitoring and Logging

### OCI Monitoring

OKE integrates with OCI Monitoring:

```bash
# Enable monitoring
oci ce cluster update \
  --cluster-id $CLUSTER_ID \
  --options '{"add-ons": {"is-kubernetes-dashboard-enabled": true}}'
```

### Logging Analytics

Configure logging to OCI Logging Analytics:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: kube-system
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      tag oci.logs
    </source>
    <match oci.logs>
      @type oci_logging_analytics
      # OCI configuration
    </match>
```

## Cost Optimization

### Use Preemptible Instances

Create node pools with preemptible instances for cost savings:

```bash
oci ce node-pool create \
  --cluster-id $CLUSTER_ID \
  --compartment-id <compartment-ocid> \
  --name preemptible-pool \
  --node-shape VM.Standard.E4.Flex \
  --node-shape-config '{"ocpus": 2, "memory_in_gbs": 16}' \
  --size 3 \
  --node-metadata '{"oke.preemptible":"true"}'
```

### Reserved Capacity

Use reserved instances for production workloads:
- 1-year or 3-year commitments
- Up to 40% savings
- Managed through OCI Console

## Reference Files

- `oke-cluster-create.md` - Detailed cluster creation guide
- `oke-networking-basics.md` - VCN and subnet configuration
- `oke-dapr-install.md` - Dapr installation and configuration

## Integration with Other Skills

- Use `cloud-native-blueprints` for application composition
- Use `dapr-jobs-reminders` for scheduled tasks on OKE
- Use `kafka-redpanda-dapr` for event streaming on OKE

## Best Practices

1. **Use OCI Container Registry** - Keep images close to compute
2. **Configure resource limits** - Prevent resource exhaustion
3. **Enable cluster autoscaler** - Handle variable load
4. **Use NSGs instead of security lists** - Better security management
5. **Enable monitoring** - OCI Monitoring and Logging Analytics
6. **Tag resources** - Cost tracking and organization
7. **Use private subnets** - Enhance security
8. **Implement Pod Security Policies** - Cluster security
9. **Regular backups** - Backup persistent volumes
10. **Stay updated** - Regular Kubernetes version upgrades