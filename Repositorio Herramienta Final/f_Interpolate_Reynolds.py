import pandas as pd
import numpy as np

def interpolate_Reynolds(file_path, Re_values, alphas):
    # Cargar archivo Excel
    Epler817 = pd.ExcelFile(file_path, engine='openpyxl')
    dfs = {
        sheet_name: pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')[['alpha', 'CL', 'CD', 'CDp', 'Cpmin']]
        for sheet_name in Epler817.sheet_names
    }

    # Mapeo entre valores numéricos de Reynolds y nombres de hojas
    re_mapping = {
        0.75e6: '0.75x10^6',
        1.0e6: '1x10^6',
        1.25e6: '1.25x10^6',
        1.5e6: '1.5x10^6',
        1.75e6: '1.75x10^6',
        2.0e6: '2x10^6',
        2.25e6: '2.25x10^6',
        2.5e6: '2.5x10^6',
        2.75e6: '2.75x10^6',
        3.0e6: '3x10^6',
        3.25e6: '3.25x10^6',
        3.5e6: '3.5x10^6'
    }

    def get_inferior_superior_dfs(Re):
        Re_keys = sorted(re_mapping.keys())

        # Verifica que Re esté dentro del rango
        if Re < Re_keys[0] or Re > Re_keys[-1]:
            raise ValueError(f"Reynolds {Re} está fuera del rango disponible ({Re_keys[0]} - {Re_keys[-1]})")

        # Buscar los dos valores más cercanos
        Re_inf = max([re for re in Re_keys if re <= Re], default=None)
        Re_sup = min([re for re in Re_keys if re >= Re], default=None)

        if Re_inf is None or Re_sup is None:
            raise ValueError(f"No se encontraron valores de Reynolds adecuados para interpolar con Re = {Re}")

        return dfs[re_mapping[Re_inf]], dfs[re_mapping[Re_sup]], Re_inf, Re_sup



    def interpolate_cl_cd(alpha, df_inf, df_sup, Re_inf, Re_sup, Re):
        cl_inf = np.interp(alpha, df_inf['alpha'], df_inf['CL'])
        cd_inf = np.interp(alpha, df_inf['alpha'], df_inf['CD'])
        cl_sup = np.interp(alpha, df_sup['alpha'], df_sup['CL'])
        cd_sup = np.interp(alpha, df_sup['alpha'], df_sup['CD'])
        cl = np.interp(Re, [Re_inf, Re_sup], [cl_inf, cl_sup])
        cd = np.interp(Re, [Re_inf, Re_sup], [cd_inf, cd_sup])
        return cl, cd
    cl_list = []
    cd_list = []
    for Re, alpha in zip(Re_values, alphas):
        df_inf, df_sup, Re_inf, Re_sup = get_inferior_superior_dfs(Re)
        cl, cd = interpolate_cl_cd(alpha, df_inf, df_sup, Re_inf, Re_sup, Re)
        cl_list.append(cl)
        cd_list.append(cd)

    return cl_list, cd_list

