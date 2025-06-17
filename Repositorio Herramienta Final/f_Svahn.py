import numpy as np
from scipy.optimize import fsolve

def calcular_Svahn(datos, vmin, vmax):
    # Datos Step
    VS = datos['VS']  # m , 0.105
    LS = datos['LS']  # m , 4.244
    phi = datos['phi']  # degrees , 0
    # Datos iniciales
    m = datos['m']  # kg , 2415
    b = datos['b']  # m , 2.589
    Puntal = datos['Puntal']  # m , 1.35
    h_codillo = datos['h_codillo']  # m , 0.5
    LCG2 = datos['LCG']  # m , 4
    LCG1 = LS - LCG2  # m , LS - LCG2
    VCG = datos['VCG']  # m , 0.67
    beta1 = datos['beta']  # degrees , 18
    beta2 = datos['beta2']  # degrees , 18
    epsilon = datos['epsilon']  # degrees , 0
    f = datos['f']  # m , 1.36
    # Constantes
    g = datos['g']  # m/s^2 , 9.81
    rho = datos['rho']  # kg/m^3 , 1025

    # Listas para almacenar los resultados
    R_totales = []
    Trims = []

    # Velocidades
    Vel_nudos = np.arange(vmin, vmax, 0.5)  # knots
    Vel_mps = Vel_nudos * 0.514444  # m/s

    # Bucle para obtener los resultados a distintas velocidades
    for U in Vel_mps:
        # Angles that are covered by the method
        Tau = np.arange(2.5, 6.5, 0.01)  # degrees
        # Omega values covered by the method
        Omega = np.arange(0.5, 0.75, 0.01)
        # Speed Coefficient
        Cv = U / np.sqrt(g * b)

        # Funciones auxiliares para la iteración
        def ClB(x):
            r = Clbeta - x + 0.0065 * beta1 * x**0.6
            return r

        def lam(l):
            q = Cl0 - (tau**1.1) * (0.012 * (l**0.5) + 0.0055 * ((l**2.5) / (Cv**2)))
            return q

        # Bucle de Tau
        for tau in Tau:
            # Bucle de Omega
            for omega in Omega:
                # Cálculos iniciales
                Fl1 = omega * m * g  # N
                Clbeta = Fl1 / (0.5 * rho * U**2 * b**2)  # Coeficiente de sustentación de cuepo de proa
                Cl0 = fsolve(ClB, 0.1)[0]  # Zero-deadrise Cl
                lamda1 = fsolve(lam, 0.1)[0]  # Lambda
                Lk1 = lamda1 * b + (b * np.tan(np.radians(beta1))) / (2 * np.pi * np.tan(np.radians(tau)))  # m

                # Ecuaciones de la teoría de ondas
                X_b4 = 3 * b * ((Cv / np.pi) * np.arcsin((VS + 0.25 * b * (np.tan(np.radians(beta2)) - np.tan(np.radians(beta1)))) / (b * 0.17 * (0.75 + 0.03 * (Lk1 / b) * (tau**1.5)))))**(2 / 3)  # m
                tau2 = 0.085 * (np.pi / Cv) * (0.75 + 0.03 * (Lk1 / b) * tau**1.5) * ((X_b4 / (3 * b))**0.5) * np.cos((np.pi / Cv) * ((X_b4 / (3 * b))**1.5))  # radians
                tau2_degrees = tau2 * (180 / np.pi)  # degrees
                if 0 < beta1 <= 15:
                    Xcl = 3 * b * ((Cv / np.pi) * np.arcsin((VS + np.tan(np.radians(phi))) / (b * 0.17 * (1.5 + 0.03 * (Lk1 / b) * tau**1.5))))**(2 / 3)  # m
                    Hcl = 0.17 * b * (1.5 + 0.03 * (Lk1 / b) * (tau2_degrees**1.5)) * np.sin((np.pi / Cv) * ((X_b4 / (3 * b))**1.5))  # Para x_b4
                else:
                    Xcl = 3 * b * ((Cv / np.pi) * np.arcsin((VS + np.tan(np.radians(phi))) / (b * 0.17 * (2 + 0.03 * (Lk1 / b) * tau**1.5))))**(2 / 3)  # m
                    Hcl = 0.17 * b * (2 + 0.03 * (Lk1 / b) * (tau2_degrees**1.5)) * np.sin((np.pi / Cv) * ((X_b4 / (3 * b))**1.5))  # Para x_b4

                H_b4 = VS + 0.25 * b * (np.tan(np.radians(beta2)) - np.tan(np.radians(beta1))) + X_b4 * np.tan(np.radians(phi))  # m
                beta2l = beta2 * (np.pi / 180) - np.arctan(H_b4 + 0.25 * b * np.tan(np.radians(beta1)) - Hcl) / (0.25 * b)  # radians
                beta2l_degrees = beta2l * (180 / np.pi)  # degrees
                L2_2 = 2 * (X_b4 - Xcl) / np.cos(np.radians(phi))  # m
                Lk2 = LS - (Xcl / np.cos(np.radians(phi)))  # m
                b2l = (2 * L2_2 * np.tan(tau2)) / np.tan(beta2l)  # m
                Ll2 = (b2l / np.pi) * (np.tan(beta2l) / np.tan(tau2))  # m
                lamda2 = (Lk2 / b2l) - (Ll2 / (2 * b2l))  # Lambda

                # Coeficiente de sustentación del segundo step
                Cv2 = U / np.sqrt(g * b2l)  # Coeficiente de velocidad para el cuerpo de popa
                Cl0_2 = tau2_degrees * (0.012 * (np.sqrt(lamda2)) + 0.0055 * ((lamda2**2.5) / (Cv2**2)))
                Clbeta_2 = Cl0_2 - 0.0065 * beta2l_degrees * (Cl0_2**0.6)  # Coeficiente de sustentación del cuerpo de popa
                Fl2l = Clbeta_2 * (0.5 * rho * U**2 * b2l**2) * np.cos(np.radians(beta2 - beta2l_degrees))  # N
                Fl2 = Fl2l * np.cos(np.radians(tau - tau2_degrees))  # N

                # Ecuación de equilibrio vertical
                Eq_Vert = Fl1 + Fl2 - m * g  # N
                if abs(Eq_Vert) < 500:
                    break
                else:
                    continue

            # Cálculo del trimado
            a1 = VCG - (b / 4) * np.tan(np.radians(beta1))  # m
            a2 = VCG - (b2l / 4) * np.tan(np.radians(beta2))  # m
            Cp1 = 0.75 - (1 / (2.39 + 5.21 * (Cv / lamda1)**2))
            Cp2 = 0.75 - (1 / (2.39 + 5.21 * (Cv2 / lamda2)**2))
            lp1 = Cp1 * lamda1 * b  # m
            lp2 = Cp2 * lamda2 * b2l  # m
            c1 = lp1 + LCG1  # m
            c2 = LCG2 - lp2  # m

            # Drag de fricción
            Re1 = (U * b * lamda1) / (1e-6)  # Reynolds number for the first step
            Re2 = (U * b2l * lamda2 + U * b * lamda1) / (1e-6)  # Reynolds number for the second step
            Am1 = lamda1 * b**2 / np.cos(np.radians(beta1))  # m^2
            Am2 = lamda2 * b2l**2 / np.cos(np.radians(beta2))  # m^2
            Cf1 = 0.075 / (np.log10(Re1) - 2)**2  # Friction coefficient for the first step
            Cf2 = 0.075 / (np.log10(Re2) - 2)**2  # Coeficiente de fricción para el segundo step
            Crough = 0.0004  # Coeficiente de rugosidad
            Df1 = (Cf1 + Crough) * 0.5 * rho * U**2 * Am1  # Drag de fricción para el primer step
            Df2 = (Cf2 + Crough) * 0.5 * rho * U**2 * Am2  # Drag de fricción para el segundo step

            # Ecuaciones de equilibrio
            N1 = omega * m * g  # N ; Fuerza normal para el primer step
            N2 = (1 - omega) * m * g  # N ; Fuerza normal para el segundo step
            T = (Df1 * np.cos(np.radians(tau)) + Df2 * np.cos(np.radians(tau2_degrees)) + N1 * np.sin(np.radians(tau)) + N2 * np.sin(np.radians(tau2_degrees))) / np.cos(np.radians(tau + epsilon))  # N ; Empuje total
            momentum = N2 * c2 - N1 * c1 + Df1 * a1 + Df2 * a2 - T * f  # m ; Ecuación de momento

            if abs(momentum) < 1000:  # N*m
                Rt = T * np.cos(np.radians(tau + epsilon))  # N
                break
            else:
                continue

        # Añadimos el Drag Aerodinámico
        Cd_aero = 0.8  # entre 0.5 y 1.2
        rho_aire = 1.204  # kg/m^3
        Af = b * (Puntal - h_codillo)  # m^2 ; Área frontal del casco
        D_aero = 0.5 * rho_aire * U**2 * Af * Cd_aero  # N ; Drag aerodinámico
        R_total = Rt + D_aero  # N ; Resistencia total

        R_totales.append(R_total)  # Añadir el resultado a la lista
        Trims.append(tau)  # Añadir el trimado a la lista

    return R_totales, Trims, Vel_nudos
