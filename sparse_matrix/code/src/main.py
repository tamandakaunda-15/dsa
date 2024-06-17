class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        if matrixFilePath:
            self.load_from_file(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols
            self.values = {}

    def load_from_file(self, matrixFilePath):
        self.values = {}
        with open(matrixFilePath, 'r') as file:
            lines = file.readlines()
            self.numRows = int(lines[0].split('=')[1].strip())
            self.numCols = int(lines[1].split('=')[1].strip())
            for line in lines[2:]:
                line = line.strip()
                if line:
                    try:
                        row, col, val = map(int, line.strip('()').split(','))
                        self.values[(row, col)] = val
                    except ValueError:
                        raise ValueError("Input file has wrong format")
    
    def getElement(self, currRow, currCol):
        return self.values.get((currRow, currCol), 0)
    
    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.values[(currRow, currCol)] = value
        elif (currRow, currCol) in self.values:
            del self.values[(currRow, currCol)]
    
    def __str__(self):
        return f"Rows: {self.numRows}, Columns: {self.numCols}, Values: {self.values}"

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must agree for addition")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        all_keys = set(self.values.keys()).union(other.values.keys())
        for key in all_keys:
            result.setElement(key[0], key[1], self.getElement(key[0], key[1]) + other.getElement(key[0], key[1]))
        return result
    
    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must agree for subtraction")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        all_keys = set(self.values.keys()).union(other.values.keys())
        for key in all_keys:
            result.setElement(key[0], key[1], self.getElement(key[0], key[1]) - other.getElement(key[0], key[1]))
        return result
    
    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions must agree for multiplication")
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        for (i, k), v in self.values.items():
            for j in range(other.numCols):
                if (k, j) in other.values:
                    result.setElement(i, j, result.getElement(i, j) + v * other.values[(k, j)])
        return result

def main():
    print("Welcome to Sparse Matrix Operations")
    print("Choose the operation you want to perform:")
    print("1. Load and Display Matrix")
    print("2. Addition")
    print("3. Subtraction")
    print("4. Multiplication")
    
    choice = int(input("Enter your choice (1/2/3/4): "))

    if choice not in [1, 2, 3, 4]:
        print("Invalid choice!")
        return

    file1 = input("Enter the file name for the sparse matrix (e.g., matrixfile1.txt): ")
    
    # Load the first matrix
    matrix1 = SparseMatrix(matrixFilePath=file1)
    
    if choice == 1:
        print("Loaded Matrix:")
        print(matrix1)
    else:
        file2 = input("Enter the file name for the second sparse matrix (e.g., matrixfile2.txt): ")
        # Load the second matrix for operations
        matrix2 = SparseMatrix(matrixFilePath=file2)
        
        try:
            if choice == 2:
                result = matrix1.add(matrix2)
            elif choice == 3:
                result = matrix1.subtract(matrix2)
            elif choice == 4:
                result = matrix1.multiply(matrix2)
            
            print("Resultant Matrix:")
            print(result)
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
