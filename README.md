# kubectl-show

A kubectl Plugin with Python

## Install

> pip install kubectl-show

## Version 22.1.0.8

- 首位为kubernetes版本

## Usage

> kubectl show [command]  [flags]

### flags

- -A all namespace，--ALL
- -r svc,pod,..., --resource 指定资源类型
- -f github|plain..., table format, --fmt 输出格式化

> 参考[tabulate](https://github.com/astanin/python-tabulate)

- -i , table index, --index, 输出增加行号
- -s "xx", --strip, 输出镜像信息时将该字符串替换为空 