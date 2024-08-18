[Pura Vida Neutrosophic Algebra](https://arxiv.org/pdf/2312.02169) is a initiative lead byRanulfo Paiva Barbosa and Florentin Smarandache.
This project aims to implement these ideas into a Python module which can be utilized for other several applications.

### Content
A simple neutrosophic number is a number of the form "X = a + bI".
Where "a" is a real or complex coefficient and "b" is a real or complex number binded to indeterminacy (I).
    
 Having two simple neutrosophic numbers `X = a + bI` and `Y = c + dI`. 
 Operations for Simple Neutrosophic Number stated in Pura Vida Neutrosophic Algebra are:
- Addition using Max-Plus algebra.
    - `add_max(X, Y) = max(a, c) + max(b, d)I`
- Addition using Min-Plus (Tropical) algebra.
    Having two simple neutrosophic numbers X = a + bI and Y = c + dI. 
    - `add_min(X, Y) = min(a, c) + min(b, d)I`
- Multiplication.
    Having two simple neutrosophic numbers X = a + bI and Y = c + dI.
    - `multiply(X, Y) = (a + c) + (b + d)I`

### Limitations
Current features missing:
* Support for complex numbers as coefficients

### How to use
Adding this project to PyPI is intended for a better adoption
Right now you can copy and paste the code to your project.

Here is a simple example of the current features:
![alt text](/src/image.png)

#### Install
> pip install pvn_algebra

#### Import
> import pvn_algebra as pvna

#### Create a number
> X = pvna.NeutrosophicNumber("-3.4 + 3I")
or
> Y = pvna.NeutrosophicNumber(3, -3.4)

#### Operations
> pvna.number.add_min(X, Y)

> pvna.number.add_max(X, Y)

> pvna.number.multipy(X, Y)

#### Matrices
```
A = np.matrix([
    [NeutrosophicNumber(-8, 1), NeutrosophicNumber(5, -1)],
    [NeutrosophicNumber(3, 8), NeutrosophicNumber(23, -2)]
])
```

```
B = np.matrix([
    [NeutrosophicNumber(3, 2), NeutrosophicNumber(13, 3)],
    [NeutrosophicNumber(7, 9), NeutrosophicNumber(3, 5)]
])
```

> C = pvna.matrix.add_min(A, B)

> D = pvna.matrix.add_max(A, B)

```
A = np.matrix([
    [NeutrosophicNumber(-1,0), NeutrosophicNumber(2,0), NeutrosophicNumber(0,-1)],
    [NeutrosophicNumber(3,0), NeutrosophicNumber(0, 1), NeutrosophicNumber(0,0)]
])
```

```
B = np.matrix([
    [NeutrosophicNumber(0,1), NeutrosophicNumber(1,0), NeutrosophicNumber(2,0), NeutrosophicNumber(4,0)],
    [NeutrosophicNumber(1,0), NeutrosophicNumber(0,1), NeutrosophicNumber(0,0), NeutrosophicNumber(2,0)],
    [NeutrosophicNumber(5,0), NeutrosophicNumber(-2,0), NeutrosophicNumber(0,3), NeutrosophicNumber(0,-1)]
])
```

> E = matrix.multiply(A, B)