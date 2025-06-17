import pandas as pd

def buscar_AoA(file_path, cl_target, reynolds_target):
    # Load the Excel file
    xls = pd.ExcelFile(file_path)

    # Dictionary to store DataFrames for each Reynolds number
    dfs = {}

    # Iterate through each sheet and store the DataFrame in the dictionary
    for sheet_name in xls.sheet_names:
        reynolds_number = float(sheet_name.replace('x10^6', '')) * 1e6
        dfs[reynolds_number] = pd.read_excel(xls, sheet_name=sheet_name, engine='openpyxl')

    # Function to interpolate between two DataFrames
    def interpolar_dataframes(df_lower, df_upper, reynolds_lower, reynolds_upper, reynolds_target):
        # Select only the columns to be interpolated
        columns_to_interpolate = ['alpha', 'CL', 'CD', 'Cpmin']
        df_lower_interpolate = df_lower[columns_to_interpolate]
        df_upper_interpolate = df_upper[columns_to_interpolate]

        # Perform the interpolation
        interpolated_df = df_lower_interpolate + (df_upper_interpolate - df_lower_interpolate) * ((reynolds_target - reynolds_lower) / (reynolds_upper - reynolds_lower))

        return interpolated_df

    # Function to get interpolated DataFrame for a given Reynolds number
    def interpolar_Re(reynolds_target):
        # Get the Reynolds numbers in sorted order
        reynolds_numbers = sorted(dfs.keys())

        # Find the two Reynolds numbers closest to the target
        reynolds_lower = max([r for r in reynolds_numbers if r <= reynolds_target])
        reynolds_upper = min([r for r in reynolds_numbers if r >= reynolds_target])
        
        # If the target Reynolds number matches exactly with one of the available Reynolds numbers
        if reynolds_lower == reynolds_upper:
            return dfs[reynolds_lower][['alpha', 'CL', 'CD', 'Cpmin']]

        # Get the corresponding DataFrames
        df_lower = dfs[reynolds_lower]
        df_upper = dfs[reynolds_upper]

        # Interpolate between the two DataFrames
        interpolated_df = interpolar_dataframes(df_lower, df_upper, reynolds_lower, reynolds_upper, reynolds_target)

        return interpolated_df

    # Function to interpolate alpha for a given CL in the interpolated DataFrame
    def interpolar_AoA(interpolated_df, cl_target):
        # Sort the DataFrame by CL
        sorted_df = interpolated_df.sort_values(by='CL')

        # Find the two CL values closest to the target
        cl_lower = max([cl for cl in sorted_df['CL'] if cl <= cl_target])
        cl_upper = min([cl for cl in sorted_df['CL'] if cl >= cl_target])

        # Get the corresponding alpha values
        alpha_lower = sorted_df[sorted_df['CL'] == cl_lower]['alpha'].values[0]
        alpha_upper = sorted_df[sorted_df['CL'] == cl_upper]['alpha'].values[0]
        # Check if alpha_lower and alpha_upper are the same to avoid division by zero
        if alpha_lower == alpha_upper:
            return alpha_lower

        # Interpolate to find the alpha for the target CL
        alpha_target = alpha_lower + (alpha_upper - alpha_lower) * ((cl_target - cl_lower) / (cl_upper - cl_lower))

        return alpha_target

    # Get the interpolated DataFrame for the given Reynolds number
    interpolated_df = interpolar_Re(reynolds_target)

    # Get the interpolated alpha for the given CL
    alpha_target = interpolar_AoA(interpolated_df, cl_target)

    return alpha_target

