# Description: This code is used to integrate the different methods used to obtain 
# the resistance of planning boats.
# Also includes methods to obtain the resistance of step hull boats and foil boats.

import numpy as np
# import matplotlib.pyplot as plt
# from scipy.optimize import fsolve
from f_Savitsky import calcular_Savitsky
from f_Savitsky_SprayAeroDrag import calcular_Savitsky_SprayAero
from f_SavitskyFoils import calcular_Savitsky_foils
from f_BandF import calcular_BlountandFox
from f_BandF_SprayAeroDrag import calcular_BandF_SprayAero
from f_Svahn import calcular_Svahn
from f_Foils import calcular_foils
from f_fase_vuelo import calcular_fase_vuelo
from f_resultados_colores import plot_results
from f_resultados_colores import plot_lift_curves



# INPUTS
file_path='Foils/Análisis_2D_Epler817.xlsx'

datos = {
    'b': 2.589, 'T': 0.4, 'Puntal': 1.35, 'h_codillo': 0.5,
    'm': 2415, 'LCG': 4, 'VCG': 0.664,
    'beta': 18, 'f': 1.36, 'epsilon': 0,
    'Crought': 0.0004,'Cd_aero': 0.8,
    'g': 9.81, 'rho': 1025, 'rho_aero': 1.204, 'nu': 1e-6,
    'VS': 0.105, 'LS': 4.12, 'phi': 0, 'beta2': 18,
    'x1': 5.144, 's1': 2, 'c1': 0.27, 'K1': 0.6,
    'x2': 0.679, 's2': 1.2, 'c2': 0.16, 'K2': 0.8,
    'alpha1': 3, 'alpha2': 3.25 ,
    'H1': 0.8, 'c1a': 0.27, 'Cd_01a': 0.009,
    'H2': 0.7, 'c2a': 0.2, 'Cd_02a': 0.01,
}

# Options
FOILS = 1 # 1 = Yes, 0 = No
STEP = 0 # 1 = Yes, 0 = No
Aero_SprayDrag = 0 # 1 = Yes, 0 = No
# Lista para almacenar los resultados
velocities = []
resistances = []
trims = []
method_names = []
lifts = []

if FOILS == 0 and STEP == 0:
    R_Savitsky, Trim_Savitsky, Vels_Savitsky = calcular_Savitsky(datos, 7.5, 25.5)
    R_CorrSavitsky, Trim_CorrSavitsky, Vels_CorrSavitsky = calcular_Savitsky_SprayAero(datos, 7.5, 25.5)
    R_BandF, Trim_BandF, Vels_BandF = calcular_BlountandFox(datos, 7.5, 25.5)
    R_CorrBandF, Trim_CorrBandF, Vels_CorrBandF = calcular_BandF_SprayAero(datos, 7.5, 25.5)

    
    velocities.extend([Vels_Savitsky, Vels_CorrSavitsky, Vels_BandF, Vels_CorrBandF])
    resistances.extend([R_Savitsky, R_CorrSavitsky, R_BandF, R_CorrBandF])
    trims.extend([Trim_Savitsky, Trim_CorrSavitsky, Trim_BandF, Trim_CorrBandF])
    method_names.extend(['Savitsky', 'CorrSavitsky', 'BandF', 'CorrBandF'])
    

elif FOILS == 1 and Aero_SprayDrag == 0: # Si tiene foils, tenga o no step, va a utilizar los mismos métodos, eligiendo si emplear los convencionales o los corregidos
    R_Savitsky, Trim_Savitsky, Vels_Savitsky = calcular_Savitsky(datos, 7.5, 25.5)
    R_BandF, Trim_BandF, Vels_BandF = calcular_BlountandFox(datos, 7.5, 25.5)
    R_SavitskyFoils, L_SavitskyFoils ,Trim_SavitskyFoils, Vels_SavitskyFoils = calcular_Savitsky_foils(datos, file_path, 10, 18.5)
    R_Foils, L_foils, Vels_Foils = calcular_foils(datos, file_path ,10, 18.5)
    R_Vuelo, L_Vuelo, Vels_Vuelo = calcular_fase_vuelo(datos, file_path , 18, 25.5)
    # Unir SavitskyFoils y Vuelo
    # Eliminar posible duplicidad en el punto de unión
    if Vels_SavitskyFoils[-1] == Vels_Vuelo[0]:
        Vels_Total = np.concatenate([Vels_SavitskyFoils, Vels_Vuelo[1:]])
        R_Total = np.concatenate([R_SavitskyFoils, R_Vuelo[1:]])
    else:
        Vels_Total = np.concatenate([Vels_SavitskyFoils, Vels_Vuelo])
        R_Total = np.concatenate([R_SavitskyFoils, R_Vuelo])

    velocities.extend([Vels_Savitsky, Vels_BandF, Vels_SavitskyFoils, Vels_Foils, Vels_Vuelo, Vels_Total])
    resistances.extend([R_Savitsky, R_BandF, R_SavitskyFoils, R_Foils, R_Vuelo, R_Total])
    trims.extend([Trim_Savitsky, Trim_BandF, Trim_SavitskyFoils, [0]*len(Vels_Foils), [0]*len(Vels_Vuelo)])
    lifts.extend([L_SavitskyFoils, L_foils, L_Vuelo])
    method_names.extend(['Savitsky', 'BandF', 'SavitskyFoils', 'Foils', 'Vuelo', 'Resistencia Total'])
    
    # Call the plot_lift_curves function
    plot_lift_curves(Vels_SavitskyFoils, L_SavitskyFoils, Vels_Foils, L_foils, Vels_Vuelo, L_Vuelo)


