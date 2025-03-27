# 🎙️ Text-to-Speech: Convert Almost Any Text File to High-Fidelity Audio!! 🎧

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI API](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/blog/openai-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Text-to-Speech is a powerful tool that converts almost any text file (PDF, EPUB) to high-fidelity audio using the OpenAI API and advanced audio processing techniques for an exceptional listening experience.

## 🌟 Features

- 📄 **Intelligent text extraction** from PDF and EPUB files
- 🔊 **Natural voice conversion** using OpenAI API (gpt-4o-mini-tts model)
- 🧩 **Automatic splitting** of long texts into manageable chunks
- 🔄 **Audio file merging** for a seamless experience
- ✂️ **Silence removal** from audio files
- 📊 **Volume normalization** for consistent audio quality
- 🌐 **Multilingual support** (Spanish and English)
- 📝 **Detailed logging** of all operations

## 🛠️ Prerequisites

- Python 3.8 or higher
- FFmpeg installed and configured
- OpenAI API key
- The following Python libraries:
  - openai
  - PyMuPDF (fitz)
  - ebooklib
  - beautifulsoup4
  - pydub
  - tqdm
  - asyncio

## 📋 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/text-to-speech.git
   cd text-to-speech
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**:
   - [Download FFmpeg](https://ffmpeg.org/download.html)
   - Add FFmpeg path to your PATH or configure the `FFMPEG_PATH` variable in the script

5. **Configure OpenAI API**:
   - Get an API key from [OpenAI](https://platform.openai.com/)
   - Configure the `OPENAI_API_KEY` variable in the script

## 🚀 Usage

The script offers three main functionalities:

### 1️⃣ Process a file (PDF/EPUB → Audio)

Convert a complete PDF or EPUB file to audio:

```bash
python text_to_speech.py
# Select option 1
# Enter the text language (1: Spanish, 2: English)
# Provide the full path to the file
```

### 2️⃣ Merge existing audio chunks

Combine multiple MP3 files in a folder and enhance the quality of the resulting audio:

```bash
python book_to_audio.py
# Select option 2
# Provide the path to the folder containing MP3 files
```

### 3️⃣ Enhance an existing audio file

Remove silences and normalize the volume of an MP3 file:

```bash
python book_to_audio.py
# Select option 3
# Provide the full path to the MP3 file
```

## 📊 Workflow

1. **Text extraction**:
   - Automatically removes headers and footers from PDFs
   - Extracts text from EPUB files preserving content structure

2. **Text splitting**:
   - Divides text into chunks of approximately 2000 characters
   - Maintains complete words in each chunk

3. **Voice conversion**:
   - Uses OpenAI API to convert each chunk to audio
   - Applies a natural voice (default is "ash" voice)

4. **Audio processing**:
   - Merges all audio chunks
   - Removes silences for a smoother experience
   - Normalizes volume for consistent quality

5. **Finalization**:
   - Saves the final audio file in the same location as the original file
   - Optional: removes temporary files

## ⚙️ Configuration

You can customize various parameters in the script:

```python
# General configuration
CHAR_LIMIT = 2000          # Character limit per chunk
VOICE = "ash"              # OpenAI voice to use
MODEL = "gpt-4o-mini-tts"  # OpenAI model for conversion
FFMPEG_PATH = "C:\\ffmpeg\\bin"  # Path to FFmpeg installation
```

## 🔮 Future Features

- 👁️ **OCR recognition** for scanned PDF files
- 📝 **DOCX document support**
- ☁️ **SaaS implementation** to run the code as a scalable service
- 🎛️ **Graphical user interface** for easier use
- 🌐 **Support for more languages**

## 🤝 Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/new-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ❓ Troubleshooting

- **FFmpeg error**: Make sure FFmpeg is correctly installed and the path in `FFMPEG_PATH` is correct.
- **API error**: Verify that your OpenAI API key is valid and correctly configured.
- **PDF files not properly processed**: Some PDFs with complex formats may require additional processing.

## 📞 Contact

If you have questions or suggestions, feel free to open an issue in this repository.