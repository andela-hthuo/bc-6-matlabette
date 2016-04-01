# Matlabette
Matlabette is a minimal [REPL](https://en.wikipedia.org/wiki/Read–eval–print_loop) clone of MATLAB.

It's also my project for Andela Class VI boot camp.

The name Matlabette is MATLAB plus the diminutive suffix -ette to imply a smaller version of MATLAB. Like how a cigarette refers to a smaller cigar

## Installation
### Requirements
 * Python 2.7
 * Git

It's recommended to use a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

You can install Matlabette using pip
```
pip install -e git+https://github.com/thuo/bc-6-matlabette#egg=matlabette
```

Alternatively, you can install by cloning this repo then using setup_tools to install
```
git clone https://github.com/thuo/bc-6-matlabette
cd bc-6-matlabette
python setup.py install
```

## Running
If you have installed the app, you can run by simply using the `matlabette` command.

Alternatively, you can run without installing by cloning this repo and running `run.py`. (It's recommended to use a virtual environment)
```
git clone https://github.com/thuo/bc-6-matlabette
cd bc-6-matlabette
pip install -r requirements
python run.py
```

## Features
### Array creation
```
matlabette> a = [1 2 3]
 a =
    1.0    2.0    3.0

```
```
matlabette> a = [1 2 3; 4 5 6; 7 8 9]
 a =
    1.0    2.0    3.0
    3.0    5.0    6.0
    7.0    8.0    9.0
```
 
### Matrix operations
**Transpose**
```
matlabette> a = [1 2]
matlabette> a'
 ans =
    1.0
    2.0
```
**Dot product**
```
matlabette> a = [3 2; 2, 5]
matlabette> b = [4 6; 3 2]
matlabette> a * b
 ans =
    18.0    22.0
    23.0    22.0
```

**Element-wise operations**
```
matlabette> [7 8] .* [4 3]
 ans =
    28.0    24.0
```
```
matlabette> [2 3; 4 5] + 1
 ans =
    2.0    3.0
```

**Inverse**
```
matlabette> inv([2 0; 0 2])
 ans =
   0.5    0.0
   0.0    0.5
```


### Saving and loading workspace:
To save the workspace:
```
matlabette> save <filename>
```
To load workspace from file:
```
matlabette> load <filename>
```
