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

from .cli import KubernetesQueryCli, KubernetesTemplateCli


def main():
    fire.Fire({
        "q": KubernetesQueryCli,
        "query": KubernetesQueryCli,
        "generate": KubernetesTemplateCli,
        "gen": KubernetesTemplateCli,
    })

if __name__ == '__main__':
    main()
