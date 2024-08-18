from setuptools import setup, find_packages

# 读取 README.md 文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='custom-file-encryptor',
    version='1.0.2',
    description='A custom Python library for file encryption and decryption using a simple, self-made encryption algorithm. This library supports encryption of any file type and is easy to integrate into other projects.',
    long_description=long_description,  # 设置长描述
    long_description_content_type="text/markdown",  # 确保内容类型为 Markdown
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[],
    # 其他配置...
)
