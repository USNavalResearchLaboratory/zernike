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

From within console or a jupyter notebook it is possible to see which enviroment is being used by running `import sys; sys.prefix` [1]. 
From terminal, run `conda env list` to show installed enviroments [2]. 
To deactivate the enviroment, run `conda deactivate`. 


### Installing 

To locally install the package, use the following command from within the conda enviroment

```
python -m pip install -e PATH/zernike/
```
where PATH is the path to the package directory. 
Check installalation using `pip list` or `conda list` from outside of the package directory. 

### Uninstall 

To uninstall, run the following outside ofthe the package directory:

```
pip uninstall zernike
```

### Running

In terminal run,

```
conda activate NAME
jupyter notebook
```

then create a jupyter notebook and import using `import zernike`. 
If editing the package and you need to constantly re-import the package use `importlib` library. 
Run `from importlib import reload` and then use `reload(zernike)` as needed.  

### Contributing

For local testing the package without the need to install/uninstall in `pip` or `conda` it is useful to run a python terminal from within the top directory of the package. 
Then `zernike` will be in the search path.
It will show up in `pip` as installed.  

The key functions are in the file `zernike/__init__.py`.

For distributing the package, the following tutorial discusses in detail the procedure: https://packaging.python.org/tutorials/packaging-projects/.
Run `conda install wheel setuptools` if you plan on editing this package. 
In short, from within the directory where `setup.py` is located, run 

```
python3 setup.py sdist bdist_wheel
```


### References 

[1: ]https://biasandvariance.com/2019/02/07/importing-packages-in-jupyter-notebooks/
[2: ]https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
