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

__all__ = ['KubernetesCliBase']


class KubernetesCliBase:
    @property
    def _map(self):
        kind_map = {
            "cm": "configmap",
            "configmap": "configmap",
            "configmaps": "configmap",

            "crb": "clusterrolebinding",
            "clusterrolebinding":"clusterrolebinding",
            "clusterrolebindings": "clusterrolebinding",

            "deploy": "deployment",
            "deployment": "deployment",
            "deployments": "deployment",

            "ds": "daemonset",
            "daemonset": "daemonset",
            "daemonsets": "daemonset",

            "ingress": "ingress",

            "pod": "pod",
            "pods": "pod",

            "pvc": "persistentvolumeclaim",
            "persistentvolumeclaim": "persistentvolumeclaim",
            "persistentvolumeclaims": "persistentvolumeclaim",

            "rc": "replicaset",
            "replicaset": "replicaset",
            "replicasets": "replicaset",

            "secret": "secret",
            "secrets": "secret",

            "svc": "service",
            "service": "service",
            "services": "service",
        }
        return kind_map

    def _parse_kind(self, kind):
        kind = kind if isinstance(kind, tuple) else [kind]
        return [self._map.get(i) for i in kind if self._map.get(i)]