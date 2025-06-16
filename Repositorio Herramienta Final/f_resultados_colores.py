import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker

# Function to save results to a txt file
def results_to_txt(filename, velocities, resistances, trims, lifts = None):
    with open(filename, 'w') as f:
        f.write("Velocities:\n")
        for vels in velocities:
            f.write(",".join(map(str, vels)) + "\n")
            f.write("\nResistances:\n")
        for res in resistances:
            f.write(",".join(map(str, res)) + "\n")
            f.write("\nTrims:\n")
        for trim in trims:
            f.write(",".join(map(str, trim)) + "\n")
        if lifts:
            f.write("\nLifts:\n")
            for lift in lifts:
                f.write(",".join(map(str, lift)) + "\n")

# Function to plot resistances and trims
def plot_results(velocities, resistances, trims, method_names):
    import matplotlib.ticker as ticker
    import matplotlib.pyplot as plt

    # Diccionario de colores fijos para cada método
    color_dict = {
        'Savitsky': 'blue',
        'CorrSavitsky': 'deepskyblue',
        'BandF': 'orange',
        'CorrBandF': 'gold',
        'SavitskyFoils': 'green',
        'Foils': 'lime',
        'Vuelo': 'red',
        'Resistencia Total': 'black',
        'Svahn': 'purple'
    }

    plt.figure(figsize=(12, 6))
    
    # Plot resistances
    plt.subplot(1, 2, 1)
    for i in range(len(resistances)):
        color = color_dict.get(method_names[i], None)
        res_kN = np.array(resistances[i]) / 1000
        plt.plot(velocities[i], res_kN, label=method_names[i], linewidth=2.2, color=color)
    plt.xlabel('Velocidad (kn)', fontsize=15, fontweight='bold')
    plt.ylabel('Resistencia (kN)', fontsize=15, fontweight='bold')
    plt.title('Curvas de Resistencia', fontsize=17, fontweight='bold')
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    plt.tick_params(axis='both', labelsize=13)
    for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
        label.set_fontweight('bold')

    # Plot trims
    plt.subplot(1, 2, 2)
    for i in range(len(trims)):
        color = color_dict.get(method_names[i], None)
        plt.plot(velocities[i], trims[i], label=method_names[i], linewidth=2.2, color=color)
    plt.xlabel('Velocidad (kn)', fontsize=15, fontweight='bold')
    plt.ylabel('Trimado (degrees)', fontsize=15, fontweight='bold')
    plt.title('Curvas de Trimado', fontsize=17, fontweight='bold')
    plt.legend()
    plt.grid(True)
    plt.tick_params(axis='both', labelsize=13)
    for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
        label.set_fontweight('bold')

    plt.tight_layout()
    plt.show()



def plot_lift_curves(velocities_foils, lift_foils, velocities_savitskyfoils, lift_savitskyfoils, velocities_vuelo, lift_vuelo):
    plt.figure(figsize=(10, 6))
    
    # Convertir lift a kN
    lift_foils_kN = np.array(lift_foils) / 1000
    lift_savitskyfoils_kN = np.array(lift_savitskyfoils) / 1000
    lift_vuelo_kN = np.array(lift_vuelo) / 1000

    # Plotting the lift curves for each method
    plt.plot(velocities_foils, lift_foils_kN, label='Foils', linewidth=2.2, marker='o')
    plt.plot(velocities_savitskyfoils, lift_savitskyfoils_kN, label='SavitskyFoils',linewidth=2.2 , marker='x')
    plt.plot(velocities_vuelo, lift_vuelo_kN, label='Vuelo', linewidth=2.2, marker='s')
    plt.axhline(y=2.415*9.81, color='r', linestyle='--', label = 'Peso (kN)')
    # Adding titles and labels
    plt.title('Curvas de Sustentación')
    plt.xlabel('Velocidad (m/s)')
    plt.ylabel('Lift (kN)')
    plt.legend()
    plt.grid(True)
    
    # Save the plot as a PNG file
    plt.savefig('lift_curves.png')
    plt.show()


