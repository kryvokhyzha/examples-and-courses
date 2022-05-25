class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        for i in range(n):
            for j in range(i, n-i-1):
                matrix[i][j], matrix[j][n-i-1] = matrix[j][n-i-1], matrix[i][j]
                matrix[i][j], matrix[n-i-1][n-j-1] = matrix[n-i-1][n-j-1], matrix[i][j]
                matrix[i][j], matrix[n-j-1][i] = matrix[n-j-1][i], matrix[i][j]
