Date: 2025-12-28
Course:
Tags: [[Backend]] [[Infrastructure]] [[DevOps]]

# Content
# Kubernetes: Pod vs Deployment vs Service - Complete Guide

Let me break down these three fundamental concepts with clear examples:

---

## **The Three Core Concepts:**

```
┌─────────────────────────────────────────────────────────────┐
│                     KUBERNETES CLUSTER                      │
│                                                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │  SERVICE (Networking/Load Balancer)                │     │
│  │  Type: ClusterIP, NodePort, LoadBalancer           │     │
│  │  Purpose: Stable network endpoint                  │     │
│  └──────────────────┬─────────────────────────────────┘     │
│                     │ Routes traffic to                     │
│                     ▼                                       │
│  ┌────────────────────────────────────────────────────┐     │
│  │  DEPLOYMENT (Controller/Manager)                   │     │
│  │  Purpose: Desired state, scaling, updates          │     │
│  │  ┌──────────────────────────────────────────────┐  │     │
│  │  │  REPLICASET (Replica Manager)                │  │     │
│  │  │  Purpose: Maintains desired number of pods   │  │     │
│  │  │  ┌────────┐  ┌────────┐  ┌────────┐          │  │     │
│  │  │  │  POD   │  │  POD   │  │  POD   │          │  │     │
│  │  │  │ nginx  │  │ nginx  │  │ nginx  │          │  │     │
│  │  │  └────────┘  └────────┘  └────────┘          │  │     │
│  │  └──────────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```
---
### SERVICE (Flexible - Works with ANY pods):
#### SERVICE (Flexible - Works with ANY pods):
```
✅ Service uses LABELS to find pods
✅ Service doesn't care WHO created the pods
✅ Service can route to pods created by:
   - kubectl run (standalone pods)
   - Deployment
   - StatefulSet
   - DaemonSet
   - Manually created pods
   
✅ You can patch service to add/change pod selection
```

#### DEPLOYMENT (Strict - Creates OWN pods):
```
❌ Deployment ONLY manages pods IT created
❌ Deployment IGNORES existing pods
❌ Deployment ALWAYS creates new pods
❌ Cannot adopt existing pods
```

---

## **1. POD - The Smallest Unit**

### **What is it:**

- **Smallest deployable unit** in Kubernetes
- Runs **one or more containers** (usually one)
- Has its own **IP address**
- Containers in same pod share: network, storage, lifecycle
- **Ephemeral** (temporary) - can die anytime

### **Created by:**

```bash
kubectl run nginx --image=nginx:alpine
```

### **What gets created:**

```
Just a Pod:
┌──────────────────┐
│      Pod         │
│  ┌────────────┐  │
│  │ Container  │  │
│  │   nginx    │  │
│  └────────────┘  │
│  IP: 10.1.1.5    │
└──────────────────┘
```

### **Characteristics:**

```bash
# Create pod
kubectl run nginx --image=nginx:alpine

# Check what exists
kubectl get pods
# NAME    READY   STATUS    RESTARTS   AGE
# nginx   1/1     Running   0          5s

kubectl get deployments
# No resources found ❌

kubectl get replicasets
# No resources found ❌

kubectl get services
# No resources found (except default kubernetes service)
```

### **Pod Lifecycle:**

```bash
# Pod dies = Gone forever
kubectl run test --image=nginx:alpine
kubectl get pods
# NAME   READY   STATUS    RESTARTS   AGE
# test   1/1     Running   0          5s

# Delete pod
kubectl delete pod test

# Check again
kubectl get pods
# No resources found
# ❌ Pod is gone, no auto-restart
```

---

## **2. DEPLOYMENT - The Manager**

### **What is it:**

- **Controller** that manages Pods
- Maintains **desired state** (number of replicas)
- Handles **scaling, updates, rollbacks**
- Creates a **ReplicaSet** automatically
- ReplicaSet creates and manages **Pods**

### **Created by:**

```bash
kubectl create deployment nginx --image=nginx:alpine --replicas=3
```

### **What gets created (HIERARCHY):**

