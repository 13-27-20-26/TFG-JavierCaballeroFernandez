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
