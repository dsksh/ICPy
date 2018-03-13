# ICPy

Interval Constraint Programming tool implemented with Python 3.


## Dependencies

- [PyInterval](https://github.com/taschini/pyinterval)
- [Grako](https://bitbucket.org/neogeny/grako)


## Usage

    $ pip install icpy-solver
    
    $ cat example.bch
    Variables
      x in [-1e+8,  1e+8];
    
    Constraints
      x^2 == 2;
    
    end
    
    $ icpy example.bch
    [result]
    solution 0:
    box{'x': interval([1.414213562373095, 1.4142135623730951])}
    
    solution 1:
    box{'x': interval([-1.4142135623730951, -1.414213562373095])}

