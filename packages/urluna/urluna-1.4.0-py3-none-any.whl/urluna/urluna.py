

import random
import math

class Flex:
    """
    A class for performing various flexible array operations.
    """

    @classmethod
    def fill_array(cls, value, num_rows, num_cols):
        """
        Generates a 2D array filled with the specified value.

        :param value: Value to fill the array with.
        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with the value.
        """
        if not isinstance(value, int) or not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError("All parameters must be integers")
        if num_rows < 0 or num_cols < 0:
            raise ValueError("Number of rows and columns must be non-negative")
        return [[value] * num_cols for _ in range(num_rows)]
    @classmethod
    def sorted_random_array(cls, min_value, max_value, num_rows, num_cols):
        """
        Generates a 2D array filled with random values sorted in ascending order.

        :param min_value: Minimum value for random generation.
        :param max_value: Maximum value for random generation.
        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with random values sorted in ascending order.
        """
        if not isinstance(min_value, int) or not isinstance(max_value, int) or not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError("All parameters must be integers")
        if min_value > max_value:
            raise ValueError("Minimum value must be less than or equal to Maximum value")
        random_list = [random.randint(min_value, max_value) for _ in range(num_rows * num_cols)]
        random_list.sort()
        return [random_list[i * num_cols: (i + 1) * num_cols] for i in range(num_rows)]

    @classmethod
    def random_array(cls, min_value, max_value, num_rows, num_cols):
        """
        Generates a 2D array filled with random values.

        :param min_value: Minimum value for random generation.
        :param max_value: Maximum value for random generation.
        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with random values.
        """
        if not isinstance(min_value, int) or not isinstance(max_value, int) or not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError("All parameters must be integers")
        if min_value > max_value:
            raise ValueError("Minimum value must be less than or equal to Maximum value")
        return [[random.randint(min_value, max_value) for _ in range(num_cols)] for _ in range(num_rows)]

    @classmethod
    def range_array(cls, start, stop=None, step=1):
        """
        Generates an array containing evenly spaced values within a given range.

        :param start: Start of the range.
        :param stop: End of the range.
        :param step: Step between each value.
        :return: Array containing evenly spaced values within the given range.
        """
        if stop is None:
            start, stop = 0, start

        if not isinstance(start, int) or not isinstance(stop, int) or not isinstance(step, int):
            raise TypeError("Start, stop, and step must be integers")

        if step == 0:
            raise ValueError("Step must not be zero")

        result = list(range(start, stop, step))
        return [result]

    @classmethod
    def zeros_array(cls, num_rows, num_cols):
        """
        Generates a 2D array filled with zeros.

        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with zeros.
        """
        return cls.fill_array(0, num_rows, num_cols)

    @classmethod
    def ones_array(cls, num_rows, num_cols):
        """
        Generates a 2D array filled with ones.

        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with ones.
        """
        return cls.fill_array(1, num_rows, num_cols)
    
    @classmethod
    def identity_matrix(cls, size):
        """
        Generates an identity matrix of given size.

        :param size: Size of the identity matrix.
        :return: Identity matrix.
        """
        if not isinstance(size, int) or size < 0:
            raise TypeError("Size must be a non-negative integer")
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

    @classmethod
    def diagonal_matrix(cls, diagonal):
        """
        Generates a diagonal matrix with the given diagonal elements.

        :param diagonal: List of diagonal elements.
        :return: Diagonal matrix.
        """
        if not isinstance(diagonal, list):
            raise TypeError("Diagonal must be a list of numbers")
        size = len(diagonal)
        return [[diagonal[i] if i == j else 0 for j in range(size)] for i in range(size)]



