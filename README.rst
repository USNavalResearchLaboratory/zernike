zernike - Python tools for Zernike polynomials and decomposition
----------------------------------------------------------------

### Setup

Create a conda enviroment

```
conda create -n NAME scipy matplotlib jupyter
```

and replace `NAME` with the enviroment name. 
If you ever want to remove the enviroment use `conda env remove -n NAME`
Activate the enviroment using 


```
conda activate NAME
```


### Installing 

To locally install the package, use the following command from within the conda enviroment

```
python -m pip install -e PATH/zernike/
```
where PATH is the path to the package directory. 
Check installalation using `pip list` or `conda list` from outside of the package directory. 

### Contributing

For local testing the package without the need to install/uninstall in `pip` or `conda` it is useful to run a python terminal from within the top directory of the package. 
Then `zernike` will be in the search path.
It will show up in `pip` as installed.  

For distributing the package, the following tutorial discusses in detail the procedure: https://packaging.python.org/tutorials/packaging-projects/.
Run `conda install wheel setuptools` if you plan on editing this package. 
In short, from within the directory where `setup.py` is run 

```
python3 setup.py sdist bdist_wheel
```