def save_to_excel(filename, velocities, resistances, trims, lifts, method_names):
    """
    Guarda todos los resultados en una única hoja de Excel.
    Cada fila contiene el método al que pertenece.
    """
    rows = []

    for i, method in enumerate(method_names):
        num_points = min(len(velocities[i]), len(resistances[i]), len(trims[i]))
        for j in range(num_points):
            row = {
                'Método': method,
                'Velocidad (kn)': velocities[i][j],
                'Resistencia (N)': resistances[i][j],
                'Trim (grados)': trims[i][j],
            }
            if lifts is not None and i < len(lifts) and j < len(lifts[i]):
                row['Sustentación (N)'] = lifts[i][j]
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)

# # Example data (replace with actual data from your script)
# velocities = [[7.5, 10, 15], [7.5, 10, 15], [7.5, 10, 15]]
# resistances = [[100, 150, 200], [110, 160, 210], [120, 170, 220]]
# trims = [[5, 6, 7], [5.5, 6.5, 7.5], [6, 7, 8]]
# lifts = [[50, 60, 70], [55, 65, 75], [60, 70, 80]]
# method_names = ['Savitsky', 'CorrSavitsky', 'BandF']

# # Save results to Excel and text files
# save_to_excel('resultados.xlsx', velocities, resistances, trims, lifts, method_names)
# save_to_txt('result.txt', velocities, resistances, trims, lifts, method_names)

# print("Results have been saved to 'resultados.xlsx' and 'result.txt'.")



# Example usage:
# Assuming the following lists are obtained from the calculations
# velocities_foils = [10, 12, 14, 16, 18]
# lift_foils = [1000, 1500, 2000, 2500, 3000]

# velocities_savitskyfoils = [10, 12, 14, 16, 18]
# lift_savitskyfoils = [1100, 1600, 2100, 2600, 3100]

# velocities_vuelo = [10, 12, 14, 16, 18]
# lift_vuelo = [1200, 1700, 2200, 2700, 3200]

# # Call the function to plot the lift curves
# plot_lift_curves(velocities_foils, lift_foils, velocities_savitskyfoils, lift_savitskyfoils, velocities_vuelo, lift_vuelo)


# # INPUTS
# file_path='Foils/Análisis_2D_Epler817.xlsx'
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
# # Options
# FOILS = 1 # 1 = Yes, 0 = No
# STEP = 1 # 1 = Yes, 0 = No
# Aero_SprayDrag = 1 # 1 = Yes, 0 = No

# # Lista para almacenar los resultados
# velocities = []
# resistances = []
# trims = []
# method_names = []

# if FOILS == 0 and STEP == 0:
#     R_Savitsky, Trim_Savitsky, Vels_Savitsky = calcular_Savitsky(datos, 7.5, 25.5)
#     R_CorrSavitsky, Trim_CorrSavitsky, Vels_CorrSavitsky = calcular_Savitsky_SprayAero(datos, 7.5, 25.5)
#     R_BandF, Trim_BandF, Vels_BandF = calcular_BlountandFox(datos, 7.5, 25.5)
#     R_CorrBandF, Trim_CorrBandF, Vels_CorrBandF = calcular_BandF_SprayAero(datos, 7.5, 25.5)
    
#     velocities.extend([Vels_Savitsky, Vels_CorrSavitsky, Vels_BandF, Vels_CorrBandF])
#     resistances.extend([R_Savitsky, R_CorrSavitsky, R_BandF, R_CorrBandF])
#     trims.extend([Trim_Savitsky, Trim_CorrSavitsky, Trim_BandF, Trim_CorrBandF])
#     method_names.extend(['Savitsky', 'CorrSavitsky', 'BandF', 'CorrBandF'])

