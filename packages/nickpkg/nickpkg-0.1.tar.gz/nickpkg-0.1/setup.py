from setuptools import setup, find_packages

setup(
    name='nickpkg',
    version='0.1',
    description='A simple package to add two numbers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='loujiajia',
    author_email='loujiajia1@163.com',
    url='https://github.com/yourusername/nickpkg',  # 如果你有项目主页
    packages=find_packages(),  # 自动找到所有的包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 要求的Python版本
)
