# setup.py

from setuptools import setup, find_packages

setup(
    name='skyeye-python-instrumentator',
    version='0.2.20',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'starlette'
    ],
    description='Skyeye Python FastAPI R.E.D ',
    author='zhangrui',
    author_email='yihengrui1206@163.com',
    url='https://artifact.srdcloud.cn/artifactory/api/pypi/ctcai-oshare-pypi-mc/skyeye-python-instrumentator',
)