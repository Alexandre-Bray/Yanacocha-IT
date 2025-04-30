Procesamiento y Visualización de Datos Experimentales / Experiment Data Processing and Visualization
Resumen / Overview
Español: Este proyecto procesa datos experimentales de experimentos de filtración por membranas en el sitio YANACOCHA/data. El código carga datos de experimentos, aplica correcciones de conductividad y/o temperatura a las mediciones de presión del concentrado y genera gráficos de caja de los valores de presión corregidos al 30% de recuperación. El proyecto está escrito en Python y utiliza bibliotecas como Pandas y Matplotlib, junto con módulos personalizados (misc, preprocessing, integrity).English: This project processes experimental data from membrane filtration experiments at the YANACOCHA/data site. The code loads experiment data, applies conductivity and/or temperature corrections to concentrate pressure measurements, and generates boxplot visualizations of the corrected pressure values at 30% recovery. The project is written in Python and uses libraries such as Pandas and Matplotlib, along with custom modules (misc, preprocessing, integrity).
Prerrequisitos / Prerequisites
Español: Para ejecutar este proyecto en un sistema Windows, necesitas instalar lo siguiente:  

Python 3.8 o superior  
Visual Studio Code (IDE recomendado)  
Bibliotecas de Python requeridas  
Git (opcional, para clonar el repositorio)

English: To run this project on a Windows system, you need to install the following:  

Python 3.8 or higher  
Visual Studio Code (recommended IDE)  
Required Python libraries  
Git (optional, for cloning the repository)

Instrucciones de Instalación / Installation Instructions
1. Instalar Python / Install Python
Español:  

Descargar Python:  
Visita el sitio oficial de Python.  
Descarga la última versión de Python (por ejemplo, Python 3.11) para Windows.  
Selecciona el instalador ejecutable (por ejemplo, python-3.11.x.exe).


Instalar Python:  
Ejecuta el instalador descargado.  
Marca la casilla "Add Python to PATH" en la parte inferior de la ventana del instalador.  
Selecciona "Install Now" y sigue las instrucciones.  
Verifica la instalación abriendo un Símbolo del Sistema (cmd) y ejecutando:  python --version

Deberías ver la versión instalada (por ejemplo, Python 3.11.x).


Instalar pip (gestor de paquetes de Python):  
Pip está incluido con Python 3.4+. Verifícalo ejecutando:  pip --version


Si pip no está instalado, descarga get-pip.py desde el sitio oficial de pip y ejecuta:  python get-pip.py





English:  

Download Python:  
Visit the official Python website.  
Download the latest Python version (e.g., Python 3.11) for Windows.  
Choose the executable installer (e.g., python-3.11.x.exe).


Install Python:  
Run the downloaded installer.  
Check the box "Add Python to PATH" at the bottom of the installer window.  
Select "Install Now" and follow the prompts.  
Verify the installation by opening a Command Prompt (cmd) and running:  python --version

You should see the installed Python version (e.g., Python 3.11.x).


Install pip (Python package manager):  
Pip is included with Python 3.4+. Verify it by running:  pip --version


If pip is not installed, download get-pip.py from pip's official site and run:  python get-pip.py





2. Instalar Visual Studio Code / Install Visual Studio Code
Español:  

Descargar VS Code:  
Visita el sitio web de VS Code.  
Haz clic en "Download for Windows" para descargar el instalador.


Instalar VS Code:  
Ejecuta el instalador descargado (por ejemplo, VSCodeUserSetup-x64-x.x.x.exe).  
Sigue las instrucciones, aceptando las configuraciones predeterminadas.  
Opcionalmente, marca "Add to PATH" y "Register Code as an editor for supported file types" durante la instalación.


Instalar la Extensión de Python:  
Abre VS Code.  
Ve a la vista de Extensiones (Ctrl+Shift+X).  
Busca "Python" de Microsoft y haz clic en Instalar.  
Opcionalmente, instala la extensión Jupyter para trabajar con archivos .ipynb:  
Busca "Jupyter" de Microsoft y haz clic en Instalar.





English:  

Download VS Code:  
Visit the VS Code website.  
Click "Download for Windows" to download the installer.


Install VS Code:  
Run the downloaded installer (e.g., VSCodeUserSetup-x64-x.x.x.exe).  
Follow the prompts, accepting the default settings.  
Optionally, check "Add to PATH" and "Register Code as an editor for supported file types" during installation.


Install Python Extension:  
Open VS Code.  
Go to the Extensions view (Ctrl+Shift+X).  
Search for "Python" by Microsoft and click Install.  
Optionally, install the Jupyter extension for working with .ipynb files:  
Search for "Jupyter" by Microsoft and click Install.





3. Clonar el Repositorio / Clone the Repository
Español:  

Instalar Git (si no está instalado):  
Descarga Git desde git-scm.com.  
Ejecuta el instalador, aceptando las configuraciones predeterminadas.  
Verifica la instalación ejecutando en el Símbolo del Sistema:  git --version




Clonar el Repositorio:  
Abre el Símbolo del Sistema y navega a tu directorio deseado:  cd C:\ruta\a\tu\carpeta


