zernike - Python tools for Zernike polynomials and decomposition
----------------------------------------------------------------


Create a conda enviroment 

```
conda create --name zernike
```

Then activate the enviroment using 

```
conda activate zernike
```

Install needed packages 

```
conda install scipy  matplotlib jupyter
```

Run `conda install wheel setuptools` if you plan on editing this package. 

Within the directory where `setup.py` is run 

```
python3 setup.py sdist bdist_wheel
```
The following tutorial discusses in detail this procedure and the meaning of the output: https://packaging.python.org/tutorials/packaging-projects/




Test that the following works

```
conda create -n NAME scipy matplotlib jupyter
```
