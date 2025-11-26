# Compilación del módulo `busqueda` (pybind11)

Instrucciones simples para compilar e instalar la extensión C++ (`busqueda`) usada por `main.py`.

Requisitos mínimos
- Windows con Python 3.x instalado.
- `pip` disponible.
- Visual Studio Build Tools (MSVC) con el workload "Desktop development with C++" instalado. Si no lo tiene, instale "Build Tools for Visual Studio".

Pasos (PowerShell)

1. Abra PowerShell en la carpeta del proyecto (la que contiene `setup.py`). Por ejemplo:

```powershell
cd "C:\Users\artur\Downloads\proyecto final_ Permutas Naive\proyecto final_ Permutas Naive"
```

2. Instale/actualice las dependencias de construcción:

```powershell
python -m pip install --upgrade pip setuptools wheel pybind11
```

3. Compile la extensión (comando fiable en PowerShell):

```powershell
python .\setup.py build_ext --inplace
```

Uso después de compilar
- Si la compilación fue correcta, en la carpeta aparecerá un archivo `busqueda*.pyd`. Puede ejecutar `main.py` que importa `busqueda` normalmente:

```powershell
python .\main.py
```

## Error de certificacion
SSL y `certifi`
- Si al ejecutar `main.py` obtiene errores de certificado SSL, agregue este snippet al inicio de `main.py` (luego de `import os`):

```python
try:
		import certifi
		import os
		os.environ['SSL_CERT_FILE'] = certifi.where()
except Exception:
		# If certifi is not available yet, instale con:
		# python -m pip install certifi
		pass
```

- Para instalar `certifi`:

```powershell
python -m pip install certifi
```

## Problema de imagen (`adn.png`) 
— dónde cambiar la ruta
- El archivo `main.py` carga una imagen con `tk.PhotoImage(...)`. Busque la línea que asigna `img_adn`, por ejemplo:

```python
img_adn = tk.PhotoImage(file="C:\\Users\\migue\\Desktop\\proyectoFinal2\\adn.png").subsample(20,20)
```
- Como hacer que el programa encuentre la imagen:
	- Como adn ya esta en la carpeta del proyecto (la misma que contiene `main.py`) solo habra que cambiar la línea anterior a:

		```python
		img_adn = tk.PhotoImage(file="adn.png").subsample(20,20)
		```
# Como usarlo:

- Interfaz inicial:

	<img width="370" height="267" alt="image" src="https://github.com/user-attachments/assets/fac8f577-8808-41d5-b1fc-8585b31c5fe0" />
- Ingresar un patron:

  	<img width="370" height="267" alt="image" src="https://github.com/arturomartinez8970-cpu/Equipo-Permutas-Naive/blob/main/src/Proyecto-Final-Permutas-Naive/img/Captura%20de%20pantalla%202025-11-25%20032741.png?raw=true" />

- Primer patron guardado:

  <img width="370" height="267" alt="image" src="https://github.com/arturomartinez8970-cpu/Equipo-Permutas-Naive/blob/main/src/Proyecto-Final-Permutas-Naive/img/Captura%20de%20pantalla%202025-11-25%20032748.png?raw=true" />

- El programa no te deja hacer permutas hasta tener 3 patrones guardados:

  <img width="370" height="267" alt="image" src="https://github.com/arturomartinez8970-cpu/Equipo-Permutas-Naive/blob/main/src/Proyecto-Final-Permutas-Naive/img/Captura%20de%20pantalla%202025-11-25%20032757.png?raw=true" />

- Después de presionar el botón de generar permutas se agregan símbolos de más a las cadenas de ADN:

  <img width="370" height="267" alt="image" src="https://github.com/arturomartinez8970-cpu/Equipo-Permutas-Naive/blob/main/src/Proyecto-Final-Permutas-Naive/img/Captura%20de%20pantalla%202025-11-25%20032805.png?raw=true" />

- Al darles click se muestran las permutas:

  <img width="370" height="267" alt="image" src="https://github.com/arturomartinez8970-cpu/Equipo-Permutas-Naive/blob/main/src/Proyecto-Final-Permutas-Naive/img/Captura%20de%20pantalla%202025-11-25%20032813.png?raw=true" />

- Puedes darle click a la permuta que quieras para buscar una permuta en la secuencia de ADN:

  <img width="370" height="267" alt="image" src="https://github.com/arturomartinez8970-cpu/Equipo-Permutas-Naive/blob/main/src/Proyecto-Final-Permutas-Naive/img/Captura%20de%20pantalla%202025-11-25%20032821.png?raw=true" />

- Al darle click aparecerá en una nueva ventana la secuencia de ADN con texto subrayado donde encontró dicha permuta o patron de adn:

  <img width="370" height="267" alt="image" src="https://github.com/arturomartinez8970-cpu/Equipo-Permutas-Naive/blob/main/src/Proyecto-Final-Permutas-Naive/img/Captura%20de%20pantalla%202025-11-25%20032838.png?raw=true" />

- Y la información en la tabla de patrones cambiara a los resultados que obtuvo la búsqueda:

  <img width="370" height="267" alt="image" src="https://github.com/arturomartinez8970-cpu/Equipo-Permutas-Naive/blob/main/src/Proyecto-Final-Permutas-Naive/img/Captura%20de%20pantalla%202025-11-25%20032848.png?raw=true" />

  - Fin del algoritmo