Clona el repositorio (reemplaza <repository-url> con la URL real de Git):  git clone <repository-url>


Navega al directorio del proyecto:  cd <nombre-del-repositorio>



Nota: Si no usas Git, puedes descargar el proyecto como un archivo ZIP desde la plataforma de alojamiento del repositorio (por ejemplo, GitHub) y extraerlo en una carpeta.


English:  

Install Git (if not already installed):  
Download Git from git-scm.com.  
Run the installer, accepting default settings.  
Verify installation by running in Command Prompt:  git --version




Clone the Repository:  
Open Command Prompt and navigate to your desired directory:  cd C:\path\to\your\folder


Clone the repository (replace <repository-url> with the actual Git URL):  git clone <repository-url>


Navigate to the project directory:  cd <repository-name>



Note: If you don't use Git, you can download the project as a ZIP file from the repository's hosting platform (e.g., GitHub) and extract it to a folder.


4. Instalar Dependencias / Install Dependencies
Español:  

Crear un Entorno Virtual (recomendado para aislar dependencias):  
En el Símbolo del Sistema, navega al directorio del proyecto:  cd C:\ruta\a\tu\proyecto


Crea un entorno virtual:  python -m venv venv


Activa el entorno virtual:  venv\Scripts\activate

Deberías ver (venv) en tu prompt.


Instalar Bibliotecas Requeridas:  
Con el entorno virtual activado, instala las bibliotecas necesarias:  pip install pandas matplotlib


Nota: Los módulos personalizados (misc, preprocessing, integrity) son archivos Python incluidos en el repositorio. Asegúrate de que estén presentes en el directorio del proyecto.


Verificar Instalación:  
Ejecuta lo siguiente para verificar los paquetes instalados:  pip list

Deberías ver pandas, matplotlib y sus dependencias listadas.



English:  

Create a Virtual Environment (recommended to isolate dependencies):  
In Command Prompt, navigate to the project directory:  cd C:\path\to\your\project


Create a virtual environment:  python -m venv venv


Activate the virtual environment:  venv\Scripts\activate

You should see (venv) in your prompt.


Install Required Libraries:  
With the virtual environment activated, install the required libraries:  pip install pandas matplotlib


Note: The custom modules (misc, preprocessing, integrity) are Python files included in the repository. Ensure these files are present in the project directory.


Verify Installation:  
Run the following to check installed packages:  pip list

You should see pandas, matplotlib, and their dependencies listed.



5. Configurar VS Code para el Proyecto / Set Up VS Code for the Project
Español:  

Abrir el Proyecto en VS Code:  
Abre VS Code.  
Ve a Archivo > Abrir Carpeta y selecciona el directorio del proyecto (por ejemplo, C:\ruta\a\tu\proyecto).


Seleccionar el Intérprete de Python:  
Abre la Paleta de Comandos (Ctrl+Shift+P).  
Escribe y selecciona "Python: Select Interpreter".  
Elige el intérprete de Python del entorno virtual (por ejemplo, .\venv\Scripts\python.exe).


Configurar Jupyter (si usas cuadernos):  
Si trabajas con archivos .ipynb, asegúrate de que la extensión Jupyter esté instalada (ver paso 2.3).  
Instala el paquete Jupyter en el entorno virtual:  pip install jupyter


Prueba abriendo un archivo .ipynb en VS Code. Si encuentras un error de webview, consulta la sección de solución de problemas.



English:  

Open the Project in VS Code:  
Open VS Code.  
Go to File > Open Folder and select the project directory (e.g., C:\path\to\your\project).


Select Python Interpreter:  
Open the Command Palette (Ctrl+Shift+P).  
Type and select "Python: Select Interpreter".  
Choose the Python interpreter from the virtual environment (e.g., .\venv\Scripts\python.exe).


Configure Jupyter (if using notebooks):  
If working with .ipynb files, ensure the Jupyter extension is installed (see step 2.3).  
Install the Jupyter package in the virtual environment:  pip install jupyter


Test by opening a .ipynb file in VS Code. If you encounter a webview error, see the troubleshooting section.



Ejecutar el Código / Running the Code
Español:  

Asegurar Dependencias:  
Verifica que los módulos misc, preprocessing y integrity estén presentes en el directorio del proyecto.  
Confirma que los datos experimentales (directorios bajo YANACOCHA/data) sean accesibles. Actualiza la variable site en el código si los datos están en otra ubicación.


Ejecutar el Script:  
Abre el script principal de Python (por ejemplo, main.py) en VS Code.  
Haz clic en el botón Ejecutar (ícono de triángulo) o presiona F5 para ejecutar.  
Alternativamente, ejecuta desde el Símbolo del Sistema con el entorno virtual activado:  python main.py




Salida Esperada:  
Un gráfico de caja que visualiza la distribución de los valores de presión del concentrado corregidos al 30ucionales si la carga o el procesamiento de datos fallan.



English:  

Ensure Dependencies:  
Verify that the misc, preprocessing, and integrity modules are present in the project directory.  
Confirm that the experiment data (directories under YANACOCHA/data) are accessible. Update the site variable in the code if the data is stored elsewhere.


