import sys
import argparse
from PIL import Image
import mutagen
from PyPDF2 import PdfReader, PdfWriter
import docx
import openpyxl
import ffmpeg
import pikepdf
import zipfile
from xml.etree import ElementTree as ET
import os
def remove_image_metadata(image_path, output_path):
    """Remove metadata from an image file."""
    try:
        img = Image.open(image_path)
        img_data = list(img.getdata())
        img_no_meta = Image.new(img.mode, img.size)
        img_no_meta.putdata(img_data)
        img_no_meta.save(output_path)
        print(f"Metadata removed from image and saved to '{output_path}'")
    except Exception as e:
        print(f"Error processing image: {e}")
def remove_pdf_metadata(pdf_path, output_path):
    """Remove all metadata from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

   
        for page in reader.pages:
            writer.add_page(page)

        cleaned_metadata = {key: "" for key in reader.metadata}


        writer.add_metadata(cleaned_metadata)

        with open(output_path, "wb") as out:
            writer.write(out)

        print(f"Metadata removed from PDF and saved to '{output_path}'")
    except Exception as e:
        print(f"Error processing PDF: {e}")



def remove_audio_metadata(audio_path, attributes=None):
    """Remove metadata from an audio file, optionally clearing specific attributes."""
    try:
        audio_file = mutagen.File(audio_path, easy=True)
        if audio_file:
            if attributes:
                for attr in attributes:
                    if attr in audio_file:
                        audio_file[attr] = ''
            else:
                audio_file.delete()
            audio_file.save()
            print(f"Selected metadata removed from audio file '{audio_path}'")
        else:
            print(f"No metadata found in audio file '{audio_path}'")
    except Exception as e:
        print(f"Error processing audio file: {e}")

def remove_docx_metadata(docx_path, output_path):
    try:
        with zipfile.ZipFile(docx_path, 'r') as zf:
            # Delete docProps folder and its contents
            for filename in zf.namelist():
                if filename.startswith('docProps/'):
                    zf.extract(filename)
                    os.remove(filename)

            # Remove metadata from core.xml
            core_xml_filename = 'docProps/core.xml'
            if core_xml_filename in zf.namelist():
                with zf.open(core_xml_filename) as core_xml_file:
                    core_xml_tree = ET.parse(core_xml_file)
                    core_xml_root = core_xml_tree.getroot()

                    for element in core_xml_root.findall('.//{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}*'):
                        element.text = ''

                    with open(core_xml_filename, 'wb') as out_file:
                        core_xml_tree.write(out_file, xml_declaration=True, encoding='utf-8', method='xml')

            # Save the modified DOCX file
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as out_zf:
                for filename in zf.namelist():
                    if not filename.startswith('docProps/'):
                        with zf.open(filename) as in_file:
                            out_zf.writestr(filename, in_file.read())

            print(f"Metadata removed from DOCX and saved to '{output_path}'")

    except Exception as e:
        print(f"Error processing DOCX: {e}")
def remove_xlsx_metadata(xlsx_path, output_path):
    try:
        with zipfile.ZipFile(xlsx_path, 'r') as zf:
            # Delete docProps folder and its contents
            for filename in zf.namelist():
                if filename.startswith('docProps/'):
                    zf.extract(filename)
                    os.remove(filename)

            # Remove metadata from core.xml
            core_xml_filename = 'docProps/core.xml'
            if core_xml_filename in zf.namelist():
                with zf.open(core_xml_filename) as core_xml_file:
                    core_xml_tree = ET.parse(core_xml_file)
                    core_xml_root = core_xml_tree.getroot()

                    for element in core_xml_root.findall('.//{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}*'):
                        element.text = ''

                    with open(core_xml_filename, 'wb') as out_file:
                        core_xml_tree.write(out_file, xml_declaration=True, encoding='utf-8', method='xml')

            # Save the modified XLSX file
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as out_zf:
                for filename in zf.namelist():
                    if not filename.startswith('docProps/'):
                        with zf.open(filename) as in_file:
                            out_zf.writestr(filename, in_file.read())

            print(f"Metadata removed from XLSX and saved to '{output_path}'")

    except Exception as e:
        print(f"Error processing XLSX: {e}")
def remove_video_metadata(video_path, output_path):
    """Remove or reset video metadata using ffmpeg-python."""
    try:
        # Metadata fields to clear
        metadata_dict = {
            'comment': '',
            'creation_time': '1970-01-01T00:00:00.000000Z',
            'title': '',
            'artist': '',
            'encoded_by': '',
            'major_brand': '',
            'minor_version': '',
            'compatible_brands': '',
            'writing_application': '',
            'encoder': '',
            'software': '',
            'copyright': '',
            'track': '',
            'description': ''
        }

    
        metadata = ','.join([f'{k}={v}' for k, v in metadata_dict.items()])

        
        (
            ffmpeg
            .input(video_path)
            .output(
                output_path,
                map_metadata=-1, 
                metadata=metadata,
                vcodec='libx264',  
                acodec='aac',  
                audio_bitrate='128k',
                vf='format=yuv420p', 
                max_muxing_queue_size=9999
            )
            .run(overwrite_output=True)
        )

        print(f"Metadata removed from video and saved to '{output_path}'")
    except Exception as e:
        print(f"Error processing video file: {e}")

def main():
    """Main entry point for the CLI."""
    description = """
    This software removes metadata from various file types, including images, PDFs,
    Office files, audio files, and video files.

    Supported File Types:
    - Images: JPEG, PNG, TIFF, BMP
    - PDFs
    - Microsoft Office files: DOCX (Word), XLSX (Excel)
    - Audio: MP3, FLAC, OGG, WAV
    - Videos: MP4, MKV, MOV, AVI, FLV

    Examples:
    - Remove all metadata from a DOCX file:
      python metadata_cleaner.py input.docx --output output.docx

    - Remove specific metadata from an audio file:
      python metadata_cleaner.py input.mp3 --attributes artist album

    Attributes:
    - For DOCX: author, title, subject, comments
    - For XLSX: creator, title, subject, keywords, comments
    - For audio (MP3): artist, album, genre, etc.
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="Path to the input file")
    parser.add_argument("--output", help="Output path for the file (required for some file types)", default=None)
    parser.add_argument("--attributes", nargs="*", help="Specific attributes to remove (for supported file types only)")

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    attributes = args.attributes

    # Determine file type based on extension
    if input_path.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.bmp')):
        if not output_path:
            print("Error: Please provide an output file path using --output for image files.")
            sys.exit(1)
        remove_image_metadata(input_path, output_path)
    elif input_path.lower().endswith('.pdf'):
        if not output_path:
            print("Error: Please provide an output file path using --output for PDF files.")
            sys.exit(1)
        remove_pdf_metadata(input_path, output_path)
    elif input_path.lower().endswith(('.mp3', '.flac', '.ogg', '.wav')):
        remove_audio_metadata(input_path, attributes)
    elif input_path.lower().endswith('.docx'):
        if not output_path:
            print("Error: Please provide an output file path using --output for DOCX files.")
            sys.exit(1)
        remove_docx_metadata(input_path, output_path)
    elif input_path.lower().endswith('.xlsx'):
        if not output_path:
            print("Error: Please provide an output file path using --output for XLSX files.")
            sys.exit(1)
        remove_xlsx_metadata(input_path, output_path)
    elif input_path.lower().endswith(('.mp4', '.mkv', '.mov', '.avi', '.flv')):
        if not output_path:
            print("Error: Please provide an output file path using --output for video files.")
            sys.exit(1)
        remove_video_metadata(input_path, output_path)
    else:
        print(f"Unsupported file type for '{input_path}'.")

if __name__ == "__main__":
    main()
