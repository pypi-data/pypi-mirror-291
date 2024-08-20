import numpy as np
import itrm

N = 50
M = np.random.randn(N, N)
M = M.T @ M
itrm.heat(M)

N = 25
M = np.random.randn(N, N)
M = M.T @ M
itrm.CONFIG.uni = False
itrm.heat(M)
