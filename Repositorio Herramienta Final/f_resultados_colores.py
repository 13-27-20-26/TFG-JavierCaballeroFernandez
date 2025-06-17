import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
# import matplotlib.pyplot as plt

# Function to save results to a txt file
# def results_to_txt(filename, velocities, resistances, trims, lifts = None):
#     with open(filename, 'w') as f:
#         f.write("Velocities:\n")
#         for vels in velocities:
#             f.write(",".join(map(str, vels)) + "\n")
#             f.write("\nResistances:\n")
#         for res in resistances:
#             f.write(",".join(map(str, res)) + "\n")
#             f.write("\nTrims:\n")
#         for trim in trims:
#             f.write(",".join(map(str, trim)) + "\n")
#         if lifts:
#             f.write("\nLifts:\n")
#             for lift in lifts:
#                 f.write(",".join(map(str, lift)) + "\n")

# Function to plot resistances and trims
def plot_results(velocities, resistances, trims, method_names):


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


# def save_to_excel(filename, velocities, resistances, trims, lifts, method_names):
#     """
#     Guarda todos los resultados en una única hoja de Excel.
#     Cada fila contiene el método al que pertenece.
#     """
#     rows = []

#     for i, method in enumerate(method_names):
#         num_points = min(len(velocities[i]), len(resistances[i]), len(trims[i]))
#         for j in range(num_points):
#             row = {
#                 'Método': method,
#                 'Velocidad (kn)': velocities[i][j],
#                 'Resistencia (N)': resistances[i][j],
#                 'Trim (grados)': trims[i][j],
#             }
#             if lifts is not None and i < len(lifts) and j < len(lifts[i]):
#                 row['Sustentación (N)'] = lifts[i][j]
#             rows.append(row)

#     df = pd.DataFrame(rows)
#     df.to_excel(filename, index=False)
