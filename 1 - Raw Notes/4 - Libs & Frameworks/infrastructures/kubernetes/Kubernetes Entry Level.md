Date: 2025-10-26
Course:
Tags: [[Terminology]] [[Base Knowledge]] [[Infrastructure]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

## 1. What is Kubernetes?

**Answer (with teaching explanation):**
Kubernetes is an **open-source container orchestration platform**. Think of it as a **manager for containers**. It doesn’t replace containers—it organizes them.

**Why:**

* If you run **just Docker**, you can start containers manually, but when you have **hundreds or thousands of containers**, managing them manually is impossible.
* Kubernetes handles **deployment, scaling, health checks, and self-healing** automatically.
* It also helps you **connect services**, manage **storage**, and roll out updates safely.

## 2. What is a Pod?

**Answer:**
A Pod is the **smallest deployable unit in Kubernetes**. Usually, it contains **one container**, but sometimes it contains **a few containers that must share storage/network**.

**Why:**

* Multiple containers in a Pod **share the same IP address and storage volumes**, which is useful if containers work together (like a main app + helper container).
* Kubernetes schedules Pods, not individual containers, so the Pod is the unit of scaling and deployment.

## 3. What is a Node?

**Answer:**
A Node is a **worker machine** in the cluster (can be a VM or physical server). Each Node runs containers inside Pods.

**Why:**

* Nodes are like “workers” in a factory: they actually run the products (containers).
* Each Node runs a **kubelet agent**, which communicates with the Control Plane to know what Pods to run.

## 4. What is a Cluster?

**Answer:**
A Cluster is a **group of Nodes managed together** by the **control plane**.

**Why:**

* The control plane sees the **desired state** of the system (e.g., “3 web Pods should be running”) and schedules Pods on the Nodes to match that.
* Nodes can fail, but Kubernetes will **reschedule Pods** on other Nodes to maintain the desired state.


## 5. What is the Control Plane?

**Answer:**
The Control Plane manages the cluster. It includes:

* **API server** – receives requests (kubectl, internal controllers).
* **Scheduler** – decides which Node runs which Pod.
* **Controller manager** – maintains cluster state (replica counts, scaling).
* **etcd** – key-value store for cluster configuration.

**Why:**

* Without the control plane, Nodes don’t know what to do.
* It ensures the cluster is **self-healing** and matches the desired configuration.


## 6. What is a Deployment?

**Answer:**
A Deployment manages **Pods and ReplicaSets**. It ensures the **desired number of Pods** are running, can **update them** safely, and can **roll back** if needed.

**Why:**

* You don’t want to manually start/stop containers for updates.
* Deployment handles **scaling, updates, and recovery** automatically, so your app stays available.

## 7. What is a Service?

**Answer:**
A Service is a **stable network endpoint** to access a set of Pods.

**Types:**

* **ClusterIP** – internal communication within the cluster.
* **NodePort** – exposes the service on each Node’s port.
* **LoadBalancer** – external traffic via cloud provider load balancer.

**Why:**

* Pods are **ephemeral** (can die and be replaced), so IP addresses change.
* Service provides a **fixed IP or DNS name** to reach the Pods reliably.

## 8. ConfigMap and Secret

**Answer:**

* **ConfigMap** – stores **non-sensitive configuration** for Pods.
* **Secret** – stores **sensitive data** like passwords, API keys, or certificates.

**Why:**

* Keeps configuration **separate from code**.
* Secrets are **encoded and can be encrypted** at rest to enhance security.

## 9. Deployment vs StatefulSet

**Answer:**

* **Deployment**: for stateless apps, like web servers. Pods are interchangeable.
* **StatefulSet**: for stateful apps, like databases. Each Pod has a **stable identity and persistent storage**.

**Why:**

* Stateless apps don’t care which Pod serves traffic; Stateful apps need **persistent identity** for data consistency.

## 10. Scaling

**Answer:**
Use `kubectl scale deployment <name> --replicas=<n>` to increase or decrease the number of Pods.

**Why:**

* Kubernetes automatically schedules new Pods or removes excess Pods to match the desired count.
* Helps handle **traffic spikes** automatically.


## 11. Check Pod Status

**Answer:**
`kubectl get pods` → see Pod names, status, age.
`kubectl describe pod <pod>` → see detailed info like events and container logs.

**Why:**

* Helps you debug issues (CrashLoopBackOff, OOMKilled).
* Shows which Nodes are running your Pods.


## 12. Namespace

**Answer:**
Namespace isolates resources within a cluster.

* Example: `dev`, `test`, `prod` namespaces.

**Why:**

* Prevents name collisions (two `web` Deployments in different environments).
* Can apply **resource limits per namespace**.


## 13. Persistent Volume (PV) and Claim (PVC)

**Answer:**

* **PV** – a storage resource in the cluster.
* **PVC** – a request for storage by a Pod.

**Why:**

* Pods are ephemeral; data needs **persistent storage**.
* PVC abstracts the storage so Pods don’t need to know details about the storage provider.

---

## 14. Ingress

**Answer:**
Ingress manages **external HTTP/S traffic** into the cluster.

**Why:**

* Services expose Pods internally, but Ingress allows **path-based routing**, **SSL**, and **host-based routing** from the outside world.

---

## 15. Commands You Should Know

| Command                          | Purpose                |
| -------------------------------- | ---------------------- |
| `kubectl get pods`               | List all Pods          |
| `kubectl get services`           | List all Services      |
| `kubectl apply -f <file.yaml>`   | Deploy resources       |
| `kubectl logs <pod>`             | See container logs     |
| `kubectl exec -it <pod> -- bash` | Access container shell |

**Why:**

* These commands cover **deployment, debugging, and management**, which is enough for a “basic Kubernetes” role.


## 1️⃣ Sample Flask App

**File: `app.py`**

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Kubernetes!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY app.py .

RUN pip install flask

EXPOSE 5000
CMD ["python", "app.py"]
```

* Build and push this Docker image to **Docker Hub** or **ECR**.


## 2️⃣ Kubernetes Deployment

**File: `deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-container
        image: your-docker-username/flask-app:latest
        ports:
        - containerPort: 5000
```

**Explanation:**

* `replicas: 2` → Kubernetes will run **2 Pods** for this app.
* `selector` & `labels` → Kubernetes uses labels to manage which Pods belong to this Deployment.

---

## 3️⃣ Kubernetes Service

**File: `service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  type: NodePort
  selector:
    app: flask-app
  ports:
    - port: 80
      targetPort: 5000
      nodePort: 30080
```

**Explanation:**

* Exposes the Pods to the **outside world** through NodePort 30080.
* Requests to NodeIP:30080 will be forwarded to Pods on port 5000.

---

## 4️⃣ Deploy to Kubernetes

```bash
# Apply the deployment
kubectl apply -f deployment.yaml

# Apply the service
kubectl apply -f service.yaml

# Check Pods
kubectl get pods

# Check Service
kubectl get service flask-service
```

---

## 5️⃣ Test the App

* If using **Minikube**:

```bash
minikube service flask-service
```

* If using a cloud cluster, open **NodeIP:30080** in your browser.
* You should see:

```
Hello from Kubernetes!
```

---

## 6️⃣ What This Example Shows

| Kubernetes Concept   | How it Appears Here                                                     |
| -------------------- | ----------------------------------------------------------------------- |
| **Pod**              | Each running container is a Pod. Two replicas = 2 Pods.                 |
| **Deployment**       | Manages Pods: ensures 2 replicas, updates Pods if the image changes.    |
| **Service**          | Provides a stable network endpoint to access the Pods.                  |
| **Scaling**          | Change `replicas` to 3 → Kubernetes will add another Pod automatically. |
| **Labels/Selectors** | Connects Deployment and Service to the correct Pods.                    |

---

## 7️⃣ Optional: Scale the App

```bash
kubectl scale deployment flask-deployment --replicas=3
kubectl get pods
```

* Kubernetes automatically creates a **3rd Pod** to handle traffic.

---

This is a **full beginner-friendly, real example** of Kubernetes in action. It shows **how an app is packaged, deployed, exposed, and scaled**.

---

If you want, I can also **show how to update the app image** and **let Kubernetes do a rolling update** without downtime. This will demonstrate one of Kubernetes’ **most powerful features** for beginners.

Do you want me to show that too?


# Note


# Reference

