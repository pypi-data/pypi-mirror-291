# jnp3

一个 Python 语言的辅助工具集，用于记录个人感觉比较有用的辅助函数或者类。

> 名称中的 3 是指 python3，同时也是为了避免和已存在的包冲突。

## 安装

安装预构建的 `.whl` 包：

```sh
pip install https://github.com/JulianFreeman/jnp3/releases/download/v0.2.0/jnp3-0.2.0-py3-none-any.whl
```

通过源码安装：

```sh
pip install git+https://github.com/JulianFreeman/jnp3.git@v0.2.0
```

## 安装可选的 pyside6 工具集

安装预构建的 `.whl` 包：

```shell
pip install jnp3[gui]@https://github.com/JulianFreeman/jnp3/releases/download/v0.2.0/jnp3-0.2.0-py3-none-any.whl
```

通过源码安装：

```shell
pip install jnp3[gui]@git+https://github.com/JulianFreeman/jnp3.git@v0.2.0
```

## 构建

```shell
pip install build
python -m build
```

更多见 [文档](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)
