import numpy as np
import numba

@numba.njit
def compute_bin_medians(wedge_vals, bin_indices, n_bins):
    # Force output array to be float64 so we can represent NaN.
    result = np.empty(n_bins, dtype=np.float64)
    for bin_i in range(n_bins):
        count = 0
        for j in range(wedge_vals.shape[0]):
            if bin_indices[j] == bin_i:
                count += 1
        if count == 0:
            result[bin_i] = np.nan
        else:
            # Use float64 for temporary array as well.
            tmp = np.empty(count, dtype=np.float64)
            k = 0
            for j in range(wedge_vals.shape[0]):
                if bin_indices[j] == bin_i:
                    tmp[k] = wedge_vals[j]
                    k += 1
            tmp.sort()
            if count % 2 == 1:
                result[bin_i] = tmp[count // 2]
            else:
                result[bin_i] = 0.5 * (tmp[count // 2 - 1] + tmp[count // 2])
    return result