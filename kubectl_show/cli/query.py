#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2022/3/30 21:08
@Author : harvey
@File : main.py
@Software: PyCharm
@Desc:
@Module
"""
import os.path
import time

from kubernetes import client, config
import urllib3
from tabulate import tabulate

from .base import KubernetesCliBase

urllib3.disable_warnings()


__all__ = ['KubernetesQueryCli']


class KubernetesQueryCli(KubernetesCliBase):
    """
    查看pod镜像信息或统计部分资源数量
    """

    def __init__(self, namespace=None, kind=('pod',), ALL=False,
                 fmt="plain", index=False, strip=""):

        config.load_kube_config()
        c = client.Configuration.get_default_copy()
        c.verify_ssl = False
        client.Configuration.set_default(c)

        self._namespace = namespace or self._get_default_ns()
        self._kind = self._parse_kind(kind)
        self._ALL = ALL
        self._fmt = fmt  # table format
        self._index = index
        self._strip = str(strip)  # 该字符串从image_url中移除

        self._corev1api = client.api.CoreV1Api()  # 需要在加载k8s配置之后实例化
        self._appsv1api = client.api.AppsV1Api()
        self._netv1api = client.api.NetworkingV1Api()



    def _get_default_ns(self):
        _, current_context = config.list_kube_config_contexts()
        return current_context.get('context').get('namespace') or 'default'

    def _get_resp_namespace(self, rtype='items-list'):
        """CoreV1Api"""
        corev1api = client.api.CoreV1Api()
        resp = corev1api.list_namespace()
        if rtype == 'items-list':
            return resp.items
        elif rtype == 'ns-list':
            return [i.metadata.name for i in resp.items]
        else:
            return resp

    def _get_resp_pod(self):
        """CoreV1Api"""
        api = self._corev1api
        if self._ALL:
            return api.list_pod_for_all_namespaces()
        return api.list_namespaced_pod(namespace=self._namespace)

    def _get_resp_configmap(self):
        """CoreV1Api"""
        api = self._corev1api
        if self._ALL:
            return api.list_config_map_for_all_namespaces()
        return api.list_namespaced_config_map(namespace=self._namespace)

    def _get_resp_service(self):
        """CoreV1Api"""
        api = self._corev1api
        if self._ALL:
            return api.list_service_for_all_namespaces()
        return api.list_namespaced_service(namespace=self._namespace)

    def _get_resp_ingress(self):
        """CoreV1Api"""
        api = self._netv1api
        if self._ALL:
            return api.list_ingress_for_all_namespaces()
        return api.list_namespaced_ingress(namespace=self._namespace)

    def _get_resp_secret(self):
        """CoreV1Api"""
        api = self._corev1api
        if self._ALL:
            return api.list_secret_for_all_namespaces()
        return api.list_namespaced_secret(namespace=self._namespace)

    def _get_resp_persistentvolumeclaim(self):
        """CoreV1Api"""
        api = self._corev1api
        if self._ALL:
            return api.list_persistent_volume_claim_for_all_namespaces()
        return api.list_namespaced_persistent_volume_claim(namespace=self._namespace)

    # apps v1 api
    def _get_resp_deployment(self):
        """AppsV1Api"""
        api = self._appsv1api
        if self._ALL:
            return api.list_deployment_for_all_namespaces()
        return api.list_namespaced_deployment(namespace=self._namespace)

    def _get_resp_replicaset(self):
        """AppsV1Api"""
        api = self._appsv1api
        if self._ALL:
            return api.list_replica_set_for_all_namespaces()
        return api.list_namespaced_replica_set(namespace=self._namespace)

    def _get_resp_daemonset(self):
        """AppsV1Api"""
        api = self._appsv1api
        if self._ALL:
            return api.list_daemon_set_for_all_namespaces()
        return api.list_namespaced_daemon_set(namespace=self._namespace)

    def _get_resp_event(self):
        api = self._corev1api
        if self._ALL:
            return api.list_event_for_all_namespaces()
        return api.list_namespaced_event(namespace=self._namespace)

    def _run_f(self, func):
        try:
            return eval(func)()
        except Exception as e:
            print(e)
            return None

    def image(self):
        """
        show images of pod
        """
        resp = self._get_resp_pod()
        return tabulate(
            [[i.metadata.namespace,
              i.metadata.name,
              [[j.name, j.image.replace(self._strip, ""), ] for j in i.spec.containers],
              i.status.phase,
              ['Ready' if x.ready else 'Not Ready' or 1 for x in i.status.container_statuses],
              # len(i.spec.containers),
              ]
             for i in resp.items],
            headers=['namespace', 'pod name', 'container name , image', 'pod status', 'container status', ],
            showindex=self._index,
            tablefmt=self._fmt,
        )

    def images(self):
        """images = image"""
        return self.image()

    def count(self):
        """-r pod,deployment  count kind numbers"""

        def get_resp(res):
            func = f"self._get_resp_{res}"
            resp = self._run_f(func)

            return resp

        # table_data = []
        # table_headers = []
        if self._ALL:
            ns_list = ['all-namespaces'] + self._get_resp_namespace(rtype='ns-list')
            table_data = {'namespace': ns_list}
            table_headers = "keys"
            for r in self._kind:
                resp = get_resp(r)
                if resp:
                    _tmp_list = [0] * len(ns_list)
                    for item in resp.items:
                        index = ns_list.index(item.metadata.namespace)
                        _tmp_list[index] += 1
                        _tmp_list[0] += 1
                    table_data[r] = _tmp_list
        else:
            table_headers = "keys"
            _tmp_dict = {"namespace": self._namespace}
            for r in self._kind:
                resp = get_resp(r)
                if resp:
                    _tmp_dict[r] = len(resp.items)
            table_data = [_tmp_dict]
        return tabulate(
            table_data,
            headers=table_headers,
            showindex=self._index,
            tablefmt=self._fmt,
        )

    def counts(self):
        """counts = count"""
        return self.count()