class Operator:
    """
    A class for performing basic array operations.
    """

    @classmethod
    def add_arrays(cls, array1, array2):
        """
        Adds two arrays element-wise.

        :param array1: First array.
        :param array2: Second array.
        :return: Resultant array after element-wise addition.
        """
        if not isinstance(array1, list) or not isinstance(array2, list):
            raise TypeError("Both parameters must be lists")
        if len(array1) != len(array2) or len(array1[0]) != len(array2[0]):
            raise ValueError("Both arrays must have the same dimensions")

        return [[array1[i][j] + array2[i][j] for j in range(len(array1[0]))] for i in range(len(array1))]

    @classmethod
    def subtract_arrays(cls, array1, array2):
        """
        Subtracts two arrays element-wise.

        :param array1: First array.
        :param array2: Second array.
        :return: Resultant array after element-wise subtraction.
        """
        if not isinstance(array1, list) or not isinstance(array2, list):
            raise TypeError("Both parameters must be lists")
        if len(array1) != len(array2) or len(array1[0]) != len(array2[0]):
            raise ValueError("Both arrays must have the same dimensions")

        return [[array1[i][j] - array2[i][j] for j in range(len(array1[0]))] for i in range(len(array1))]

    @classmethod
    def transpose(cls, matrix):
        """
        Transposes the given matrix.

        :param matrix: Matrix to be transposed.
        :return: Transposed matrix.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
        return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

    @classmethod
    def multiply_matrices(cls, matrix1, matrix2):
        """
        Multiplies two matrices.

        :param matrix1: First matrix.
        :param matrix2: Second matrix.
        :return: Resultant matrix after multiplication.
        """
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both parameters must be lists")
        if not all(isinstance(row, list) for row in matrix1) or not all(isinstance(row, list) for row in matrix2):
            raise TypeError("Both parameters must be lists of lists")
        if len(matrix1[0]) != len(matrix2):
            raise ValueError("Number of columns in the first matrix must equal the number of rows in the second matrix")

        result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    result[i][j] += matrix1[i][k] * matrix2[k][j]
        return result

    @classmethod
    def determinant(cls, matrix):
        """
        Calculates the determinant of the given square matrix.

        :param matrix: Square matrix to calculate the determinant.
        :return: Determinant of the matrix.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Matrix must be square")
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for i in range(n):
            det += ((-1) ** i) * matrix[0][i] * cls.determinant([row[:i] + row[i + 1:] for row in matrix[1:]])
        return det

    @classmethod
    def inverse_matrix(cls, matrix):
        """
        Calculates the inverse of a matrix.

        :param matrix: Input matrix.
        :return: Inverse of the input matrix.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Matrix must be square")
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            row = matrix[i]
            if row[i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        identity[i], identity[j] = identity[j], identity[i]
                        break
            if matrix[i][i] == 0:
                raise ValueError("Matrix is singular")
            scalar = 1 / matrix[i][i]
            matrix[i] = [elem * scalar for elem in matrix[i]]
            identity[i] = [elem * scalar for elem in identity[i]]
            for j in range(n):
                if i != j:
                    scalar = matrix[j][i]
                    matrix[j] = [elem1 - elem2 * scalar for elem1, elem2 in zip(matrix[j], matrix[i])]
                    identity[j] = [elem1 - elem2 * scalar for elem1, elem2 in zip(identity[j], identity[i])]
        return identity
    
    @classmethod
    def hadamard_product(cls, matrix1, matrix2):
        """
        Computes the Hadamard product (element-wise multiplication) of two matrices.

        :param matrix1: First matrix.
        :param matrix2: Second matrix.
        :return: Resultant matrix after element-wise multiplication.
        """
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both parameters must be lists")
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Both matrices must have the same dimensions")
        
        return [[matrix1[i][j] * matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]

    @classmethod
    def scalar_multiply(cls, matrix, scalar):
        """
        Multiplies a matrix by a scalar value.

        :param matrix: Input matrix.
        :param scalar: Scalar value.
        :return: Resultant matrix after scalar multiplication.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be a number")

        return [[scalar * element for element in row] for row in matrix]
    
    @classmethod
    def power_matrix(cls, matrix, pow=1):
        """
        Raises a square matrix to the power of 'pow'.

        :param matrix: Input square matrix.
        :param pow: Exponent to raise the matrix to (default is 1).
        :return: Resultant matrix after exponentiation.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
    
        if len(matrix) != len(matrix[0]):
            raise ValueError("Matrix must be square")

        if pow == 0:
            return cls.identity_matrix(len(matrix))

        if pow == 1:
            return matrix

        result = matrix

        for _ in range(pow - 1):
            result = cls.multiply_matrices(result, matrix)

        return result
    
    @classmethod
    def trace(cls, matrix):
         

         if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
         
         if len(matrix) != len(matrix[0]):
             raise ValueError("Matrix must be square")
         
         return [sum(matrix[i][i] for i in range(len(matrix)))]
            
    @classmethod
    def norm_vector(cls, vector):
        """
        Calculate the Euclidean norm of a vector.
        """
    
        if not isinstance(vector, list) or not all(isinstance(element, list) for element in vector):
            raise TypeError("Vector must be a list of numbers")
    
        return [math.sqrt(sum(element**2 for element in vector[0]))]