from setuptools import setup, find_packages

setup(
    name='zetta_grpc_protos',
    version='0.0.1',
    packages=find_packages(where='generated/python'),
    package_dir={'': 'generated/python'},
    install_requires=[
        'grpcio',
        'grpcio-tools',
    ],
    include_package_data=True,
    description='Protobuf definitions and generated Python code for Zetta',
    author='Scott Shi',
    author_email='scott.shi@zettablock.com',
    url='https://github.com/zettablock/zetta-grpc-protos',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

