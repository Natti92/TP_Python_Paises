
# CONSTANTE

ARCHIVO_CSV = "paises.csv"


# CARGA DE DATOS DESDE ARCHIVO

def cargar_paises():
    paises = []

    try:
        with open(ARCHIVO_CSV, "r", encoding="utf-8") as archivo:
            # Descartamos la primera línea que es el encabezado
            archivo.readline()

            for linea in archivo:
                linea = linea.strip()
                if linea == "":
                    continue

                datos = linea.split(",")

                if len(datos) == 4:
                    nombre = datos[0].strip()
                    poblacion_str = datos[1].strip()
                    superficie_str = datos[2].strip()
                    continente = datos[3].strip()

                    # Validación: Evitamos agregar si hay algún campo vacío
                    if nombre == "" or poblacion_str == "" or superficie_str == "" or continente == "":
                        continue

                    try:
                        poblacion = int(poblacion_str)
                        superficie = int(superficie_str)

                        # Validación: No permitimos números negativos
                        if poblacion >= 0 and superficie >= 0:
                            paises.append({
                                "nombre": nombre,
                                "poblacion": poblacion,
                                "superficie": superficie,
                                "continente": continente
                            })
                    except ValueError:
                        continue
    except FileNotFoundError:
        # Si el archivo no existe, arrancamos con la lista vacía
        return paises
    except Exception:
        print("Error al procesar los datos del archivo.")

    return paises



# GUARDADO DE DATOS A ARCHIVO #

def guardar_paises(paises):
    """Guarda la lista completa de países en paises.csv - Hoja 1.csv usando operaciones simples de escritura."""
    try:
        with open(ARCHIVO_CSV, "w", encoding="utf-8") as archivo:
            # Escribimos la cabecera del archivo
            archivo.write("NOMBRE,POBLACION,SUPERFICIE,CONTINENTE\n")
            
            # Escribimos cada país
            for pais in paises:
                archivo.write(f"{pais['nombre']},{pais['poblacion']},{pais['superficie']},{pais['continente']}\n")
                
        print(f"Datos guardados con éxito en '{ARCHIVO_CSV}'.")
    except Exception:
        print("Ocurrió un error al guardar los datos en el archivo.")



# VALIDACIONES DE ENTRADA
def leer_cadena_no_vacia(mensaje):
    """Solicita una entrada de texto y reintenta hasta que no sea vacía."""
    while True:
        entrada = input(mensaje).strip()
        if entrada != "":
            return entrada
        print("Error: Este campo no puede quedar vacío. Por favor, ingresá un valor.")


