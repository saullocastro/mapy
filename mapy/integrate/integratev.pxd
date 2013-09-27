from cpython cimport tuple

cimport numpy as np

cdef trapz2d(f, double xmin, double xmax, int m,
                double ymin, double ymax, int n,
                np.ndarray out, tuple args)

cdef simps2d(f, double xmin, double xmax, int m,
                double ymin, double ymax, int n,
                np.ndarray out, tuple args)
