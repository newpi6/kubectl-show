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
            "pod": "pod",
            "pods": "pod",
            "deploy": "deployment",
            "deployment": "deployment",
            "deployments": "deployment",
            "ds": "daemonset",
            "daemonset": "daemonset",
            "daemonsets": "daemonset",
            "cm": "configmap",
            "configmap": "configmap",
            "configmaps": "configmap",
            "secret": "secret",
            "secrets": "secret",
            "svc": "service",
            "service": "service",
            "services": "service",
            "ingress": "ingress",
            "rc": "replicaset",
            "replicaset": "replicaset",
            "replicasets": "replicaset",
            "pvc": "persistentvolumeclaim",
            "persistentvolumeclaim": "persistentvolumeclaim",
            "persistentvolumeclaims": "persistentvolumeclaim",
        }
        return kind_map

    def _parse_kind(self, kind):
        kind = kind if isinstance(kind, tuple) else [kind]
        return [self._map.get(i) for i in kind if self._map.get(i)]