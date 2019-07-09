from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read();

setup(name='zernike',
    version='0.0.1',
    description='Zernike polynomials and decomposition',
    long_description=readme(),
    classifiers=[
            'Development Status :: 1 - Planning',
            'Programming Language :: Python :: 3',
            ],
    author='Luke A Johnson',
    author_email='luke.johnson@nrl.navy.mil',
    url='',
    packages=['zernike'],
    install_requires=['scipy',],
    include_package_data=True,
    zip_safe=False)
