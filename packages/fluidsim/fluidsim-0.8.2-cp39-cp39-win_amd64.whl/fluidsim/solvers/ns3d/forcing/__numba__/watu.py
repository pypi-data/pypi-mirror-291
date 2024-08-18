
from numba import njit


@njit(cache=True, fastmath=True)
def compute_watu_coriolis_forcing_component(sigma, mask, coef_forcing_time, target, velocity, out):
    out[:] = sigma * mask * (coef_forcing_time * target - velocity)
    return out


__transonic__ = '0.7.1'
