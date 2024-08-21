# setup.py

from setuptools import setup, find_packages

setup(
    # name='skyeye-python-instrumentator',
    # version='0.1.20',
    name='self-python-instr',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'starlette'
    ],
    description='Skyeye Python FastAPI R.E.D ',
    author='zr',
    author_email='yihengrui1206@163.com',
    url='https://artifact.srdcloud.cn/artifactory/api/pypi/ctcai-oshare-pypi-mc/skyeye-python-instrumentator',
)