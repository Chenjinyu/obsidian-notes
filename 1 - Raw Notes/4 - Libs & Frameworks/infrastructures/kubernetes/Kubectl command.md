Date: 2025-12-15
Course:
Tags: [[Terminology]] [[Base Knowledge]] [[Infrastructure]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

```
kubectl get pods
```

```
kubectl get nodes
```

#### create redis output to yaml in terminal
```
kubectl run redis --image=redis123 --dry-run=client -o yaml
```

#### create redis yaml config file output to file
```
kubectl run redis --image=redis123 --dry-run=client -o yaml > redis.yaml
```

#### create pods
```cli
kubectl create -f redis.yaml
```

#### list all pods in all namespaces
```
kubectl get pods -A -o wide

```
# Note


# Reference