elif FOILS == 1 and Aero_SprayDrag == 1: # Si tiene foils, tenga o no step, va a utilizar los mismos métodos, eligiendo si emplear los convencionales o los corregidos
    R_CorrSavitsky, Trim_CorrSavitsky, Vels_CorrSavitsky = calcular_Savitsky_SprayAero(datos, 7.5, 25.5)
    R_CorrBandF, Trim_CorrBandF, Vels_CorrBandF = calcular_BandF_SprayAero(datos, 7.5, 25.5)
    R_SavitskyFoils, L_SavitskyFoils ,Trim_SavitskyFoils, Vels_SavitskyFoils = calcular_Savitsky_foils(datos, file_path, 10, 18.5)
    R_Foils, L_foils, Vels_Foils = calcular_foils(datos, file_path ,10, 18.5)
    R_Vuelo, L_Vuelo, Vels_Vuelo = calcular_fase_vuelo(datos, file_path , 18, 25.5)
    # Unir SavitskyFoils y Vuelo
    # Eliminar posible duplicidad en el punto de unión
    if Vels_SavitskyFoils[-1] == Vels_Vuelo[0]:
        Vels_Total = np.concatenate([Vels_SavitskyFoils, Vels_Vuelo[1:]])
        R_Total = np.concatenate([R_SavitskyFoils, R_Vuelo[1:]])
    else:
        Vels_Total = np.concatenate([Vels_SavitskyFoils, Vels_Vuelo])
        R_Total = np.concatenate([R_SavitskyFoils, R_Vuelo])

    velocities.extend([Vels_CorrSavitsky, Vels_CorrBandF,  Vels_SavitskyFoils, Vels_Foils, Vels_Vuelo, Vels_Total])
    resistances.extend([R_CorrSavitsky, R_CorrBandF, R_SavitskyFoils, R_Foils, R_Vuelo, R_Total])
    trims.extend([Trim_CorrSavitsky, Trim_CorrBandF, Trim_SavitskyFoils, [0]*len(Vels_Foils), [0]*len(Vels_Vuelo)])
    lifts.extend([L_SavitskyFoils, L_foils, L_Vuelo])

    method_names.extend(['CorrSavitsky', 'CorrBandF', 'SavitskyFoils', 'Foils', 'Vuelo', 'Resistencia Total'])

    # Call the plot_lift_curves function
    plot_lift_curves(Vels_SavitskyFoils, L_SavitskyFoils, Vels_Foils, L_foils, Vels_Vuelo, L_Vuelo)

elif STEP == 1 and FOILS ==0 and Aero_SprayDrag == 0: # Ya sólo queda la opción de que STEP = 1, y luego jugar si Aero_SprayDrag es 0 o 1
    R_Savitsky, Trim_Savitsky, Vels_Savitsky = calcular_Savitsky(datos, 7.5, 25.5)
    R_BandF, Trim_BandF, Vels_BandF = calcular_BlountandFox(datos, 7.5, 25.5)
    R_Svahn, Trim_Svahn, Vels_Svahn = calcular_Svahn(datos, 18, 25.5) #Svahn está pensado para velocidades muy altas, a menores no encuentra el equilibrio.

    velocities.extend([Vels_Savitsky, Vels_BandF, Vels_Svahn])
    resistances.extend([R_Savitsky, R_BandF, R_Svahn])
    trims.extend([Trim_Savitsky, Trim_BandF, Trim_Svahn])
    method_names.extend(['Savitsky', 'BandF', 'Svahn'])

elif STEP == 1 and FOILS == 0 and Aero_SprayDrag == 1: # Ya sólo queda la opción de que STEP = 1, y luego jugar si Aero_SprayDrag es 0 o 1
    R_CorrSavitsky, Trim_CorrSavitsky, Vels_CorrSavitsky = calcular_Savitsky_SprayAero(datos, 7.5, 25.5)
    R_CorrBandF, Trim_CorrBandF, Vels_CorrBandF = calcular_BandF_SprayAero(datos, 7.5, 25.5)
    R_Svahn, Trim_Svahn, Vels_Svahn = calcular_Svahn(datos, 18, 25.5) #Svahn está pensado para velocidades muy altas, a menores no encuentra el equilibrio.

    velocities.extend([Vels_CorrSavitsky, Vels_CorrBandF, Vels_Svahn])
    resistances.extend([R_CorrSavitsky, R_CorrBandF, R_Svahn])
    trims.extend([Trim_CorrSavitsky, Trim_CorrBandF, Trim_Svahn])
    method_names.extend(['CorrSavitsky', 'CorrBandF', 'Svahn'])

# Plot results
plot_results(velocities, resistances, trims, method_names)

