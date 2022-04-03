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

from __future__ import absolute_import

import fire

import kubectl_show
from kubectl_show.cli import KubernetesQueryCli, KubernetesTemplateCli


def version():
    return kubectl_show.__version__


def main():
    fire.Fire({
        "q": KubernetesQueryCli,
        "query": KubernetesQueryCli,
        "g": KubernetesTemplateCli,
        "generate": KubernetesTemplateCli,
        "version": version,
    })


if __name__ == '__main__':
    main()
