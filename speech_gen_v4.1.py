import os
import asyncio
import shutil
import datetime
import subprocess
import tempfile
from pathlib import Path
from openai import AsyncOpenAI
from tqdm import tqdm
import fitz  # PyMuPDF
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# Ask user for OpenAI API Key
OPENAI_API_KEY = ""

# Configuration
CHAR_LIMIT = 2000
VOICE = "ash"
MODEL = "gpt-4o-mini-tts"
FFMPEG_PATH = "C:\\ffmpeg\\bin"
LOG_FILE = "conversion_log.txt"


def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_entry)


def merge_audio(files, output_path):
    temp_list_file = "temp_audio_list.txt"
    with open(temp_list_file, "w", encoding="utf-8") as f:
        for file in sorted(files, key=lambda x: os.path.getctime(str(x))):
            f.write(f"file '{file}'\n")
    subprocess.run([
        os.path.join(FFMPEG_PATH, "ffmpeg.exe"), "-f", "concat", "-safe", "0", "-i", temp_list_file,
        "-acodec", "libmp3lame", "-b:a", "128k", str(output_path)
    ], check=True)
    os.remove(temp_list_file)


def get_temp_folder(base_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(base_path) / f"TEMP_{timestamp}"


def remove_headers_footers(pdf_path, temp_folder):
    output_path = temp_folder / Path(pdf_path).name
    doc = fitz.open(pdf_path)
    for page in doc:
        rect = page.rect
        new_rect = fitz.Rect(rect.x0, rect.y0 + 56.7, rect.x1, rect.y1 - 56.7)
        page.set_cropbox(new_rect)
    doc.save(output_path)
    doc.close()
    log_message(f"Processed PDF saved as: {output_path}")
    return output_path


def extract_epub_text(epub_path):
    """
    Improved function to extract text from EPUB files
    """
    try:
        book = epub.read_epub(str(epub_path))
        all_text = []

        # Process each chapter/content item
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Get the content as string
                content = item.get_content()
                # Parse HTML content with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                # Extract text and remove extra whitespace
                if soup.body:
                    text = soup.body.get_text(" ", strip=True)
                    all_text.append(text)

        return " ".join(all_text)
    except Exception as e:
        log_message(f"Error extracting text from EPUB: {e}")
        return ""


def extract_text(file_path, language, temp_folder):
    text = ""
    if file_path.suffix.lower() == ".pdf":
        processed_pdf = remove_headers_footers(file_path, temp_folder)
        doc = fitz.open(str(processed_pdf))
        text = " ".join(page.get_text("text") for page in doc)
        doc.close()  # Close the PDF before deleting
        processed_pdf.unlink()  # Delete temporary processed file
    elif file_path.suffix.lower() == ".epub":
        text = extract_epub_text(file_path)
    return " ".join(text.split())  # Replace multiple spaces with single spaces


def split_text(text):
    words = text.split()
    chunks = []
    chunk = []
    char_count = 0
    for word in words:
        if char_count + len(word) + 1 > CHAR_LIMIT:
            chunks.append(" ".join(chunk))
            chunk = []
            char_count = 0
        chunk.append(word)
        char_count += len(word) + 1
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks


async def text_to_speech(client, text, output_path):
    if not text.strip():
        return
    async with client.audio.speech.with_streaming_response.create(
            model=MODEL,
            voice=VOICE,
            input=text,
            instructions="Speak in a cheerful and positive tone.",
            response_format="mp3",
    ) as response:
        with open(output_path, "wb") as f:
            async for chunk in response.iter_bytes():
                f.write(chunk)
    return output_path


def remove_silence_from_audio(input_file, silence_thresh=-50.0, min_silence_len=500):
    """
    Removes silent sections from an MP3 file and returns an AudioSegment object.

    Parameters:
    - input_file: Path to the input MP3 file.
    - silence_thresh: Threshold in dB below which audio is considered silent.
    - min_silence_len: Minimum length of silence (in milliseconds) to be removed.
    """
    log_message(f"Removing silence from audio: {input_file}")
    audio = AudioSegment.from_mp3(input_file)
    nonsilent_ranges = detect_nonsilent(audio, silence_thresh=silence_thresh, min_silence_len=min_silence_len)

    # Define a buffer time in milliseconds to smooth transitions
    BUFFER_TIME = 50  # 50ms buffer before and after each non-silent section
    processed_audio = AudioSegment.silent(duration=0)

    for start, end in nonsilent_ranges:
        start = max(0, start - BUFFER_TIME)
        end = min(len(audio), end + BUFFER_TIME)
        processed_audio += audio[start:end]

    return processed_audio


def normalize_audio(input_file, output_file):
    """
    Normalizes the MP3 audio file using FFmpeg, setting volume normalization and bitrate to 192k.
    """
    log_message(f"Normalizing audio: {input_file} -> {output_file}")
    ffmpeg_exe = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
    command = [
        ffmpeg_exe, "-y", "-i", str(input_file),
        "-af", "loudnorm", "-b:a", "192k", "-c:a", "mp3",
        str(output_file)
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def enhance_audio(input_file, output_file=None):
    """
    Enhances the final audio by removing silence and normalizing volume.
    Returns the path to the enhanced audio file.
    """
    log_message("Enhancing audio quality...")

    # Create paths for processing
    input_path = Path(input_file)
    base_dir = input_path.parent
    temp_file = base_dir / f"{input_path.stem}_TEMP.mp3"

    if output_file is None:
        output_file = base_dir / f"{input_path.stem}_Enhanced.mp3"

    # Step 1: Remove silence
    processed_audio = remove_silence_from_audio(input_path)
    processed_audio.export(temp_file, format="mp3", bitrate="192k")

    # Step 2: Normalize audio
    normalize_audio(temp_file, output_file)

    # Clean up
    temp_file.unlink()

    log_message(f"Enhanced audio saved at: {output_file}")
    return output_file


async def main():
    process_choice = input(
        "Do you want to (1) Process a file or (2) Merge audio chunks in a folder or (3) Simply enhance an existing audio file? Enter 1, 2 or 3: ").strip()

    if process_choice == "3":
        # Direct audio enhancement only
        file_path = Path(input("Enter the full path of the MP3 file to enhance: ").strip())
        if not file_path.exists() or file_path.suffix.lower() != ".mp3":
            log_message("Invalid MP3 file path. Exiting.")
            return

        log_message(f"Selected file for enhancement: {file_path}")
        log_message("Starting audio enhancement process (removing silence and normalizing audio)...")
        final_output = file_path.parent / f"{file_path.stem}_Enhanced.mp3"
        enhanced_audio = enhance_audio(file_path, final_output)
        log_message(f"Audio enhancement completed. Final output: {enhanced_audio}")
        return

    elif process_choice == "2":
        # Merge audio chunks and enhance
        folder_path = Path(input("Enter the folder containing audio chunks: ").strip())
        if not folder_path.exists() or not folder_path.is_dir():
            log_message("Invalid folder path. Exiting.")
            return

        audio_files = sorted(folder_path.glob("*.mp3"), key=os.path.getctime)
        if not audio_files:
            log_message("No MP3 files found in the folder. Exiting.")
            return

        # Step 1: Merge the audio chunks
        merged_mp3 = folder_path.parent / f"{folder_path.name}_merged.mp3"
        log_message("Step 1: Merging audio files...")
        merge_audio(audio_files, merged_mp3)
        log_message(f"Merge completed. Merged output saved as: {merged_mp3}")

        # Step 2: Enhance the merged audio
        log_message("Step 2: Enhancing audio (removing silence and normalizing audio)...")
        final_output = folder_path.parent / f"{folder_path.name}.mp3"
        enhanced_audio = enhance_audio(merged_mp3, final_output)

        # Clean up the intermediate merged file
        merged_mp3.unlink()
        log_message(f"Audio enhancement completed. Final output: {enhanced_audio}")
        return

    print("Select the language of the text:")
    print("1: Spanish")
    print("2: English")
    language_choice = input("Enter 1 or 2: ").strip()
    LANGUAGE = "es-CO" if language_choice == "1" else "en-US"

    file_path = Path(input("Enter the full path of the file: ").strip())
    if not file_path.exists():
        log_message("Invalid file path. Exiting.")
        return

    log_message(f"Selected file: {file_path}")
    temp_path = get_temp_folder(file_path.parent)
    temp_path.mkdir(exist_ok=True)

    text = extract_text(file_path, LANGUAGE, temp_path)
    if not text.strip():
        log_message("No text found in the document. Exiting.")
        return

    chunks = split_text(text)
    log_message(f"Text split into {len(chunks)} chunks.")

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    audio_files = []

    for i, chunk in enumerate(tqdm(chunks, desc="Converting chunks", unit="chunk")):
        final_output_file = temp_path / f"chunk_{i + 1}.mp3"
        await text_to_speech(client, chunk, final_output_file)
        audio_files.append(final_output_file)

    # First merge - raw merge
    temp_merged_mp3 = temp_path / f"{file_path.stem}_merged.mp3"
    log_message("Merging audio files...")
    merge_audio(audio_files, temp_merged_mp3)
    log_message(f"Initial merge completed. Merged output saved in temp folder.")

    # Second step - enhance audio and save to final location
    final_output_mp3 = file_path.parent / f"{file_path.stem}.mp3"
    enhanced_audio = enhance_audio(temp_merged_mp3, final_output_mp3)
    log_message(f"Audio processing completed. Final output saved as: {final_output_mp3}")

    delete_temp = input("Delete TEMP folder? (y/n): ").strip().lower()
    if delete_temp == "y":
        shutil.rmtree(temp_path)
        log_message("TEMP folder deleted.")
    else:
        log_message(f"TEMP folder retained: {temp_path}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())