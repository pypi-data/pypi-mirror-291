import math

class Variable:
    """
    A class representing a variable with automatic differentiation capabilities.

    Parameters
    ----------
    value: float or int
        Numerical value with which the Variable object is initialized

    Attributes
    __________
    value: float or int
        The numerical value of the Variable object.

    parents: list
        A list of Variable objects that have the current Variable as child. These
        are a function of the current Variable object. This attribute is always
        initialized as an empty list
    
    gradients: list
        A list with the gradients of the parents with respect to the current Variable.
        This attribute is always initialized as an empty list.
    """
    def __init__(self, value):
        self.value = value
        self.parents = []
        self.gradients = []

    def __repr__(self):
        """
        Returns a string representation of the Variable object.

        Returns
        -------
        str
            A string representation of the Variable object.
        """
        return f"Variable(value={self.value})"
    
    def __add__(self, other_value):
        """
        Adds the current Variable object to another numerical value or Variable object.

        This method supports the addition of a Variable object with either a numerical value 
        (int or float) or another Variable object. The result is a new Variable object 
        representing the sum.

        Parameters
        ----------
        other_value : int, float, or Variable
            The value or Variable object to be added to the current Variable object.

        Returns
        -------
        Variable
            A new Variable object representing the sum of the current Variable object and 
            `other_value`.

        Notes
        -----
        - If `other_value` is an int or float, it will be converted to a Variable object.
        - The Variable objects involved in the sum will have the result as its parent.
        - The gradient of `result` will be 1 as it is a sum.
        """
        # First we check if the other value is not a Variable object and is numeric
        if (not isinstance(other_value, Variable)) & (type(other_value) in [int, float]):
            # If it is not Variable but it is numeric, a new Variable object is created with the value
            # equal to `other_value`
            other_value = Variable(value = other_value)
        elif (not isinstance(other_value, Variable)) & (type(other_value) not in [int, float]):
            raise("Summation cannot be performed with a non-numeric data type")
        
        # Then, a new Variable is created with value equal to the sum of the value of our current Variable
        # and the value of `other_value`
        result = Variable(value = self.value + other_value.value)

        # Then the parents of the current Variable and `other_value` (if applicable) are updated
        # to contain the result
        self.parents.append(result)
        other_value.parents.append(result)

        # As the operation is sum, the gradient of the result with respect to the child is 1
        self.gradients.append(1)
        other_value.gradients.append(1)
        return result
    
    def __radd__(self, other_value):
        """
        Performs the addition operation when the current Variable object is on the right-hand side.
        """
        return self.__add__(other_value)
    
    def __mul__(self, other_value):
        """
        Multiplies the current Variable object to another numerical value or Variable object.

        This method supports the product of a Variable object with either a numerical value 
        (int or float) or another Variable object. The result is a new Variable object 
        representing the product.

        Parameters
        ----------
        other_value : int, float, or Variable
            The value or Variable object to be multiplied to the current Variable object.

        Returns
        -------
        Variable
            A new Variable object representing the product of the current Variable object and 
            `other_value`.

        Notes
        -----
        - If `other_value` is an int or float, it will be converted to a Variable object.
        - The Variable objects involved in the sum will have the result as its parent.
        - The gradient of the result will be `other_value` as it is a multiplication.
        """
        # First we check if the other value is not a Variable object and is numeric
        if (not isinstance(other_value, Variable)) & (type(other_value) in [int, float]):
            # If it is not Variable but it is numeric, a new Variable object is created with the value
            # equal to `other_value`
            other_value = Variable(value = other_value)
        elif (not isinstance(other_value, Variable)) & (type(other_value) not in [int, float]):
            raise("Multiplication cannot be performed with a non-numeric data type")
        
        # Then, a new Variable is created with value equal to the product of the value of our current Variable
        # and the value of `other_value`
        result = Variable(value = self.value * other_value.value)

        # Then the parents of the current Variable and `other_value` (if applicable) are updated
        # to contain the result
        self.parents.append(result)
        other_value.parents.append(result)

        # As the operation is product, the gradient of the result with respect to the child is the other
        # value involved in the product
        self.gradients.append(other_value.value)
        other_value.gradients.append(self.value)
        return result
    
    def __rmul__(self, other_value):
        """
        Performs the product operation when the current Variable object is on the right-hand side.
        """
        return self.__mul__(other_value)
    
    def __sub__(self, other_value):
        """
        Performs the addition operation after multiplying the other value by -1.
        """
        return self + (other_value*(-1))
    
    def __rsub__(self, other_value):
        """
        Performs the substraction operation when the current Variable object is on the right-hand side.
        """
        return (self.__sub__(other_value))*(-1)
    
    def __pow__(self, other_value):
        """
        Performs the power operation of a Variable object to a numeric exponent.
        """
        # For now, only numeric exponents are supported, not Variable exponents
        result = Variable((self.value)**other_value)
        # The parent of the Variable is updated to contain the result
        self.parents.append(result)
        # And the gradient is included.
        self.gradients.append(other_value*(self.value**(other_value-1)))
        return result
    
    def __neg__(self):
        """
        Performs the negation of a Variable by multiplying -1 by the Variable.
        """
        return (-1)*self
    
    def __truediv__(self, denominator):
        """
        Performs the division operation by multiplying two values, where the second (the denominator) is elevated to the -1 power
        """
        return self * (denominator)**(-1)
          
    def __rtruediv__(self, numerator):
        """
        Performs the division operation when the numerator is not a Variable object but the denominator is.
        """
        return ((self)**(-1)) * numerator
       
    def exp(self):
        """
        Performs the exp operation where the exponent of e is the Variable object
        """
        # First, the result is calculated using the math library
        result = Variable(math.exp(self.value))

        # Then, the result is included as parent
        self.parents.append(result)
        # And the gradient is also included. The gradient is the same as result
        # following the derivative of e^x
        self.gradients.append(result.value)
        return result
    
    def sigmoid(self):
        """
        Performs the sigmoid activation function of the Variable

        This method is created for simplicity as it can also be constructed from scratch just replicating
        the sigmoid function using Variable objects.
        """
        # First, the result is calculated as the sigmoid function of the current Variable
        result = Variable((1) / (1 + (math.exp(-self.value))))

        # Then, a new parent is included
        self.parents.append(result)
        # And the gradient is included following the formula of a sigmoid function
        self.gradients.append((result.value)*(1-result.value))
        return result
    
    def relu(self):
        """
        Performs the relu activation function of the Variable

        This method is created for simplicity as it can also be constructed from scratch just replicating
        the relu function using Variable objects.
        """
        # First, the result is calculated as the relu function of the current Variable 
        result = Variable(max(0, self.value))
        # Then, a new parent is included
        self.parents.append(result)
        # And the gradient is included following the formula of a relu function
        self.gradients.append(1 if (self.value > 0) else 0)
        return result

    def linear(self):
        """
        Performs the linear activation function of the Variable

        This method is created for simplicity as it can also be constructed from scratch just replicating
        the linear function using Variable objects.
        """
        # First, the result is calculated as the linear function of the current Variable 
        result = Variable(self.value)
        # Then, a new parent is included
        self.parents.append(result)
        # And the gradient is included following the formula of a linear function (always 1)
        self.gradients.append(1)
        return result
    
    def grad(self):
        """
        Computes the gradient of final output node (the root parent node) with respect to the current Variable.
        
        This method recursively calculates the gradient by summing the product of each parent's gradient 
        and the corresponding local gradient (chain rule). If the current Variable has no parents, 
        the gradient is 1 (base case for the recursive calculation).
        """
        if len(self.parents)>0:
            # To calculate the gradient of a function, the gradient of the parents is calculated recursively
            # The gradient of a function with respect to a variable is the sum of the products of the gradients
            # of all the parents with the gradients of the parents with respect to the current variable
            return sum([a * b for a, b in zip(self.gradients, [z.grad() for z in self.parents])])
        else:
            # When there are no parents, the gradient is one (initial case for the root parent node)
            return 1