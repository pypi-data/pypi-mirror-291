# pytest-status
![Languate - Python](https://img.shields.io/badge/language-python-blue.svg)
![PyPI - License](https://img.shields.io/pypi/l/pytest-status)
![PyPI](https://img.shields.io/pypi/v/pytest-status)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pytest-status)

为用例增加用例状态s标记，运行用例时可以使用--status指定用例状态运行。

## 安装方法
```shell
pip install pytest-status
```
## 使用方式
```python
# filename: test_pytest_status.py
import pytest

@pytest.mark.status('ready')
def test_a():
    pass
    
@pytest.mark.status('implement')
def test_b():
    pass
```
使用以下命令指定归属人运行，支持指定多个归属人
```shell
pytest test_pytest_status.py --status=ready 
```