def leer_entero_positivo(mensaje):
    """Solicita una entrada numérica y reintenta hasta obtener un entero >= 0."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= 0:
                return valor
            print("Error: El número debe ser mayor o igual a cero.")
        except ValueError:
            print("Error: Debés ingresar un número entero válido.")



# MOSTRAR PAISES #

def mostrar_paises(lista):
    if len(lista) == 0:
        print("No hay datos para mostrar.")
        return

    for pais in lista:
        print("-" * 50)
        print("Nombre:", pais["nombre"])
        print("Población:", pais["poblacion"])
        print("Superficie:", pais["superficie"])
        print("Continente:", pais["continente"])



# AGREGAR PAIS #

def agregar_pais(paises):
    print("\n--- Agregar Nuevo País ---")
    nombre = leer_cadena_no_vacia("Nombre del país: ")

    # Comprobamos si el país ya existe (insensible a mayúsculas/minúsculas)
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            print(f"Error: El país '{nombre}' ya existe.")
            return

    poblacion = leer_entero_positivo("Población: ")
    superficie = leer_entero_positivo("Superficie: ")
    continente = leer_cadena_no_vacia("Continente: ")

    nuevo = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

    paises.append(nuevo)
    print("País agregado correctamente.")
    
    # Persistimos inmediatamente en el archivo
    guardar_paises(paises)


# ACTUALIZAR #
def actualizar_pais(paises):
    print("\n--- Actualizar País ---")
    nombre = input("Ingrese el país a actualizar: ").strip().lower()

    for pais in paises:
        if pais["nombre"].lower() == nombre:
            print(f"País encontrado: {pais['nombre']}.")
            pais["poblacion"] = leer_entero_positivo("Nueva población: ")
            pais["superficie"] = leer_entero_positivo("Nueva superficie: ")
            print("Datos actualizados localmente.")
            
            # Guardamos los cambios inmediatamente
            guardar_paises(paises)
            return

    print("Error: País no encontrado.")


# BUSCAR #

def buscar_pais(paises):
    print("\n--- Buscar País ---")
    texto = input("Ingrese nombre a buscar (coincidencia parcial o exacta): ").strip().lower()

    if texto == "":
        print("Error: Debe ingresar un texto de búsqueda.")
        return

    encontrados = []
    for pais in paises:
        if texto in pais["nombre"].lower():
            encontrados.append(pais)

    if len(encontrados) > 0:
        print(f"\nSe encontraron {len(encontrados)} resultados:")
        mostrar_paises(encontrados)
    else:
        print("No se encontraron resultados para la búsqueda.")



# FILTRAR CONTINENTE #

def filtrar_continente(paises):
    continente = input("Continente: ").strip().lower()
    if continente == "":
        print("Error: El continente a filtrar no puede estar vacío.")
        return

    resultado = []
    for pais in paises:
        if pais["continente"].lower() == continente:
            resultado.append(pais)

    if len(resultado) > 0:
        # .title() pone la primera letra en mayúscula
        print(f"\nPaíses en el continente '{continente.title()}':")
        mostrar_paises(resultado)
    else:
        print(f"No se encontraron países en el continente '{continente.title()}'.")



# FILTRAR POBLACION 

def filtrar_poblacion(paises):
    print("\n--- Filtrar por Rango de Población ---")
    minimo = leer_entero_positivo("Población mínima: ")
    while True:
        maximo = leer_entero_positivo("Población máxima: ")
        if maximo >= minimo:
            break
        print(f"Error: La población máxima ({maximo}) debe ser mayor o igual a la mínima ({minimo}).")

    resultado = []
    for pais in paises:
        if minimo <= pais["poblacion"] <= maximo:
            resultado.append(pais)

    if len(resultado) > 0:
        print(f"\nPaíses con población entre {minimo} y {maximo}:")
        mostrar_paises(resultado)
    else:
        print("No se encontraron países en ese rango de población.")



# FILTRAR SUPERFICIE #

def filtrar_superficie(paises):
    print("\n--- Filtrar por Rango de Superficie ---")
    minimo = leer_entero_positivo("Superficie mínima: ")
    while True:
        maximo = leer_entero_positivo("Superficie máxima: ")
        if maximo >= minimo:
            break
        print(f"Error: La superficie máxima ({maximo}) debe ser mayor o igual a la mínima ({minimo}).")

    resultado = []
    for pais in paises:
        if minimo <= pais["superficie"] <= maximo:
            resultado.append(pais)

    if len(resultado) > 0:
        print(f"\nPaíses con superficie entre {minimo} y {maximo}:")
        mostrar_paises(resultado)
    else:
        print("No se encontraron países en ese rango de superficie.")



# ORDENAR #

# Funciones simples para indicarle a sorted() por qué columna ordenar:
def obtener_nombre(pais):
    return pais["nombre"].lower()

def obtener_poblacion(pais):
    return pais["poblacion"]

def obtener_superficie(pais):
    return pais["superficie"]


def ordenar_nombre(paises):
    opcion = input("A Ascendente / D Descendente: ").strip().upper()
    reversa = True if opcion == "D" else False

    # Ordenamos usando la función obtener_nombre
    ordenados = sorted(paises, key=obtener_nombre, reverse=reversa)
    mostrar_paises(ordenados)


def ordenar_poblacion(paises):
    opcion = input("A Ascendente / D Descendente: ").strip().upper()
    reversa = True if opcion == "D" else False

    # Ordenamos usando la función obtener_poblacion
    ordenados = sorted(paises, key=obtener_poblacion, reverse=reversa)
    mostrar_paises(ordenados)


def ordenar_superficie(paises):
    opcion = input("A Ascendente / D Descendente: ").strip().upper()
    reversa = True if opcion == "D" else False

    # Ordenamos usando la función obtener_superficie
    ordenados = sorted(paises, key=obtener_superficie, reverse=reversa)
    mostrar_paises(ordenados)




# ESTADISTICAS #

def mostrar_estadisticas(paises):
    if len(paises) == 0:
        print("\nNo hay datos cargados para calcular estadísticas.")
        return

    mayor = max(paises, key=obtener_poblacion)
    menor = min(paises, key=obtener_poblacion)

    suma_poblacion = 0
    suma_superficie = 0
    continentes = {}

    for pais in paises:
        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        # Normalizamos el continente para evitar duplicados (ej: "Oceania" y "oceania")
        cont = pais["continente"].strip().title()

        if cont in continentes:
            continentes[cont] += 1
        else:
            continentes[cont] = 1

    promedio_poblacion = suma_poblacion / len(paises)
    promedio_superficie = suma_superficie / len(paises)

    print("\n" + "=" * 40)
    print("ESTADÍSTICAS DEL SISTEMA")
    print("=" * 40)
    print(f"País con mayor población: {mayor['nombre']} ({mayor['poblacion']} hab.)")
    print(f"País con menor población: {menor['nombre']} ({menor['poblacion']} hab.)")
    print(f"Promedio de población:    {round(promedio_poblacion, 2)} hab.")
    print(f"Promedio de superficie:   {round(promedio_superficie, 2)} km²")
    print("\nCantidad de países por continente:")
    for continente in continentes:
        cantidad = continentes[continente]
        print(f" - {continente}: {cantidad}")
    print("=" * 40)



# MENU FILTROS #
def menu_filtros(paises):
    if len(paises) == 0:
        print("No hay países disponibles para filtrar.")
        return

    print("\n--- Opciones de Filtrado ---")
    print("1. Por continente")
    print("2. Por población")
    print("3. Por superficie")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        filtrar_continente(paises)
    elif opcion == "2":
        filtrar_poblacion(paises)
    elif opcion == "3":
        filtrar_superficie(paises)
    else:
        print("Error: Opción inválida.")



# MENU ORDENAR #

def menu_ordenar(paises):
    if len(paises) == 0:
        print("No hay países disponibles para ordenar.")
        return

    print("\n--- Opciones de Ordenamiento ---")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        ordenar_nombre(paises)
    elif opcion == "2":
        ordenar_poblacion(paises)
    elif opcion == "3":
        ordenar_superficie(paises)
    else:
        print("Error: Opción inválida.")



# MENU PRINCIPAL#

def menu():
    paises = cargar_paises()
    if len(paises) > 0:
        print(f"Se cargaron {len(paises)} países correctamente.")
    else:
        print("El sistema inició sin datos cargados.")

    while True:
        print("\n===== GESTIÓN DE PAÍSES =====")
        print("1. Agregar país")
        print("2. Actualizar país")
        print("3. Buscar país")
        print("4. Filtrar países")
        print("5. Ordenar países")
        print("6. Estadísticas")
        print("7. Mostrar todos")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_pais(paises)
        elif opcion == "2":
            actualizar_pais(paises)
        elif opcion == "3":
            buscar_pais(paises)
        elif opcion == "4":
            menu_filtros(paises)
        elif opcion == "5":
            menu_ordenar(paises)
        elif opcion == "6":
            mostrar_estadisticas(paises)
        elif opcion == "7":
            print("\nLista completa de países:")
            mostrar_paises(paises)
        elif opcion == "0":
            print("Fin del programa. ¡Hasta luego!")
            break
        else:
            print("Error: Opción inválida.")


# ==========================
# INICIO
# ==========================
if __name__ == "__main__":
    menu()