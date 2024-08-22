from centigrad.variable import Variable
import math

def test_general():
    x = Variable(3)
    assert x.value == 3
    assert x.parents == []
    assert x.gradients == []
    # Even if there is not a new variable assigment to the operation, the x Variable
    # register a new parent after an operation is made.
    (2*x + 5)**2
    # The new parent for x should be Value(6) because the first operation is a product by 2
    # and its parent's gradient should be 2
    assert len(x.parents) == 1
    assert len(x.gradients) == 1
    assert x.parents[0].value == 6
    assert x.gradients[0] == 2
    # The parent node should also have a parent because the next opperation is addition by 5
    assert len(x.parents[0].parents) == 1
    assert len(x.parents[0].gradients) == 1
    assert x.parents[0].parents[0].value == 11
    assert x.parents[0].gradients[0] == 1
    # That parent node should also have a final parent because the next opperation
    # is an exponentiation to the power of 2
    assert len(x.parents[0].parents[0].parents) == 1
    assert len(x.parents[0].parents[0].gradients) == 1
    assert x.parents[0].parents[0].parents[0].value == 121
    assert x.parents[0].parents[0].gradients[0] == 22
    # Finally, there should not be more parent nodes
    assert len(x.parents[0].parents[0].parents[0].parents) == 0
    assert len(x.parents[0].parents[0].parents[0].gradients) == 0

def test_simple_gradients():
    # Sum
    x = Variable(10)
    fx = (x + 15)
    assert x.grad() == 1

    # Product
    x = Variable(5)
    fx = (2*x)
    assert x.grad() == 2

    # Division with variable in denomintator
    x = Variable(2)
    fx = (1/x)
    assert x.grad() == -0.25

    # Exponentiation
    x = Variable(3)
    fx = (x)**3
    assert x.grad() == 27

    # exp
    x = Variable(6)
    fx = x.exp()
    assert x.grad() == math.exp(x.value)

def test_complex_gradients():
    # Operation 1
    x = Variable(3)
    fx = (2*x + 5)**2
    assert x.grad() == 44

    # Operation 2 (ReLu)
    x = Variable(3)
    fx = ((2*x + 5)**2).relu()
    assert x.grad() == 44

    # Operation 3 (Sigmoid)
    x = Variable(2)
    fx = (1/(1+(-x).exp()))
    assert round(x.grad(),5) == round((fx.value)*(1-fx.value),5)

