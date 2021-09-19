## DEFINIMOS PARÁMETROS PARA LA SIMULACIÓN
numero_vesiculas = 10000

# Constantes cinéticas
alpha = 1.43
rho = 1.0
# lamda: Proporción entre alphas y betas
lamda = 100
beta = alpha * lamda

# Definimos las constantes temporales medidos en segundos
tiempo_final = 1.00
tiempo_impresion = 0.0001
tau_estimulacion = 0.001
tiempo_inicio_estimulacion = 0.1

# Número de estimulos condicionales
numero_estimulos_condicionales = 3
intensidad_estimulo = 500

# Periodo entre los estimulos condicionales
periodo = 0.03

# Tiempo de espera entre el último estímulo condicional y el estímulo test
tiempo_espera_test = 0.1
