import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def calcular_Savitsky_SprayAero(datos, vmin, vmax):
    # Extraer datos desde el diccionario
    m = datos['m']
    b = datos['b']
    Puntal = datos['Puntal']
    h_codillo = datos['h_codillo']
    beta = datos['beta']
    LCG = datos['LCG']
    VCG = datos['VCG']
    f = datos['f']
    epsilon = datos['epsilon']
    g = datos['g']
    rho = datos['rho']
    rho_aire = datos['rho_aero']
    Cd_aero = datos['Cd_aero']

    R_totales = []
    Trims = []

    Vel_nudos = np.arange(vmin, vmax, 0.5)
    Vel_mps = Vel_nudos * 0.514444

    for U in Vel_mps:
        Tau = np.arange(1, 4, 0.005)
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

            C = np.array([[1, 1], [1, -1]])
            D = np.array([2 * l * b, (b * np.tan(np.radians(beta))) / (np.pi * np.tan(np.radians(tau)))])
            Y = np.linalg.solve(C, D)
            lk, lc = Y

            Re = U * lm / 1e-6
            Cf = 0.075 / (np.log10(Re) - 2)**2
            a = VCG - (b / 4) * np.tan(np.radians(beta))
            Crought = 0.0004
            Df = 0.5 * (Cf + Crought) * rho * U**2 * lm * b * (1 / np.cos(np.radians(beta)))

            d = lk * np.sin(np.radians(tau))
            Af = b * (Puntal - d)
            D_aero = 0.5 * rho_aire * Cd_aero * Af * U**2
            h_aero = ((Puntal - h_codillo) / 2 + h_codillo) - VCG

            A = np.array([
                [np.sin(np.radians(tau + epsilon)), np.cos(np.radians(tau))],
                [np.cos(np.radians(tau + epsilon)), -np.sin(np.radians(tau))]
            ])
            B = np.array([
                m * g - Df * np.sin(np.radians(tau)),
                Df * np.cos(np.radians(tau)) + D_aero
            ])
            X = np.linalg.solve(A, B)
            T, N = X

            momentum = N * (LCG - lp) + Df * a - T * f - D_aero * h_aero

            if abs(momentum) < 200:
                Rt = T * np.cos(np.radians(tau))

                alfa = np.arctan((np.pi * np.tan(np.radians(tau))) / (2 * np.tan(np.radians(beta))))
                theta = 2 * alfa / np.cos(np.radians(beta))
                Lws = b / (4 * np.sin(2 * alfa) * np.cos(np.radians(beta)))
                Re_ws = U * Lws / 1e-6
                Cf_ws = 0.0074 / Re_ws**0.2 - 4800 / Re_ws
                A_ws = b**2 / (4 * np.sin(2 * alfa) * np.cos(np.radians(beta)))
                D_spray = Cf_ws * 0.5 * rho * A_ws * np.cos(theta) * U**2

                R_total = Rt + D_spray
                break
        else:
            continue

        R_totales.append(R_total)
        Trims.append(tau)

    return R_totales, Trims, Vel_nudos

# Llamada a la función
# datos = {
#     'b': 2.589, 'T': 0.4, 'Puntal': 1.35, 'h_codillo': 0.5,
#     'm': 2415, 'LCG': 4, 'VCG': 0.664,
#     'beta': 18, 'f': 1.36, 'epsilon': 0,
#     'Crought': 0.0004,'Cd_aero': 0.8,
#     'g': 9.81, 'rho': 1025, 'rho_aero': 1.204, 'nu': 1e-6,
#     'VS': 0.105, 'LS': 4.244, 'phi': 0, 'beta2': 18,
#     'x1': 5.144, 's1': 2, 'c1': 0.27,
#     'x2': 0.679, 's2': 1.2, 'c2': 0.16,
#     'h1': 0.8, 'c1a': 0.27, 'Cd_01a': 0.009,
#     'h2': 0.7, 'c2a': 0.2, 'Cd_02a': 0.01,
# }
# resistencias, trims, Vel_nudos = calcular_Savitsky_SprayAero(datos, 7.5, 25)
# # print("Resistencias totales: ", resistencias)
# # print("Trims: ", trims)
# # Grafica de resultados 
# # Plot the Resistance vs Speed
# plt.figure(figsize=(10, 6))
# plt.plot(Vel_nudos, resistencias, 'o-')
# plt.title('Savitsky Method for Hard Chine Planning Hulls') 
# plt.xlabel('Speed (knots)')
# plt.ylabel('Total Resistance (N)')
# plt.grid()
# plt.show()
# # Plot the Trim vs Speed
# plt.figure(figsize=(10, 6))
# plt.plot(Vel_nudos, trims, 'o-')
# plt.title('Trim vs Speed')
# plt.xlabel('Speed (knots)')
# plt.ylabel('Trim (degrees)')
# plt.grid()
# plt.show()
# Save the results to a file
# np.savetxt('Savitsky_SprayAero.txt', np.array(resistencias), header='Total Resistance (N)')
# np.savetxt('Savitsky_SprayAero.txt', np.array(trims), header='Trim (degrees)')