Run the Script:  
Open the main Python script (e.g., main.py) in VS Code.  
Click the Run button (triangle icon) or press F5 to execute.  
Alternatively, run from Command Prompt with the virtual environment activated:  python main.py




Expected Output:  
A boxplot visualizing the distribution of corrected concentrate pressure values at 30% recovery for each experiment.  
Console output may include error messages if data loading or processing fails.



Solución de Problemas / Troubleshooting
Español:  

Error de Webview en VS Code (por ejemplo, "Error loading webview: Could not register service worker"):  
Cierra todas las instancias de VS Code y finaliza los procesos code.exe en el Administrador de Tareas (Ctrl+Shift+Esc).  
Limpia la caché de VS Code:  del %APPDATA%\Code\Cache\*
del %APPDATA%\Code\CachedData\*


Reinicia VS Code e intenta de nuevo.  
Si el problema persiste, ejecuta VS Code en modo sin sandbox:  code . --no-sandbox




Módulo No Encontrado (por ejemplo, misc, preprocessing, integrity):  
Asegúrate de que estos archivos Python estén en el directorio del proyecto.


Datos No Encontrados:  
Verifica que los directorios de datos experimentales existan y sean accesibles en la ruta especificada en la variable site (YANACOCHA/data).  
Actualiza la ruta de site en el código si es necesario.


Problemas con la Ruta de Python:  
Si VS Code no encuentra el intérprete de Python, vuelve a seleccionarlo usando Python: Select Interpreter en la Paleta de Comandos.  
Asegúrate de que el entorno virtual esté activado antes de ejecutar el script.



English:  

Webview Error in VS Code (e.g., "Error loading webview: Could not register service worker"):  
Close all VS Code instances and end code.exe processes in Task Manager (Ctrl+Shift+Esc).  
Clear the VS Code cache:  del %APPDATA%\Code\Cache\*
del %APPDATA%\Code\CachedData\*


Restart VS Code and try again.  
If the issue persists, run VS Code in no-sandbox mode:  code . --no-sandbox




Module Not Found (e.g., misc, preprocessing, integrity):  
Ensure these Python files are in the project directory.


Data Not Found:  
Verify that the experiment data directories exist and are accessible at the path specified in the site variable (YANACOCHA/data).  
Update the site path in the code if necessary.


Python Path Issues:  
If VS Code cannot find the Python interpreter, reselect it using Python: Select Interpreter in the Command Palette.  
Ensure the virtual environment is activated before running the script.



Estructura del Proyecto / Project Structure
<repository-name>/
│
├── main.py                 # Script principal para procesamiento y visualización de datos / Main script for data processing and visualization
├── misc.py                 # Módulo personalizado para funciones de utilidad / Custom module for utility functions
├── preprocessing.py        # Módulo personalizado para carga de datos / Custom module for data loading
├── integrity.py            # Módulo personalizado para correcciones de datos / Custom module for data corrections
├── README.md               # Este archivo / This file
├── venv/                   # Carpeta del entorno virtual (creada localmente) / Virtual environment folder (created locally)
└── YANACOCHA/data/         # Directorios de datos experimentales / Experiment data directories

Notas / Notes
Español:  

Los módulos personalizados (misc, preprocessing, integrity) son archivos Python incluidos en el repositorio y son esenciales para que el código funcione.  
El código asume acceso a datos experimentales en la estructura de directorios YANACOCHA/data. Asegúrate de que los datos estén formateados correctamente y sean accesibles.  
Para conjuntos de datos grandes, monitorea el uso de memoria, ya que cargar múltiples archivos de experimentos puede ser intensivo en recursos.

English:  

The custom modules (misc, preprocessing, integrity) are Python files included in the repository and are critical for the code to function.  
The code assumes access to experiment data in the YANACOCHA/data directory structure. Ensure the data is properly formatted and accessible.  
For large datasets, monitor memory usage, as loading multiple experiment files may be resource-intensive.

Contribuir / Contributing
Español:Para contribuir a este proyecto:  

Haz un fork del repositorio.  
Crea una nueva rama (git checkout -b feature-branch).  
Realiza cambios y haz commit (git commit -m "Descripción de los cambios").  
Sube a la rama (git push origin feature-branch).  
Crea un pull request en la plataforma de alojamiento del repositorio.

English:To contribute to this project:  

Fork the repository.  
Create a new branch (git checkout -b feature-branch).  
Make changes and commit (git commit -m "Description of changes").  
Push to the branch (git push origin feature-branch).  
Create a pull request on the repository's hosting platform.

Licencia / License
Español: Este proyecto está licenciado bajo la Licencia MIT (o especifica la licencia adecuada si es diferente).English: This project is licensed under the MIT License (or specify the appropriate license if different).  
Contacto / Contact
Español: Para problemas o preguntas, contacta al mantenedor del repositorio o abre un issue en el rastreador de issues del repositorio.English: For issues or questions, please contact the repository maintainer or open an issue on the repository's issue tracker.
