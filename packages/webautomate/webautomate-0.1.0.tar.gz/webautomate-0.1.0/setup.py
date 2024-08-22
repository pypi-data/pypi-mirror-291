from setuptools import setup, find_packages

setup(
    name='webautomate',
    version='0.1.0',
    description='A Python library for browser automation using Selenium',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='devcodes',
    author_email='devcodesjos@gmail.com',
    license='MIT',  # Asegúrate de tener el archivo LICENSE configurado
    packages=find_packages(),
    install_requires=[
        'selenium==4.23.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
