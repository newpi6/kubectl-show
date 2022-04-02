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

import urllib3
import jinja2

from .base import KubernetesCliBase

urllib3.disable_warnings()


__all__ = ['KubernetesTemplateCli']


class KubernetesTemplateCli(KubernetesCliBase):
    """
    生成k8s yaml模板，不依赖于k8s配置
    """

    def __init__(self, kind=('deployment',)):
        self._kind = self._parse_kind(kind)

    def template(self, ):
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parent.parent
        TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
        t_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
        t_env = jinja2.Environment(loader=t_loader)
        j2_list = []
        for res in self._kind:
            j2_file = f"{res}.j2.yaml"
            try:
                j2_list.append(t_env.get_template(j2_file))
            except Exception as e:
                print(e)
                continue
        return "\n---\n".join([j2.render() for j2 in j2_list])
