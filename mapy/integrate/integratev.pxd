from cpython cimport tuple

cimport numpy as np

cdef _trapz2d(f, double xmin, double xmax, int m,
                double ymin, double ymax, int n,
                np.ndarray out, tuple args)

cdef _simps2d(f, double xmin, double xmax, int m,
                double ymin, double ymax, int n,
                np.ndarray out, tuple args)