# elif FOILS == 1 and Aero_SprayDrag == 0:
#     R_Savitsky, Trim_Savitsky, Vels_Savitsky = calcular_Savitsky(datos, 7.5, 25.5)
#     R_BandF, Trim_BandF, Vels_BandF = calcular_BlountandFox(datos, 7.5, 25.5)
#     R_SavitskyFoils, L_SavitksyFoils ,Trim_SavitskyFoils, Vels_SavitskyFoils = calcular_Savitsky_foils(datos, file_path, 10, 18.5)
#     R_Foils, L_foils, Vels_Foils = calcular_foils(datos, file_path ,10, 18.5)
#     R_Vuelo, L_Vuelo, Vels_Vuelo = calcular_fase_vuelo(datos, file_path , 18, 25.5)
    
#     velocities.extend([Vels_Savitsky, Vels_BandF, Vels_SavitskyFoils, Vels_Foils, Vels_Vuelo])
#     resistances.extend([R_Savitsky, R_BandF, R_SavitskyFoils, R_Foils, R_Vuelo])
#     trims.extend([Trim_Savitsky, Trim_BandF, Trim_SavitskyFoils, [0]*len(Vels_Foils), [0]*len(Vels_Vuelo)])
#     method_names.extend(['Savitsky', 'BandF', 'SavitskyFoils', 'Foils', 'Vuelo'])

# elif FOILS == 1 and Aero_SprayDrag == 1:
#     R_CorrSavitsky, Trim_CorrSavitsky, Vels_CorrSavitsky = calcular_Savitsky_SprayAero(datos, 7.5, 25.5)
#     R_CorrBandF, Trim_CorrBandF, Vels_CorrBandF = calcular_BandF_SprayAero(datos, 7.5, 25.5)
#     R_Foils, L_foils, Vels_Foils = calcular_foils(datos, file_path ,10, 18.5)
#     R_Vuelo, L_Vuelo, Vels_Vuelo = calcular_fase_vuelo(datos, file_path , 18, 25.5)
    
#     velocities.extend([Vels_CorrSavitsky, Vels_CorrBandF, Vels_Foils, Vels_Vuelo])
#     resistances.extend([R_CorrSavitsky, R_CorrBandF, R_Foils, R_Vuelo])
#     trims.extend([Trim_CorrSavitsky, Trim_CorrBandF, [0]*len(Vels_Foils), [0]*len(Vels_Vuelo)])
#     method_names.extend(['CorrSavitsky', 'CorrBandF', 'Foils', 'Vuelo'])

# elif STEP == 1 and Aero_SprayDrag == 0:
#     R_Savitsky, Trim_Savitsky, Vels_Savitsky = calcular_Savitsky(datos, 7.5, 25.5)
#     R_BandF, Trim_BandF, Vels_BandF = calcular_BlountandFox(datos, 7.5, 25.5)
#     R_Svahn, Trim_Svahn, Vels_Svahn = calcular_Svahn(datos, 18, 25.5)
    
#     velocities.extend([Vels_Savitsky, Vels_BandF, Vels_Svahn])
#     resistances.extend([R_Savitsky, R_BandF, R_Svahn])
#     trims.extend([Trim_Savitsky, Trim_BandF, Trim_Svahn])
#     method_names.extend(['Savitsky', 'BandF', 'Svahn'])

# elif STEP == 1 and Aero_SprayDrag == 1:
#     R_CorrSavitsky, Trim_CorrSavitsky, Vels_CorrSavitsky = calcular_Savitsky_SprayAero(datos, 7.5, 25.5)
#     R_CorrBandF, Trim_CorrBandF, Vels_CorrBandF = calcular_BandF_SprayAero(datos, 7.5, 25.5)
#     R_Svahn, Trim_Svahn, Vels_Svahn = calcular_Svahn(datos, 18, 25.5)
    
#     velocities.extend([Vels_CorrSavitsky, Vels_CorrBandF, Vels_Svahn])
#     resistances.extend([R_CorrSavitsky, R_CorrBandF, R_Svahn])
#     trims.extend([Trim_CorrSavitsky, Trim_CorrBandF, Trim_Svahn])
#     method_names.extend(['CorrSavitsky', 'CorrBandF', 'Svahn'])

# # Save results to txt files
# save_results_to_txt('resistances_and_trims.txt', velocities, resistances, trims)

# # Plot results
# plot_results(velocities, resistances, trims, method_names)

