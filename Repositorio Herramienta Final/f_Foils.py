import numpy as np
# import matplotlib.pyplot as plt
from f_calculos_foils import calculos_foils

def calcular_foils(datos, file_path, vmin, vmax):
    # Extraer variables del diccionario
    b = datos['b']
    T = datos['T']
    Puntal = datos['Puntal']
    m = datos['m']
    Cd_aero = datos['Cd_aero']
    g = datos['g']
    rho_aero = datos['rho_aero']

    R_totales = []
    L_totales = []

    Vel_nudos = np.arange(vmin, vmax, 0.5) # vmin =10 , vmax = 18.5
    Vel_mps = Vel_nudos * 0.514444

    for U in Vel_mps:

        W = m * g
        D_foils, L_total, L1, L2 = calculos_foils(datos, file_path, U)
        #Se ha asumido una elevación lineal para obtener el Area frontal
        Af = b * (Puntal - (T * (1 - (L_total / W))))
        D_aero = Cd_aero * 0.5 * rho_aero * Af * U**2
        D_total = D_foils + D_aero

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
# Resistencia, Lift, Vel_nudos = calcular_foils (datos, 'Foils/Análisis_2D_Epler817.xlsx', 10, 18.5)
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
# np.savetxt('Foils_Resistance.txt', np.array(Resistencia), header='Total Resistance (N)')
# np.savetxt('Foils_Lift.txt', np.array(Lift), header='Lift (N)')