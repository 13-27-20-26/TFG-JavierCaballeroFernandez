#Esta función se va a emplear para el Savitsky con foils, ya que ese código tiene su propio bucle, por lo que la velocidad irá variando y no será
# necesario tener un rango de velocidades.
import numpy as np
from f_Interpolate_Reynolds import interpolate_Reynolds

def calculos_foils(datos, file_path, velocidad):
    # Extraer parámetros desde el diccionario
    m = datos['m']
    s1 = datos['s1']
    c1 = datos['c1']
    alpha1 = datos['alpha1']
    c1a = datos['c1a']
    Cd_01a = datos['Cd_01a']
    K1 = datos['K1']
    s2 = datos['s2']
    c2 = datos['c2']
    alpha2 = datos['alpha2']
    c2a = datos['c2a']
    Cd_02a = datos['Cd_02a']
    K2 = datos['K2']
    g = datos['g']
    rho = datos['rho']
    rho_aero = datos['rho_aero']
    nu = datos['nu']

    U = velocidad
    W = m * g
    A1, A2 = s1 * c1, s2 * c2
    AR1, AR2 = s1 / c1, s2 / c2
    Re1, Re2 = U * c1 / nu, U * c2 / nu

    cl_list, cd_list = interpolate_Reynolds(file_path, [Re1, Re2], [alpha1, alpha2])
    Cl1, Cl2 = cl_list
    Cd1, Cd2 = cd_list

    L1 = Cl1 * 0.5 * rho * A1 * U**2
    L2 = Cl2 * 0.5 * rho * A2 * U**2
    L_total = L1 + L2

    Cd_ind_1 = K1 * (Cl1**2) / (np.pi * AR1)
    Cd_ind_2 = K2 * (Cl2**2) / (np.pi * AR2)
    Cd_1 = Cd1 + Cd_ind_1
    Cd_2 = Cd2 + Cd_ind_2

    D1 = Cd_1 * 0.5 * rho * A1 * U**2
    D2 = Cd_2 * 0.5 * rho * A2 * U**2

    h1 = 0.3 + 0.5 * (1 - (L_total / W))
    h2 = 0.2 + 0.5 * (1 - (L_total / W))
    Aw1 = h1 * c1a
    Aw2 = h2 * c2a

    D1a = Cd_01a * 0.5 * rho_aero * Aw1 * U**2
    D2a = Cd_02a * 0.5 * rho_aero * Aw2 * U**2

    D_total = D1 + D2 + 2 * D1a + D2a

    return D_total, L_total, L1, L2


# Ejemplo de uso
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
#     'h1': 0.8, 'c1a': 0.27, 'Cd_01a': 0.009,
#     'h2': 0.7, 'c2a': 0.2, 'Cd_02a': 0.01,
# }
# velocidad = 18*0.514444  # Velocidad en nudos
# Dt, Lt, L1, L2 = calculos_foils(datos, file_path, velocidad)
# print(Dt,Lt,L1,L2)
