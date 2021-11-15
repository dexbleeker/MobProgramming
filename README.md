# Installation instructions
Install dependencies:
```
sudo apt install bison build-essential curl flex git libgmp-dev python3 python3-dev python3-pip wget
```

Install pbc library:
```wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
tar -xvf pbc-0.5.14.tar.gz && cd pbc-0.5.14
./configure --prefix=/usr --enable-shared
make && make install && ldconfig
cd .. && rm pbc-0.5.14.tar.gz
```

Install pypbc (python bindings for pbc library):
```
(echo "#define PY_SSIZE_T_CLEAN" && cat pypbc.h) > pypbc.h.temp 
mv pypbc.h.temp pypbc.h
pip3 install .
```

Install rest of the dependencies:
```
pip3 install -r requirements.txt
```

# Run tests
To run the tests, simply execute:
```
python3 -m unittest
```
