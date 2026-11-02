---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---
![](assets/1%20-%20Reliability%20-%20Mesh%20and%20Envoy/file-20261101225228396.png)![](assets/1%20-%20Reliability%20-%20Mesh%20and%20Envoy/file-20261101225614517.png)


Envoy Proxy can be integrated with Kubernetes as a service proxy, which is specifically useful in microservices architectures. Here are the general steps on how it is typically integrated:

1. **Deployment**: Envoy Proxy is deployed as a sidecar container alongside your application containers in a pod. This allows it to intercept all network traffic to and from the application.
2. **Service Mesh**: Often, Envoy is used together with service mesh technologies like Istio. In this setup, Envoy proxies manage the communication between services, offering features such as load balancing, service discovery, failure recovery, metrics, and monitoring.
3. **Configuration**: Envoy is configured through either static configuration files or dynamic configuration via APIs. The configuration includes routing rules, service discovery, and other networking policies.
4. **Communication**: Envoy listens on defined ports, handling incoming requests and routing them appropriately based on the defined rules. It can also handle egress traffic, securing outbound connections.
5. **Observability**: Envoy provides rich metrics, logs, and tracing capabilities, which can be integrated with monitoring tools to give insights into service performance and health.
6. **Enhanced Security**: By using Envoy, you can enforce security policies such as mTLS (Mutual TLS) for secure service-to-service communication.

![](assets/1%20-%20Reliability%20-%20Mesh%20and%20Envoy/file-20261101232055091.png)
![](assets/1%20-%20Reliability%20-%20Mesh%20and%20Envoy/file-20261101232144596.png)


```text
               +-----------------------------------+
               |        SERVICE MESH               |
               |       (Control Plane)             |
               +-----------------+-----------------+
                                 |
         Sends configurations   |   Sends configurations
         & security policies     |   & security policies
                                 v
         +-----------------------+-----------------------+
         |                                               |
         v                                               v
+-----------------+                             +-----------------+
|   ENVOY PROXY   |                             |   ENVOY PROXY   |
|  (Data Plane)   | -- Intercepts & Encrypts -> |  (Data Plane)   |
+--------+--------+                             +--------+--------+
         ^                                               ^
     Sits next                                       Sits next
        to                                              to
         v                                               v
+--------+--------+                             +--------+--------+
|  Microservice   |                             |  Microservice   |
|    Instance     |                             |    Instance     |
+-----------------+                             +-----------------+

```

![](assets/1%20-%20Reliability%20-%20Mesh%20and%20Envoy/file-20261101232410131.png)

# How to configure Istio?
How do we configure all these features for our microservice application?
1. You do not have to adjust Deployment and Service K8s YAML files
2. Istio configuration **separate** from application configuration

Istio is configured with Kubernetes YAML fies, uses Kubernetes CustomResourceDefinitions(CRD) to 
- extending the kubernetes API
- custom kubernetes component/object for e.g. 3rd party technologies(like Istio, Prometheus, etc.)
- can be used like any other native kubernetes object


