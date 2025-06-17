import numpy as np
from scipy.optimize import fsolve
# import matplotlib.pyplot as plt

def calcular_BlountandFox(datos, vmin, vmax):
    # Extraer datos desde el diccionario
    m = datos['m']
    b = datos['b']
    beta = datos['beta']
    LCG = datos['LCG']
    VCG = datos['VCG']
    f = datos['f']
    epsilon = datos['epsilon']
    g = datos['g']
    rho = datos['rho']

    R_totales = []
    Trims = []

    Vel_nudos = np.arange(vmin, vmax, 0.5) #Vmin = 7.5 y Vmax=25
    Vel_mps = Vel_nudos * 0.514444

    for U in Vel_mps:
        Tau = np.arange(1, 4, 0.01)
        Clbeta = m * g / (0.5 * rho * b ** 2 * U ** 2)
        Cv = U / np.sqrt(g * b)

        def ClB(x):
            return Clbeta - x + 0.0065 * beta * x**0.6

        Cl0 = fsolve(ClB, 0.1)[0]

        for tau in Tau:
            def lam(l):
                return Cl0 - (tau**1.1) * (0.012 * (l**0.5) + 0.0055 * ((l**2.5) / (Cv**2)))

            l = fsolve(lam, 3)[0]
            lm = l * b
            Cp = 0.75 - (1.0 / (5.21 * (Cv / l)**2 + 2.39))
            lp = Cp * lm
            Re = U * lm / 1e-6
            Cf = 0.075 / (np.log10(Re) - 2)**2
            a = VCG - (b / 4) * np.tan(np.radians(beta))
            Crought = 0.0004
            Df = 0.5 * (Cf + Crought) * rho * U**2 * lm * b * (1 / np.cos(np.radians(beta)))

            A = np.array([
                [np.sin(np.radians(tau + epsilon)), np.cos(np.radians(tau))],
                [np.cos(np.radians(tau + epsilon)), -np.sin(np.radians(tau))]
            ])
            B = np.array([
                m * g - Df * np.sin(np.radians(tau)),
                Df * np.cos(np.radians(tau))
            ])
            X = np.linalg.solve(A, B)
            T, N = X

            momentum = N * (LCG - lp) + Df * a - T * f

            if abs(momentum) < 600:
                R_total = T * np.cos(np.radians(tau))
                Volume = m / rho
                Fdelta = U / np.sqrt(g * Volume**(1/3))
                M = 0.98 + (2 * (LCG / b)**1.45 * np.exp(-2 * (Fdelta - 0.85))) - (3 * (LCG / b) * np.exp(-3 * (Fdelta - 0.85)))
                Rt = R_total * M
                break
        else:
            continue

        R_totales.append(Rt)
        Trims.append(tau)

    return R_totales, Trims, Vel_nudos