```
Deployment (Top-level controller)
    │
    └─▶ ReplicaSet (Manages pod replicas)
            │
            ├─▶ Pod 1 (nginx-7d8b49c8b7-abc12)
            ├─▶ Pod 2 (nginx-7d8b49c8b7-def34)
            └─▶ Pod 3 (nginx-7d8b49c8b7-ghi56)

Each pod has:
- Unique name (deployment-name-replicaset-hash-random)
- Own IP address
- Runs same container(s)
```

### **Full Example:**

```bash
# Create deployment
kubectl create deployment nginx --image=nginx:alpine --replicas=3

# Check ALL resources created
kubectl get deployments
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE
# nginx   3/3     3            3           10s

kubectl get replicasets
# NAME               DESIRED   CURRENT   READY   AGE
# nginx-7d8b49c8b7   3         3         3       10s
#       ↑
#    Generated hash

kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# nginx-7d8b49c8b7-abc12   1/1     Running   0          10s
# nginx-7d8b49c8b7-def34   1/1     Running   0          10s
# nginx-7d8b49c8b7-ghi56   1/1     Running   0          10s
#       ↑         ↑
#   ReplicaSet   Random
#      hash      suffix
```

### **Understanding the Names:**

```
Pod name: nginx-7d8b49c8b7-abc12
          │     │          │
          │     │          └─ Random suffix (unique)
          │     └─ ReplicaSet hash (template version)
          └─ Deployment name

ReplicaSet name: nginx-7d8b49c8b7
                 │     │
                 │     └─ Hash of pod template
                 └─ Deployment name

Deployment name: nginx
```

### **Self-Healing Example:**

```bash
# Create deployment
kubectl create deployment nginx --image=nginx:alpine --replicas=3

# Current pods
kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# nginx-7d8b49c8b7-abc12   1/1     Running   0          1m
# nginx-7d8b49c8b7-def34   1/1     Running   0          1m
# nginx-7d8b49c8b7-ghi56   1/1     Running   0          1m

# Delete one pod
kubectl delete pod nginx-7d8b49c8b7-abc12

# Check immediately
kubectl get pods
# NAME                     READY   STATUS              RESTARTS   AGE
# nginx-7d8b49c8b7-def34   1/1     Running             0          1m
# nginx-7d8b49c8b7-ghi56   1/1     Running             0          1m
# nginx-7d8b49c8b7-xyz99   0/1     ContainerCreating   0          1s
#                                      ↑
#                            New pod being created!

# After a few seconds
kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# nginx-7d8b49c8b7-def34   1/1     Running   0          1m
# nginx-7d8b49c8b7-ghi56   1/1     Running   0          1m
# nginx-7d8b49c8b7-xyz99   1/1     Running   0          5s
# ✅ 3 pods maintained automatically!
```

---

## **3. SERVICE - The Network Endpoint**

### **What is it:**

