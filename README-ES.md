# 🎙️ Text-to-Speech: ¡Convierte casi cualquier archivo de texto a audio de alta fidelidad!! 🎧

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI API](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/blog/openai-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Text-to-Speech es una poderosa herramienta que convierte casi cualquier archivo de texto (PDF, EPUB) a audio de alta fidelidad utilizando la API de OpenAI y técnicas avanzadas de procesamiento de audio para una experiencia auditiva excepcional.

## 🌟 Características

- 📄 **Extracción inteligente de texto** desde archivos PDF y EPUB
- 🔊 **Conversión a voz natural** usando la API de OpenAI (modelo gpt-4o-mini-tts)
- 🧩 **División automática** de textos largos en fragmentos manejables
- 🔄 **Fusión de archivos de audio** para una experiencia continua
- ✂️ **Eliminación de silencios** innecesarios en los archivos de audio
- 📊 **Normalización de volumen** para una calidad de audio consistente
- 🌐 **Soporte multilingüe** (Español e Inglés)
- 📝 **Registro detallado** de todas las operaciones

## 🛠️ Requisitos previos

- Python 3.8 o superior
- FFmpeg instalado y configurado
- Clave API de OpenAI
- Las siguientes bibliotecas de Python:
  - openai
  - PyMuPDF (fitz)
  - ebooklib
  - beautifulsoup4
  - pydub
  - tqdm
  - asyncio

## 📋 Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/sergio-usma/text-to-speech.git
   cd text-to-speech
   ```

2. **Crear y activar un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar FFmpeg**:
   - [Descargar FFmpeg](https://ffmpeg.org/download.html)
   - Agregar la ruta de FFmpeg al PATH o configurar la variable `FFMPEG_PATH` en el script

5. **Configurar la API de OpenAI**:
   - Obtener una clave API de [OpenAI](https://platform.openai.com/)
   - Configurar la variable `OPENAI_API_KEY` en el script

## 🚀 Uso

El script ofrece tres funcionalidades principales:

### 1️⃣ Procesar un archivo (PDF/EPUB → Audio)

Convierte un archivo PDF o EPUB completo a audio:

```bash
python text_to_speech.py
# Seleccionar opción 1
# Ingresar el idioma del texto (1: Español, 2: Inglés)
# Proporcionar la ruta completa al archivo
```

### 2️⃣ Fusionar fragmentos de audio existentes

Combina múltiples archivos MP3 en una carpeta y mejora la calidad del audio resultante:

```bash
python text_to_speech.py
# Seleccionar opción 2
# Proporcionar la ruta a la carpeta que contiene los archivos MP3
```

### 3️⃣ Mejorar un archivo de audio existente

Elimina silencios y normaliza el volumen de un archivo MP3:

```bash
python text_to_speech.py
# Seleccionar opción 3
# Proporcionar la ruta completa al archivo MP3
```

## 📊 Flujo de trabajo

1. **Extracción de texto**:
   - Elimina automáticamente encabezados y pies de página de los PDF
   - Extrae texto de archivos EPUB preservando la estructura del contenido

2. **División del texto**:
   - Divide el texto en fragmentos de aproximadamente 2000 caracteres
   - Mantiene palabras completas en cada fragmento

3. **Conversión a voz**:
   - Utiliza la API de OpenAI para convertir cada fragmento a audio
   - Aplica una voz natural (voz "ash" por defecto)

4. **Procesamiento del audio**:
   - Fusiona todos los fragmentos de audio
   - Elimina silencios para una experiencia más fluida
   - Normaliza el volumen para una calidad consistente

5. **Finalización**:
   - Guarda el archivo de audio final en la misma ubicación que el archivo original
   - Opcional: elimina los archivos temporales

## ⚙️ Configuración

Puedes personalizar varios parámetros en el script:

```python
# Configuración general
CHAR_LIMIT = 2000          # Límite de caracteres por fragmento
VOICE = "ash"              # Voz de OpenAI a utilizar
MODEL = "gpt-4o-mini-tts"  # Modelo de OpenAI para la conversión
FFMPEG_PATH = "C:\\ffmpeg\\bin"  # Ruta a la instalación de FFmpeg
```

## 🔮 Características futuras

- 👁️ **Reconocimiento OCR** para archivos PDF escaneados
- 📝 **Soporte para documentos DOCX**
- ☁️ **Implementación como SaaS** escalable para ejecutar el código como servicio
- 🎛️ **Interfaz gráfica de usuario** para facilitar el uso
- 🌐 **Soporte para más idiomas**

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un Fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios
4. Haz commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
5. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Abre un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ❓ Resolución de problemas

- **Error con FFmpeg**: Asegúrate de que FFmpeg esté correctamente instalado y que la ruta en `FFMPEG_PATH` sea correcta.
- **Error de API**: Verifica que tu clave API de OpenAI sea válida y esté correctamente configurada.
- **Archivos PDF no procesados correctamente**: Algunos PDFs con formatos complejos pueden requerir procesamiento adicional.

## 📞 Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en este repositorio.
