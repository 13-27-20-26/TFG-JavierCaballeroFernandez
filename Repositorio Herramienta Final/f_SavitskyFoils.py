import numpy as np
from scipy.optimize import fsolve
from f_calculos_foils import calculos_foils
# import matplotlib.pyplot as plt

def calcular_Savitsky_foils(datos, file_path, vmin, vmax):
    # Extraer variables del diccionario
    b = datos['b']
    T = datos['T']
    Puntal = datos['Puntal']
    m = datos['m']
    LCG = datos['LCG']
    VCG = datos['VCG']
    beta = datos['beta']
    f = datos['f']
    epsilon = datos['epsilon']
    Crought = datos['Crought']
    Cd_aero = datos['Cd_aero']
    x1 = datos['x1']
    x2 = datos['x2']
    H2 = datos['H2']
    g = datos['g']
    rho = datos['rho']
    rho_aero = datos['rho_aero']

    W = m * g
    R_totales = []
    Trims = []
    L_totales = []

    Vel_nudos = np.arange(vmin, vmax, 0.5) # vmin = 10 , vmax = 18.5
    Vel_mps = Vel_nudos * 0.514444

    for U in Vel_mps:
        D_foils, L_total, L1, L2 = calculos_foils(datos, file_path, U)
        Delta = (W - L_total) / g
        XCG = (LCG * W - x1 * L1 - x2 * L2) / (W - L_total)
        Tau = np.arange(0, 4, 0.01)
        Clbeta = Delta * g / (0.5 * rho * b ** 2 * U ** 2)
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

            C = np.array([[1, 1], [1, -1]])
            D = np.array([2 * l * b, (b * np.tan(np.radians(beta))) / (np.pi * np.tan(np.radians(tau)))])
            lk, lc = np.linalg.solve(C, D)

            Re = U * lm / 1e-6
            Cf = 0.075 / (np.log10(Re) - 2)**2
            a = VCG - (b / 4) * np.tan(np.radians(beta))
            Df = 0.5 * (Cf + Crought) * rho * U**2 * lm * b / np.cos(np.radians(beta))

            d = lk * np.sin(np.radians(tau))
            Af = b * (Puntal - d)
            D_aero = 0.5 * rho_aero * Cd_aero * Af * U**2
            h_aero = ((Puntal - d) / 2 + d) - VCG

            A = np.array([
                [np.sin(np.radians(tau + epsilon)), np.cos(np.radians(tau))],
                [np.cos(np.radians(tau + epsilon)), -np.sin(np.radians(tau))]
            ])
            B = np.array([
                Delta * g + (Df + D_foils) * np.sin(np.radians(tau)),
                Df * np.cos(np.radians(tau)) + D_aero + D_foils * np.cos(np.radians(tau))
            ])
            T, N = np.linalg.solve(A, B)

            momentum = N * (XCG - lp) + Df * a + D_foils * (H2 + VCG) - T * f - D_aero * h_aero

            if abs(momentum) < 350:
                Rt = T * np.cos(np.radians(tau))
                break
        else:
            continue

        R_totales.append(Rt)
        Trims.append(tau)
        L_totales.append(L_total)

    return R_totales, L_totales, Trims, Vel_nudos
