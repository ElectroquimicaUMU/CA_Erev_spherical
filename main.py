import numpy as np
from scipy.special import erfc

F = 96485  # C/mol
R = 8.314  # J/mol·K
T = 298    # K


def eta(E, E0):
    return (F / (R * T)) * (E - E0)


def c_ox_surface(c_ox_star, eta_val):
    return c_ox_star * np.exp(eta_val) / (1 + np.exp(eta_val))


def c_ox(r, t, E, c_ox_star, D_ox, r0, E0):
    eta_val = eta(E, E0)
    c_ox_surf = c_ox_surface(c_ox_star, eta_val)
    term = (c_ox_star - c_ox_surf) * (r0 / r) * erfc((r - r0) / (2 * np.sqrt(D_ox * t)))
    return c_ox_star - term


def current_density(E, t, c_ox_star, D_ox, r0, E0):
    eta_val = eta(E, E0)
    factor = np.exp(eta_val) / (1 + np.exp(eta_val))
    term1 = 1 / np.sqrt(np.pi * D_ox * t)
    term2 = 1 / r0
    return F * c_ox_star * D_ox * (term1 + term2) * factor
