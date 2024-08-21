"""
# https://en.wikipedia.org/wiki/LU_decomposition
# https://courses.physics.illinois.edu/cs357/sp2020/notes/ref-9-linsys.html
# [towards](file:///C:/Users/md%20slauddin/AppData/Local/Microsoft/Windows/INetCache/IE/BCKERTVE/The_Most_Efficient_Way_to_Solve_Any_Linear_Equation,_in_Three_Lines_of_Code___by_Andre_Ye___Towards_Data_Science[1].mhtml)

# [towards gaussian](file:///C:/Users/md%20slauddin/AppData/Local/Microsoft/Windows/INetCache/IE/3E6X2Y0C/Gaussian_Elimination_Algorithm_in_Python___by_Andrew_Joseph_Davies___Level_Up_Coding[1].mhtml)

# [stackAbluse](file:///C:/Users/md%20slauddin/AppData/Local/Microsoft/Windows/INetCache/IE/KDOBP9C6/Solving_Systems_of_Linear_Equations_with_Python's_Numpy[1].mhtml)
"""

__all__ = ['solve', 'solve_triangular', 'solveh_banded', 'solve_banded',
           'solve_toeplitz', 'solve_circulant', 'inv', 'det', 'lstsq',
           'pinv', 'pinvh', 'matrix_balance', 'matmul_toeplitz']