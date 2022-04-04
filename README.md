# kubectl-show

A kubectl Plugin with Python

## Install

> pip install kubectl-show

## Version 22.1.0.14

- 22为kubernetes sdk主版本，22支持k8s版本1.21-1.23

## Usage

> kubectl-show [command] [sub-command] [flags]

> 以kubectl插件的方式运行：kubectl show [command] [sub-command] [flags]

### command and sub-command

- q|query image|count 查询pod容器镜像|统计
- g|generate template [-k|--kind] 生成不同资源的yaml文件

### flags

- -A all namespace，--ALL, bool,指定该参数则为true
- -n namespace，--namespace
- -k svc,pod,..., --kind 指定资源类型,资源类型名称与k8s一直，支持缩写
- -f github|plain..., table format, --fmt 输出格式化

> 参考[tabulate](https://github.com/astanin/python-tabulate)

- -i , table index, --index, 输出增加行号，query(command)中有效
- -s "xx", --strip, 输出镜像信息时将该字符串替换为空，query(command)中有效

### example

> kubectl show q images

```angular2html
# kubectl-show q images
namespace    pod name                               container name , image                        pod status    container status
default      apple-app                              [['apple-app', 'hashicorp/http-echo']]        Running       ['Ready']
default      banana-app                             [['banana-app', 'hashicorp/http-echo']]       Running       ['Ready']
default      kubernetes-downwardapi-volume-example  [['client-container', 'k8s.gcr.io/busybox']]  Running       ['Ready']
default      nginx-7b57989df-6q59k                  [['nginx', 'nginx']]                          Running       ['Ready']
```

```angular2html
# kubectl-show q images -A -f github
| namespace            | pod name                                  | container name , image                                                                                  | pod status   | container status           |
|----------------------|-------------------------------------------|---------------------------------------------------------------------------------------------------------|--------------|----------------------------|
| argo                 | argo-server-79bf45b5b7-qkn9z              | [['argo-server', 'quay.io/argoproj/argocli:latest']]                                                    | Running      | ['Ready']                  |
| argo                 | workflow-controller-64d4785c88-497xx      | [['workflow-controller', 'quay.io/argoproj/workflow-controller:latest']]                                | Running      | ['Ready']                  |
| default              | apple-app                                 | [['apple-app', 'hashicorp/http-echo']]                                                                  | Running      | ['Ready']                  |
| default              | banana-app                                | [['banana-app', 'hashicorp/http-echo']]                                                                 | Running      | ['Ready']                  |
| default              | kubernetes-downwardapi-volume-example     | [['client-container', 'k8s.gcr.io/busybox']]                                                            | Running      | ['Ready']                  |
| default              | nginx-7b57989df-6q59k                     | [['nginx', 'nginx']]                                                                                    | Running      | ['Ready']                  |
| istio-system         | grafana-64b4b8f789-fkzld                  | [['grafana', 'grafana/grafana:6.5.2']]                                                                  | Running      | ['Ready']                  |
| istio-system         | istio-egressgateway-6c9778c57c-tt6xs      | [['istio-proxy', 'docker.io/istio/proxyv2:1.5.0']]                                                      | Pending      | ['Not Ready']
```

> kubectl-show query count

```html
kubectl-show query count -A -k pod,deployment,rc,svc,cm
namespace               pod    deployment    replicaset    service    configmap
all-namespaces           23            12            12         20           27
argo                      2             2             2          2            2
default                   4             1             1          4            1
istio-system              6             6             6         11           12
kube-node-lease           0             0             0          0            1
kube-public               0             0             0          0            2
kube-system               9             1             1          1            6
kubernetes-dashboard      2             2             2          2            2
operator                  0             0             0          0            1
```

> kubectl-show  g template

```angular2html
# kubectl-show g template  --name test-app --namespace default --replicas 3 -k deployment,svc
apiVersion: apps/v1
kind: Deployment
metadata:
name: test-app
namespace: default
spec:
replicas: 3
strategy:
type: RollingUpdate
rollingUpdate:
maxSurge: 50%
maxUnavailable: 50%
selector:
matchLabels:
app: test-app
template:
metadata:
labels:
app: test-app
spec:
imagePullSecrets: []
nodeSelector: {}
#node.type: db
tolerations: []
#- key: "only"
#  operator: "Equal"
#  value: "db"
#  effect: "NoSchedule"
affinity:
podAntiAffinity: {}
nodeAffinity: {}
volumes: []
#- name: postgres
#  hostPath:
#    path: /data/middleware-data/postgres-data
#    type: DirectoryOrCreate
containers:
- image: test-app
imagePullPolicy: IfNotPresent
name: test-app
args: []
env: []
ports:
- containerPort: 80
name: http
volumeMounts: []
#- name: postgres
#  subPath: postgres
#  mountPath: /var/lib/postgresql/data
resources:
requests:
memory: 50Mi
cpu: 100m
ephemeral-storage: "2Gi"
limits:
memory: 50Mi
cpu: 100m
ephemeral-storage: "10Gi"
---
apiVersion: v1
kind: Service
metadata:
name: test-app
namespace: default
spec:
selector:
app: test-app
ports:
- protocol: TCP
port: 80
targetPort: http
type: NodePort
```

### 生成yaml配置并创建资源

> kubectl-show g template --name test-app --namespace default --replicas 3 -k deployment,svc | kubectl create -f -