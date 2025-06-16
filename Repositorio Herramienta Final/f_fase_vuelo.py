import numpy as np
# import matplotlib.pyplot as plt
from f_Buscar_AoA import buscar_AoA
from f_buscar_Cd import buscar_Cd

def calcular_fase_vuelo(datos, file_path, vmin, vmax):
    # Extraer variables del diccionario
    m = datos['m']
    LCG = datos['LCG']
    x1 = datos['x1']
    x2 = datos['x2']
    s1 = datos['s1']
    c1 = datos['c1']
    K1 = datos['K1']
    s2 = datos['s2']
    c2 = datos['c2']
    K2 = datos['K2']
    H1 = datos['H1']
    c1a = datos['c1a']
    Cd_01a = datos['Cd_01a']
    H2 = datos['H2']
    c2a = datos['c2a']
    Cd_02a = datos['Cd_02a']
    g = datos['g']
    rho = datos['rho']
    rho_aero = datos['rho_aero']
    nu = datos['nu']
    Cd_aero = datos['Cd_aero']
    b = datos['b']
    Puntal = datos['Puntal']

    W = m * g
    A1, A2 = s1 * c1, s2 * c2
    AR1, AR2 = s1 / c1, s2 / c2

    R_totales = []
    L_totales = []

    Vel_nudos = np.arange(vmin, vmax, 0.5) # vmin = 18 kn, vmax = 25.5 kn
    Vel_mps = Vel_nudos * 0.514444

    for U in Vel_mps:

        A = np.array([[1, 1], [x1 - LCG, x2 - LCG]])
        B = np.array([W, 0])
        L1, L2 = np.linalg.solve(A, B)
        L_total = L1 + L2

        Cl1 = L1 / (0.5 * rho * A1 * U**2)
        Cl2 = L2 / (0.5 * rho * A2 * U**2)

        Re1 = U * c1 / nu
        Re2 = U * c2 / nu

        alpha1 = buscar_AoA(file_path, Cl1, Re1)
        alpha2 = buscar_AoA(file_path, Cl2, Re2)

        Cd1 = buscar_Cd(file_path, alpha1, Re1)
        Cd2 = buscar_Cd(file_path, alpha2, Re2)

        Cd_ind_1 = K1 * (Cl1**2) / (np.pi * AR1)
        Cd_ind_2 = K2 * (Cl2**2) / (np.pi * AR2)

        Cd_1 = Cd1 + Cd_ind_1
        Cd_2 = Cd2 + Cd_ind_2

        D1 = Cd_1 * 0.5 * rho * A1 * U**2
        D2 = Cd_2 * 0.5 * rho * A2 * U**2

        Aw1 = H1 * c1a
        Aw2 = H2 * c2a
        D1a = Cd_01a * 0.5 * rho_aero * Aw1 * U**2
        D2a = Cd_02a * 0.5 * rho_aero * Aw2 * U**2

        Af = b * Puntal
        D_aero = Cd_aero * 0.5 * rho_aero * Af * U**2

        D_total = D1 + D2 + 2 * D1a + D2a + D_aero

        R_totales.append(D_total)
        L_totales.append(L_total)

    return  R_totales, L_totales, Vel_nudos

# file_path = 'Foils/Análisis_2D_Epler817.xlsx'
# datos = {
#     'b': 2.589, 'T': 0.4, 'Puntal': 1.35, 'h_codillo': 0.5,
#     'm': 2415, 'LCG': 4, 'VCG': 0.664,
#     'beta': 18, 'f': 1.36, 'epsilon': 0,
#     'Crought': 0.0004,'Cd_aero': 0.8,
#     'g': 9.81, 'rho': 1025, 'rho_aero': 1.204, 'nu': 1e-6,
#     'VS': 0.105, 'LS': 4.244, 'phi': 0, 'beta2': 18,
#     'x1': 5.144, 's1': 2, 'c1': 0.27, 'K1': 1.2,
#     'x2': 0.679, 's2': 1.2, 'c2': 0.16, 'K2': 1.2,
#     'alpha1': 3, 'alpha2': 3.25 ,
#     'H1': 0.8, 'c1a': 0.27, 'Cd_01a': 0.009,
#     'H2': 0.7, 'c2a': 0.2, 'Cd_02a': 0.01,
# }
# W = 2415 * 9.81
# Resistencia, Lift, Vel_nudos = calcular_fase_vuelo (datos, 'Foils/Análisis_2D_Epler817.xlsx', 18, 25.5)
# # print("Resistencias totales: ", resistencias)
# # print("Trims: ", trims)
# # Grafica de resultados 
# # Plot the Resistance vs Speed
# plt.figure(figsize=(10, 6))
# plt.plot(Vel_nudos, Resistencia, 'o-')
# plt.title('Resistencia Foils') 
# plt.xlabel('Speed (knots)')
# plt.ylabel('Total Resistance (N)')
# plt.grid()
# plt.show()
# # Plot the Lift vs Speed
# plt.figure(figsize=(10, 6))
# plt.plot(Vel_nudos, Lift, 'o-')
# plt.title('Lift vs Speed')
# plt.xlabel('Speed (knots)')
# plt.ylabel('Lift (N)')
# plt.axhline(y=W, color='r', linestyle='--')
# plt.grid()
# plt.show()
# # Save the results to a file
# np.savetxt('Vuelo_Resistance.txt', np.array(Resistencia), header='Total Resistance (N)')
# np.savetxt('Vuelo_Lift.txt', np.array(Lift), header='Lift (N)')