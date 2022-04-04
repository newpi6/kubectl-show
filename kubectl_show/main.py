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

import fire

import kubectl_show
from kubectl_show.cli import KubernetesQueryCli, KubernetesTemplateCli


def version():
    return f"kubectl-show version: {kubectl_show.__version__}, support kubenertes 1.21-1.23"


def main():
    fire.Fire({
        "q": KubernetesQueryCli,
        "query": KubernetesQueryCli,
        "g": KubernetesTemplateCli,
        "generate": KubernetesTemplateCli,
        "version": version,
    })