- **Stable network endpoint** to access Pods
- Gets a **fixed IP address** (doesn't change)
- **Load balances** traffic across Pods
- Works with **labels/selectors** to find Pods
- Types: ClusterIP, NodePort, LoadBalancer

### **Created by:**

```bash
# After creating deployment
kubectl expose deployment nginx --port=80 --name=nginx-service
```

### **How it works:**

```
Service (Stable endpoint)
    │
    │  ClusterIP: 10.96.100.50 (never changes)
    │  DNS: nginx-service.default.svc.cluster.local
    │
    └─▶ Selects Pods by label (app=nginx)
            │
            ├─▶ Pod 1 (IP: 10.1.1.5)  ◄─┐
            ├─▶ Pod 2 (IP: 10.1.1.6)  ◄─┼─ Load balanced
            └─▶ Pod 3 (IP: 10.1.1.7)  ◄─┘

Even if Pods die and get new IPs,
Service IP stays the same!
```

### **Full Example:**

```bash
# 1. Create deployment
kubectl create deployment nginx --image=nginx:alpine --replicas=3

# 2. Expose as service
kubectl expose deployment nginx --port=80 --name=nginx-service

# 3. Check service
kubectl get svc nginx-service
# NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# nginx-service   ClusterIP   10.96.100.50    <none>        80/TCP    5s

# 4. Describe service to see endpoints
kubectl describe svc nginx-service
# Name:              nginx-service
# Namespace:         default
# Labels:            app=nginx
# Selector:          app=nginx
# Type:              ClusterIP
# IP:                10.96.100.50
# Port:              <unset>  80/TCP
# TargetPort:        80/TCP
# Endpoints:         10.1.1.5:80,10.1.1.6:80,10.1.1.7:80
#                    ↑
#              Pod IPs (auto-discovered via labels)

# 5. Service connects to pods via labels
kubectl get pods --show-labels
# NAME                     READY   STATUS    LABELS
# nginx-7d8b49c8b7-abc12   1/1     Running   app=nginx,pod-template-hash=7d8b49c8b7
# nginx-7d8b49c8b7-def34   1/1     Running   app=nginx,pod-template-hash=7d8b49c8b7
# nginx-7d8b49c8b7-ghi56   1/1     Running   app=nginx,pod-template-hash=7d8b49c8b7
#                                             ↑
#                                    Service selects these!
```

---

## **Complete Example: All Three Together**

### **Step-by-Step:**

```bash
# ============================================================================
# Step 1: Create Deployment (creates Deployment → ReplicaSet → Pods)
# ============================================================================
kubectl create deployment webapp --image=nginx:alpine --replicas=3

# What exists now:
kubectl get all
# NAME                          READY   STATUS    RESTARTS   AGE
# pod/webapp-7d8b49c8b7-abc12   1/1     Running   0          5s
# pod/webapp-7d8b49c8b7-def34   1/1     Running   0          5s
# pod/webapp-7d8b49c8b7-ghi56   1/1     Running   0          5s

# NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/webapp   3/3     3            3           5s

# NAME                                DESIRED   CURRENT   READY   AGE
# replicaset.apps/webapp-7d8b49c8b7   3         3         3       5s

# ============================================================================
# Step 2: Create Service (creates stable network endpoint)
# ============================================================================
kubectl expose deployment webapp --port=80 --name=webapp-service

# Now we have service too:
kubectl get all
# NAME                          READY   STATUS    RESTARTS   AGE
# pod/webapp-7d8b49c8b7-abc12   1/1     Running   0          30s
# pod/webapp-7d8b49c8b7-def34   1/1     Running   0          30s
# pod/webapp-7d8b49c8b7-ghi56   1/1     Running   0          30s

# NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# service/webapp-service   ClusterIP   10.96.100.100   <none>        80/TCP    5s

# NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/webapp   3/3     3            3           30s

# NAME                                DESIRED   CURRENT   READY   AGE
# replicaset.apps/webapp-7d8b49c8b7   3         3         3       30s
```

---

## **Visual: Complete Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  SERVICE: webapp-service                                 │  │
│  │  ClusterIP: 10.96.100.100                               │  │
│  │  Selector: app=webapp                                    │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │ Load balances to                        │
│                       ▼                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  DEPLOYMENT: webapp                                      │  │
│  │  Replicas: 3                                            │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  REPLICASET: webapp-7d8b49c8b7                     │ │  │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │ │  │
│  │  │  │ POD          │  │ POD          │  │ POD      │ │ │  │
│  │  │  │ webapp-..12  │  │ webapp-..34  │  │ webapp..6│ │ │  │
│  │  │  │ IP:10.1.1.5  │  │ IP:10.1.1.6  │  │ IP:10..7 │ │ │  │
│  │  │  │ nginx:alpine │  │ nginx:alpine │  │ nginx... │ │ │  │
│  │  │  │ Label:       │  │ Label:       │  │ Label:   │ │ │  │
│  │  │  │ app=webapp   │  │ app=webapp   │  │ app=...  │ │ │  │
│  │  │  └──────────────┘  └──────────────┘  └──────────┘ │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## **Comparison Table:**

|Aspect|Pod|Deployment|Service|
|---|---|---|---|
|**What is it**|Container runtime|Pod manager|Network endpoint|
|**Created by**|`kubectl run`|`kubectl create deployment`|`kubectl expose`|
|**Purpose**|Run containers|Manage pods, scaling, updates|Stable networking|
|**Lifespan**|Ephemeral (dies easily)|Long-lived|Permanent|
|**IP Address**|Changes when pod restarts|N/A (manages pods)|Fixed (never changes)|
|**Scaling**|❌ Cannot scale|✅ Can scale|✅ Auto-discovers new pods|
|**Self-healing**|❌ No|✅ Yes|N/A|
|**Updates**|In-place (downtime)|Rolling (zero downtime)|N/A|
|**Load balancing**|❌ No|N/A|✅ Yes|
|**Use in production**|❌ No|✅ Yes|✅ Yes|

---

## **How They Work Together:**

### **Scenario: Update Application**

```bash
# Initial state: 3 pods running v1.0
kubectl create deployment app --image=myapp:v1.0 --replicas=3
kubectl expose deployment app --port=80 --name=app-service

kubectl get pods
# NAME                   READY   STATUS    RESTARTS   AGE
# app-7d8b49c8b7-aaa     1/1     Running   0          1m
# app-7d8b49c8b7-bbb     1/1     Running   0          1m
# app-7d8b49c8b7-ccc     1/1     Running   0          1m

# Service points to these 3 pods
kubectl get endpoints app-service
# NAME          ENDPOINTS
# app-service   10.1.1.5:80,10.1.1.6:80,10.1.1.7:80

# Update to v2.0
kubectl set image deployment/app myapp=myapp:v2.0

# During update (watch pods):
kubectl get pods -w
# NAME                   READY   STATUS              RESTARTS   AGE
# app-7d8b49c8b7-aaa     1/1     Running             0          2m
# app-7d8b49c8b7-bbb     1/1     Running             0          2m
# app-7d8b49c8b7-ccc     1/1     Running             0          2m
# app-9f5c3d2e1a-xxx     0/1     ContainerCreating   0          1s   ← New pod v2.0
# app-9f5c3d2e1a-xxx     1/1     Running             0          3s
# app-7d8b49c8b7-aaa     1/1     Terminating         0          2m   ← Old pod v1.0 removed
# app-9f5c3d2e1a-yyy     0/1     ContainerCreating   0          1s   ← Another new pod
# ...continues until all updated

# Final state: 3 new pods running v2.0
kubectl get pods
# NAME                   READY   STATUS    RESTARTS   AGE
# app-9f5c3d2e1a-xxx     1/1     Running   0          30s
# app-9f5c3d2e1a-yyy     1/1     Running   0          25s
# app-9f5c3d2e1a-zzz     1/1     Running   0          20s

# Service automatically updated to point to new pods
kubectl get endpoints app-service
# NAME          ENDPOINTS
# app-service   10.1.1.8:80,10.1.1.9:80,10.1.1.10:80
#               ↑ New pod IPs!

# Service IP never changed
kubectl get svc app-service
# NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# app-service   ClusterIP   10.96.100.100   <none>        80/TCP    5m
#                           ↑ Same IP!
```

---

## **Real-World Example: Web Application**

```bash
# ============================================================================
# 1. Create Backend API (Deployment + Service)
# ============================================================================

# Create deployment (manages 5 pods)
kubectl create deployment api \
  --image=myapi:v1.0 \
  --replicas=5

# Expose internally (ClusterIP)
kubectl expose deployment api \
  --port=8080 \
  --name=api-service

# What exists:
# - Deployment: api
# - ReplicaSet: api-xxxxxxxxxx
# - Pods: api-xxxxxxxxxx-xxxxx (5 of them)
# - Service: api-service (ClusterIP: 10.96.50.100)

# ============================================================================
# 2. Create Frontend (Deployment + Service)
# ============================================================================

# Create deployment
kubectl create deployment frontend \
  --image=myfrontend:v1.0 \
  --replicas=3

# Expose publicly (LoadBalancer)
kubectl expose deployment frontend \
  --port=80 \
  --target-port=3000 \
  --name=frontend-lb \
  --type=LoadBalancer

# What exists:
# - Deployment: frontend
# - ReplicaSet: frontend-xxxxxxxxxx
# - Pods: frontend-xxxxxxxxxx-xxxxx (3 of them)
# - Service: frontend-lb (LoadBalancer, public IP)

# ============================================================================
# 3. Create Database (Deployment + Service)
# ============================================================================

# Create deployment
kubectl create deployment postgres \
  --image=postgres:15 \
  --replicas=1

# Expose internally
kubectl expose deployment postgres \
  --port=5432 \
  --name=db-service

# What exists:
# - Deployment: postgres
# - ReplicaSet: postgres-xxxxxxxxxx
# - Pods: postgres-xxxxxxxxxx-xxxxx (1 pod)
# - Service: db-service (ClusterIP: 10.96.75.200)

# ============================================================================
# 4. View Complete Architecture
# ============================================================================

kubectl get all
# Pods: 9 total (5 api + 3 frontend + 1 postgres)
# Deployments: 3 (api, frontend, postgres)
# ReplicaSets: 3 (one per deployment)
# Services: 3 (api-service, frontend-lb, db-service)
```

---

## **Understanding Resource Hierarchy:**

```bash
# Get everything
kubectl get all

# Example output:
NAME                            READY   STATUS    RESTARTS   AGE
pod/api-7d8b49c8b7-11111       1/1     Running   0          5m
pod/api-7d8b49c8b7-22222       1/1     Running   0          5m
pod/api-7d8b49c8b7-33333       1/1     Running   0          5m
pod/frontend-9a8b7c6d5-aaaa    1/1     Running   0          5m
pod/frontend-9a8b7c6d5-bbbb    1/1     Running   0          5m

NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
service/api-service    ClusterIP      10.96.50.100    <none>          8080/TCP       5m
service/frontend-lb    LoadBalancer   10.96.75.150    1.2.3.4         80:30123/TCP   5m

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/api        3/3     3            3           5m
deployment.apps/frontend   2/2     2            2           5m

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/api-7d8b49c8b7       3         3         3       5m
replicaset.apps/frontend-9a8b7c6d5   2         2         2       5m
```

---

## **Quick Reference Commands:**

```bash
# ============================================================================
# PODS
# ============================================================================
kubectl run nginx --image=nginx                     # Create single pod
kubectl get pods                                     # List pods
kubectl get pods -o wide                            # Show pod IPs
kubectl describe pod nginx                          # Pod details
kubectl logs nginx                                  # Pod logs
kubectl delete pod nginx                            # Delete pod

# ============================================================================
# DEPLOYMENTS
# ============================================================================
kubectl create deployment app --image=nginx --replicas=3   # Create deployment
kubectl get deployments                                     # List deployments
kubectl get rs                                             # List replicasets
kubectl scale deployment app --replicas=5                  # Scale
kubectl set image deployment/app nginx=nginx:1.25          # Update image
kubectl rollout status deployment/app                      # Watch update
kubectl rollout undo deployment/app                        # Rollback
kubectl delete deployment app                              # Delete deployment

# ============================================================================
# SERVICES
# ============================================================================
kubectl expose deployment app --port=80 --name=app-svc     # Create service
kubectl get svc                                            # List services
kubectl get endpoints app-svc                              # Show pod IPs
kubectl describe svc app-svc                               # Service details
kubectl delete svc app-svc                                 # Delete service

# ============================================================================
# VIEW ALL
# ============================================================================
kubectl get all                                            # Everything
kubectl get all -l app=nginx                               # Filter by label
kubectl get all -n namespace                               # Specific namespace
```

---

## **Summary:**

|Resource|Purpose|Command|Result|
|---|---|---|---|
|**Pod**|Run containers|`kubectl run nginx --image=nginx`|1 pod|
|**Deployment**|Manage pods|`kubectl create deployment nginx --image=nginx --replicas=3`|1 deployment → 1 replicaset → 3 pods|
|**Service**|Network access|`kubectl expose deployment nginx --port=80`|1 service → routes to all pods|

**Remember:**

- **Pod** = Container(s) running
- **Deployment** = Manages multiple pods (creates ReplicaSet automatically)
- **Service** = Network endpoint to access pods

🎯 Always use **Deployment + Service** in production, never just **Pod**!


# Note


# Reference

