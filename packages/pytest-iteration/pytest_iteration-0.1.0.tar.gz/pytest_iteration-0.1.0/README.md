# pytest-iteration
![Languate - Python](https://img.shields.io/badge/language-python-blue.svg)
![PyPI - License](https://img.shields.io/pypi/l/pytest-iteration)
![PyPI](https://img.shields.io/pypi/v/pytest-iteration)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pytest-iteration)

为用例增加用例状态s标记，运行用例时可以使用--iteration指定用例状态运行。

## 安装方法
```shell
pip install pytest-iteration
```
## 使用方式
```python
# filename: test_pytest_iteration.py
import pytest

@pytest.mark.iteration('v2.0.0')
def test_a():
    pass
    
@pytest.mark.iteration('v2.1.0')
def test_b():
    pass
```
使用以下命令指定迭代运行，支持指定多个迭代
```shell
pytest test_pytest_iteration.py --iteration=v2.0.0 
```

