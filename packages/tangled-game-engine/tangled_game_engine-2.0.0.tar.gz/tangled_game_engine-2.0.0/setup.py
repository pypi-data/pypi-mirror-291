from setuptools import setup, find_packages

setup(
    name='tangled_game_engine',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'python_dateutil >= 2.5.3',
        'setuptools >= 21.0.0',
        'urllib3 >= 1.25.3, < 2.1.0',
        'pydantic >= 2',
        'typing-extensions >= 4.7.1',
        'wheel >= 0.29.0',
        'requests >= 2.31.0',
    ],
    dependency_links=[
    ],
    entry_points={
        'console_scripts': [
            # 'console_script_name = module_name:function_name'
        ],
    },
    author='Erik Kiss',
    author_email='erik@snowdropquantum.com',
    description='A package for the Tangled game model class',
    url='https://github.com:snowdropquantum/tangled-game-package',
)
