### How to Parse and Extract Text from Audio Files?

Parse an audio file to extract metadata and transcription. This is particularly useful for extracting spoken content from audio recordings.

```python
import os
from mutagen import File
import speech_recognition as sr
from pydub import AudioSegment

# The path to the audio file to be parsed, for example: "workspace/task.mp3"
audio_path = "workspace/task.mp3"

if not os.path.exists(audio_path):
    print(f"Error: Audio file '{audio_path}' does not exist.")

supported_formats = ['.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg', '.wma']
file_ext = os.path.splitext(audio_path)[1].lower()

if file_ext not in supported_formats:
    print(f"Error: Unsupported audio format '{file_ext}'. Supported formats: {', '.join(supported_formats)}")

result = []
result.append(f"Audio file: {os.path.basename(audio_path)}")
result.append("=" * 50)

# Extract metadata using mutagen
audiofile = File(audio_path)
if audiofile is not None:
    result.append("Metadata:")
    result.append(f"  Format: {audiofile.mime[0] if audiofile.mime else 'Unknown'}")
    result.append(f"  Duration: {audiofile.info.length:.2f} seconds" if hasattr(audiofile.info, 'length') else "  Duration: Unknown")
    result.append(f"  Bitrate: {audiofile.info.bitrate} bps" if hasattr(audiofile.info, 'bitrate') else "  Bitrate: Unknown")
    
    # Extract common tags like title, artist, album, date, genre
    tags = ['title', 'artist', 'album', 'date', 'genre']
    for tag in tags:
        if tag in audiofile and audiofile[tag]:
            result.append(f"  {tag.capitalize()}: {audiofile[tag][0]}")
    
    result.append("-" * 30)

# Extract transcription using speech recognition
audio = AudioSegment.from_file(audio_path)
temp_wav = "temp_audio.wav"
audio.export(temp_wav, format="wav")

recognizer = sr.Recognizer()

with sr.AudioFile(temp_wav) as source:
    audio_data = recognizer.record(source)
    
    # Transcribe audio to text using Google Speech Recognition
    text = recognizer.recognize_google(audio_data, language='en-US')
    result.append("\nTranscription (English):")
    result.append(text)

# Clean up temporary file
if os.path.exists(temp_wav):
    os.remove(temp_wav)

# Print the complete results
print("\n".join(result))
```

### How to Parse Word Documents and Extract Text Content?

Parse a Word document (.docx) and return the text content. Uses the LangChain community library for document processing.

```python
import os
from langchain_community.document_loaders import Docx2txtLoader

# The path to the Word document to be parsed, for example: "workspace/task.docx"
docx_path = "workspace/task.docx"

if not os.path.exists(docx_path):
    print(f"Error: Word document '{docx_path}' does not exist.")

if not docx_path.lower().endswith('.docx'):
    print(f"Error: File must be a .docx file. Got: {docx_path}")

# Load and parse the Word document using LangChain
loader = Docx2txtLoader(docx_path)
documents = loader.load()

if not documents:
    print("No content found in the Word document.")

# Extract and combine text content from all document sections
full_text = "\n\n".join([doc.page_content for doc in documents])

if full_text.strip():
    print(full_text)
else:
    print("The Word document appears to be empty.")
```

### How to Extract Text from Images Using OCR?

Parse and extract text from an image file using Hugging Face Tesseract-OCR Space. This is particularly useful when you need to count words, analyze word frequency, or extract numbers from images, as it provides more accurate and detailed text extraction compared to GPT-4o based VLM tools.

```python
import os
from gradio_client import Client, handle_file

# The path to the image file to be parsed, for example: "workspace/task.png"
image_path = "workspace/task.png"

if not os.path.exists(image_path):
    print(f"Error: Image file '{image_path}' does not exist.")

supported_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp']
file_ext = os.path.splitext(image_path)[1].lower()

if file_ext not in supported_formats:
    print(f"Error: Unsupported image format '{file_ext}'. Supported formats: {', '.join(supported_formats)}")

# Initialize Hugging Face Tesseract-OCR client
client = Client("kneelesh48/Tesseract-OCR")

# Process the image and extract text using OCR
result = client.predict(
    handle_file(image_path)
)

if result and result.strip():
    print(f"Extracted text from image using Hugging Face OCR Space:")
    print(result.strip())
else:
    print("No text found in the image.")
```

### How to Analyze Images Using GPT-4o Multimodal Model?

Parse and analyze an image file using GPT-4o multimodal model. This code can understand complex visual content, generate captions, extract tables as HTML, create SVG code for geometric shapes, and answer specific questions about images.

```python
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# The local path to the image file to be parsed, for example: "workspace/task.png"
image_path = "workspace/task.png"
# Optional question to ask about the image. If None, provides general analysis
question = "What is the main content of the image?"

if not os.path.exists(image_path):
    print(f"Error: Image file '{image_path}' does not exist.")

supported_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp']
file_ext = os.path.splitext(image_path)[1].lower()

if file_ext not in supported_formats:
    print(f"Error: Unsupported image format '{file_ext}'. Supported formats: {', '.join(supported_formats)}")

# Encode image to base64 format
img_type = "data:image/jpeg;base64," if file_ext in ['.jpg', '.jpeg'] else "data:image/png;base64,"
with open(image_path, "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode("utf-8")

# Define content analysis rules for different image types
base_rules = (
    "# Content Analysis Rules\n"
    "**Tables**: Extract content and styling as well-structured HTML.\n"
    "**Geometric Shapes**: Generate vector graphic code (SVG).\n"
    "**Complex Graphics**: Provide extremely detailed description.\n"
    "**General Images**: Generate comprehensive caption.\n"
    "**Math**: Represent formulas in latex code.\n"
    "**Text**: Extract and transcribe all visible text accurately.\n"
)

# Create prompt based on whether a specific question is provided
if question:
    prompt = (
        f"Analyze the image carefully and answer the following question: {question}\n"
        f"{base_rules}"
        "# Output Format\n"
        "## Image Caption\n"
        "[Provide detailed caption of the image]\n"
        "## Answer\n"
        "[Provide answer to the question based on image content]"
    )
else:
    prompt = (
        "Analyze the image and provide appropriate output based on its content type:\n"
        f"{base_rules}"
        "# Output Format\n"
        "## Image Caption\n"
        "[Provide detailed caption of the image]\n"
        "## Image Content [Optional]\n"
        "[Provide drawing codes, extracted text, or other relevant content]"
    )

# Prepare API request payload
payload = {
    "model": "gpt-4o-0806",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"{img_type}{img_base64}"
                    }
                }
            ],
        },
    ],
    "max_tokens": 8192,
}

# Get API credentials from environment variables
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_BASE_URL")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Send request to OpenAI API
response = requests.post(f"{api_base}/chat/completions", headers=headers, json=payload)

if response.status_code != 200:
    print(f"Error: API request failed with status {response.status_code}: {response.text}")

result = response.json()
if "choices" not in result or len(result["choices"]) == 0:
    print(f"Error: Invalid API response: {result}")

# Extract and print the analysis result
output = result["choices"][0]["message"]["content"]
print(output)
```

### How to Parse PDB (Protein Data Bank) Files and Extract Structural Information?

Parse a PDB file to extract protein structural information including models, chains, residues, and atoms. It provides detailed analysis of protein structure data.

```python
import os
import warnings
from Bio.PDB import PDBParser

warnings.filterwarnings("ignore")

# The path to the PDB file to be parsed, for example: "workspace/task.pdb"
pdb_path = "workspace/task.pdb"
# The starting index for atom lines to preview (default: 0)
start_atom_idx = 0
# The ending index for atom lines to preview (default: 5)
end_atom_idx = 5

if not os.path.exists(pdb_path):
    print(f"Error: PDB file '{pdb_path}' does not exist.")

if not pdb_path.lower().endswith('.pdb'):
    print(f"Error: File must be a .pdb file. Got: {pdb_path}")

result = []
result.append(f"PDB file: {os.path.basename(pdb_path)}")
result.append("=" * 50)

# Parse PDB structure using BioPython
parser = PDBParser()
structure = parser.get_structure('protein', pdb_path)

result.append("Structure Information:")
result.append(f"  Structure ID: {structure.id}")
result.append(f"  Number of models: {len(structure)}")

# Analyze each model in the structure
for model in structure:
    result.append(f"\nModel {model.id}:")
    result.append(f"  Number of chains: {len(model)}")
    
    # Analyze each chain in the model
    for chain in model:
        residues = list(chain)
        result.append(f"    Chain {chain.id}: {len(residues)} residues")
        
        if residues:
            first_res = residues[0]
            last_res = residues[-1]
            result.append(f"      First residue: {first_res.get_resname()} {first_res.get_id()[1]}")
            result.append(f"      Last residue: {last_res.get_resname()} {last_res.get_id()[1]}")
            
            # Count total atoms in this chain
            atom_count = sum(len(list(residue.get_atoms())) for residue in residues)
            result.append(f"      Total atoms: {atom_count}")

result.append("-" * 30)

# Parse basic PDB file information by reading raw text
with open(pdb_path, 'r') as f:
    lines = f.readlines()

result.append("\nBasic PDB Information:")

# Extract header information
header_lines = [line for line in lines if line.startswith('HEADER')]
if header_lines:
    result.append(f"  Header: {header_lines[0].strip()}")

# Extract title information
title_lines = [line for line in lines if line.startswith('TITLE')]
if title_lines:
    title = ' '.join([line[10:].strip() for line in title_lines])
    result.append(f"  Title: {title}")

# Count different record types in the PDB file
record_types = {}
for line in lines:
    if len(line) >= 6:
        record_type = line[:6].strip()
        record_types[record_type] = record_types.get(record_type, 0) + 1

result.append("\nRecord Types:")
for record_type, count in sorted(record_types.items()):
    result.append(f"  {record_type}: {count}")

# Extract and display sample atom lines
atom_lines = [line for line in lines if line.startswith('ATOM')]
if atom_lines:
    # Ensure indices are within bounds
    start_idx = max(0, min(start_atom_idx, len(atom_lines)))
    end_idx = max(start_idx, min(end_atom_idx, len(atom_lines)))
    
    if start_idx < end_idx:
        result.append(f"\nAtom lines ({start_idx} to {end_idx-1}):")
        for line in atom_lines[start_idx:end_idx]:
            result.append(f"  {line.strip()}")
        
        if end_idx < len(atom_lines):
            result.append(f"  ... and {len(atom_lines) - end_idx} more atoms after index {end_idx-1}")
        if start_idx > 0:
            result.append(f"  ... and {start_idx} atoms before index {start_idx}")
    else:
        result.append(f"\nNo atoms to display in range [{start_idx}, {end_idx})")
        result.append(f"  Total atoms available: {len(atom_lines)}")

# Print the complete analysis
print("\n".join(result))
```

### How to Parse PDF Files and Extract Text Content?

Parse a PDF file and return the text content with optional page range selection. Uses the LangChain community library for document processing.

```python
from langchain_community.document_loaders import PyPDFLoader

# The path to the PDF file to be parsed, for example: "workspace/task.pdf"
pdf_path = "workspace/task.pdf"
# The starting page number to read from (1-indexed). If None, read from the beginning
start_page = None
# The ending page number to read to (1-indexed, inclusive). If None, read to the end
end_page = None

# Load and split PDF into pages using LangChain
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

if len(pages) == 0:
    print("No pages found in this PDF file.")

# Handle page range parameters
if start_page is not None:
    start_idx = max(0, start_page - 1)  # Convert to 0-indexed
else:
    start_idx = 0

if end_page is not None:
    end_idx = min(len(pages), end_page)  # Convert to 0-indexed (end_page is inclusive)
else:
    end_idx = len(pages)

# Validate page range
if start_idx >= len(pages):
    print(f"Error: start_page {start_page} is beyond the PDF length ({len(pages)} pages).")

if start_page is not None and end_page is not None and start_page > end_page:
    print(f"Error: start_page ({start_page}) cannot be greater than end_page ({end_page}).")

# Extract the specified page range
selected_pages = pages[start_idx:end_idx]
content = "\n".join([page.page_content for page in selected_pages])

# Check if content is too large (only for full PDF reading)
if len(content) > 100000:
    print(f"Error: PDF '{pdf_path}' content is too large ({len(content)} characters). Total pages: {len(pages)}. Please use start_page and end_page parameters to read specific page ranges.")

# Add page range information to the result if reading a subset
if start_page is not None or end_page is not None:
    actual_start = start_idx + 1
    actual_end = start_idx + len(selected_pages)
    range_info = f"[Pages {actual_start}-{actual_end} of {len(pages)} total pages]\n"
    print(range_info + content)
else:
    print(content)
```

### How to Parse PowerPoint Presentations and Extract Structured Content?

Parse a PowerPoint presentation and return structured content in HTML format, including text, tables, and image descriptions. This tool can analyze images within presentations and extract table data.

```python
import os
import html
import tempfile
import base64
import pptx

# The path to the PowerPoint file to be parsed, for example: "workspace/task.pptx"
pptx_path = "workspace/task.pptx"

def _is_picture(shape):
    """Check if a shape is a picture."""
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
        return True
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PLACEHOLDER:
        if hasattr(shape, "image"):
            return True
    return False

def _is_table(shape):
    """Check if a shape is a table."""
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.TABLE:
        return True
    return False

def _extract_image_content(shape, slide_num, shape_num):
    """Extract image content and analyze it."""
    # Try to get alt text first
    alt_text = ""
    alt_text = shape._element._nvXxPr.cNvPr.attrib.get("descr", "")

    if alt_text:
        return f"<p><strong>Image {slide_num}-{shape_num}:</strong> {alt_text}</p>"
    
    # If no alt text, try to extract and analyze the image
    # Extract image data
    image = shape.image
    image_bytes = image.blob
    
    # Save to temporary file for analysis
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(image_bytes)
        temp_image_path = temp_file.name

    # Use parse_image to analyze the image (requires parse_image function to be available)
    # For this example, we'll just return a placeholder
    image_analysis = "[Image content analysis would be performed here]"
    
    # Clean up temporary file
    os.unlink(temp_image_path)
    
    return f"<div><strong>Image {slide_num}-{shape_num} Analysis:</strong><br/>{image_analysis}</div>"

def _extract_table_content(shape):
    """Extract table content and return as HTML."""
    html_table = "<table border='1' style='border-collapse:collapse;'>"
    first_row = True
    
    for row in shape.table.rows:
        html_table += "<tr>"
        for cell in row.cells:
            tag = "th" if first_row else "td"
            cell_text = html.escape(cell.text.strip()) if cell.text else ""
            html_table += f"<{tag}>{cell_text}</{tag}>"
        html_table += "</tr>"
        first_row = False
    
    html_table += "</table>"
    return html_table

if not os.path.exists(pptx_path):
    print(f"Error: PowerPoint file '{pptx_path}' does not exist.")

supported_formats = ['.pptx', '.ppt']
file_ext = os.path.splitext(pptx_path)[1].lower()

if file_ext not in supported_formats:
    print(f"Error: Unsupported file format '{file_ext}'. Supported formats: {', '.join(supported_formats)}")

# Parse PowerPoint presentation using python-pptx
presentation = pptx.Presentation(pptx_path)
html_content = f"<h1>PowerPoint: {os.path.basename(pptx_path)}</h1>\n"
html_content += f"<p>Number of slides: {len(presentation.slides)}</p>\n"
html_content += "<hr/>\n"

slide_num = 0
for slide in presentation.slides:
    slide_num += 1
    html_content += f"<h2>Slide {slide_num}</h2>\n"
    
    title = slide.shapes.title
    shape_num = 0
    
    for shape in slide.shapes:
        shape_num += 1
        
        # Process image shapes
        if _is_picture(shape):
            image_content = _extract_image_content(shape, slide_num, shape_num)
            html_content += image_content + "\n"
        
        # Process table shapes
        elif _is_table(shape):
            html_content += "<h4>Table:</h4>\n"
            table_content = _extract_table_content(shape)
            html_content += table_content + "\n"
        
        # Process text shapes
        elif shape.has_text_frame and shape.text.strip():
            if shape == title:
                html_content += f"<h3>{html.escape(shape.text.strip())}</h3>\n"
            else:
                # Process multi-level text content
                text_content = shape.text.strip()
                if text_content:
                    # Split text by line and preserve formatting
                    lines = text_content.split('\n')
                    html_content += "<div>\n"
                    for line in lines:
                        if line.strip():
                            html_content += f"<p>{html.escape(line.strip())}</p>\n"
                    html_content += "</div>\n"
    
    # Process slide notes if available
    if slide.has_notes_slide:
        notes_frame = slide.notes_slide.notes_text_frame
        if notes_frame is not None and notes_frame.text.strip():
            html_content += "<h4>Notes:</h4>\n"
            notes_text = notes_frame.text.strip()
            html_content += f"<div style='background-color:#f5f5f5;padding:10px;'>{html.escape(notes_text)}</div>\n"
    
    html_content += "<hr/>\n"

print(html_content.strip())
```

### How to Parse Excel Files and Extract Content with Styling?

Parse an Excel file and return the content as formatted HTML with style information preserved. Supports Excel (.xlsx, .xls) and CSV files.

```python
import os
import pandas as pd
from openpyxl import load_workbook

# The path to the Excel file to be parsed, for example: "workspace/task.xlsx" or "workspace/task.csv"
xlsx_path = "workspace/task.xlsx"

def get_cell_style(cell):
    """Extract style information from a cell and return as CSS style string."""
    styles = []

    # Check for bold formatting
    if cell.font and cell.font.bold:
        styles.append('font-weight:bold;')

    # Check for italic formatting
    if cell.font and cell.font.italic:
        styles.append('font-style:italic;')

    # Extract font color
    color = getattr(cell.font, 'color', None)
    if color is not None and getattr(color, 'type', None) == 'rgb':
        rgb = getattr(color, 'rgb', None)
        if isinstance(rgb, str) and len(rgb) >= 6:
            styles.append(f'color:#{rgb[-6:]};')
   
    # Extract background color
    fill = getattr(cell, 'fill', None)
    fgColor = getattr(fill, 'fgColor', None)
    if fgColor is not None and getattr(fgColor, 'type', None) == 'rgb':
        rgb = getattr(fgColor, 'rgb', None)
        if isinstance(rgb, str) and rgb != '00000000' and len(rgb) >= 6:
            styles.append(f'background-color:#{rgb[-6:]};')
    return ''.join(styles)

if not os.path.exists(xlsx_path):
    print(f"Error: Excel file '{xlsx_path}' does not exist.")

supported_formats = ['.xlsx', '.xls', '.csv']
file_ext = os.path.splitext(xlsx_path)[1].lower()

if file_ext not in supported_formats:
    print(f"Error: Unsupported file format '{file_ext}'. Supported formats: {', '.join(supported_formats)}")

# Handle CSV files separately using pandas
if file_ext == '.csv':
    df = pd.read_csv(xlsx_path)
    result = f"<h2>CSV : {os.path.basename(xlsx_path)}</h2>\n"
    result += f"<p>Rows: {df.shape[0]}, Columns: {df.shape[1]}</p>\n"
    result += "<table border='1'>\n"
    
    # Add header row
    result += "<tr>"
    for col in df.columns:
        result += f"<th>{col}</th>"
    result += "</tr>\n"
    
    # Add data rows (limit to first 100 rows for performance)
    for i, row in df.head(100).iterrows():
        result += "<tr>"
        for value in row:
            result += f"<td>{value if pd.notna(value) else ''}</td>"
        result += "</tr>\n"
    
    if len(df) > 100:
        result += f"<tr><td colspan='{len(df.columns)}'>... ({len(df) - 100} more rows)</td></tr>\n"
    
    result += "</table>\n"
    print(result)

# Handle Excel files using openpyxl
else:
    wb = load_workbook(xlsx_path, data_only=True)
    final_content = f"<h1>Excel: {os.path.basename(xlsx_path)}</h1>\n"
    final_content += f"<p>Number of sheets: {len(wb.worksheets)}</p>\n"
    
    # Process each worksheet in the Excel file
    for sheet in wb.worksheets:
        final_content += f"<h2>Sheet: {sheet.title}</h2>\n"
        
        max_row = sheet.max_row
        max_col = sheet.max_column
        
        final_content += f"<p>Rows: {max_row}, Columns: {max_col}</p>\n"
        final_content += "<table border='1' style='border-collapse:collapse;'>\n"
        
        # Process each row (limit to first 100 rows for performance)
        for i, row in enumerate(sheet.iter_rows(max_row=min(max_row, 100)), 1):
            final_content += "<tr>"
            for cell in row:
                tag = "th" if i == 1 else "td"  # First row as header
                style = get_cell_style(cell)
                value = cell.value if cell.value is not None else ""

                # Apply cell styling if present and not default black color
                if style and style != 'color:#000000;':
                    final_content += f"<{tag} style='{style}'>{value}</{tag}>"
                else:
                    final_content += f"<{tag}>{value}</{tag}>"
            final_content += "</tr>\n"
        
        # Add note if there are more rows than displayed
        if max_row > 100:
            final_content += f"<tr><td colspan='{max_col}'>... ({max_row - 100} more rows)</td></tr>\n"
        
        final_content += "</table>\n\n"

    print(final_content.strip())
```

### How to Read Text Files with Optional Line Range Selection?

Simply read the content of a text file with support for multiple encodings and optional line range selection. Supports common text formats like .txt, .md, .json, .py, and .js.

```python
import os

# The path to the file to read. For example, "workspace/task.txt"
file_path = "workspace/task.txt"
# The starting line number to read from (1-indexed). If None, read from the beginning
start_line = None
# The ending line number to read to (1-indexed, inclusive). If None, read to the end
end_line = None

if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' does not exist.")

# Try different encodings to handle various file types
encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1', 'ascii']

for encoding in encodings:
    lines = None
    with open(file_path, 'r', encoding=encoding) as file:
        lines = file.readlines()
        
        # Handle line range parameters
        if start_line is not None:
            start_idx = max(0, start_line - 1)  # Convert to 0-indexed
        else:
            start_idx = 0
        
        if end_line is not None:
            end_idx = min(len(lines), end_line)  # Convert to 0-indexed (end_line is inclusive)
        else:
            end_idx = len(lines)
        
        # Validate range
        if start_idx >= len(lines):
            print(f"Error: start_line {start_line} is beyond the file length ({len(lines)} lines).")
            break
        
        if start_line is not None and end_line is not None and start_line > end_line:
            print(f"Error: start_line ({start_line}) cannot be greater than end_line ({end_line}).")
            break
        
        # Extract the specified range
        selected_lines = lines[start_idx:end_idx]
        content = ''.join(selected_lines)
        
        # Check if content is too large (only for full file reading)
        if len(content) > 100000:
            print(f"Error: File '{file_path}' is too large ({len(content)} characters). Total lines: {len(lines)}. Please use start_line and end_line parameters to read specific ranges.")
            break
        
        # Add range information to the result if reading a subset
        if start_line is not None or end_line is not None:
            actual_start = start_idx + 1
            actual_end = start_idx + len(selected_lines)
            range_info = f"[Lines {actual_start}-{actual_end} of {len(lines)} total lines]\n"
            print(range_info + content)
        else:
            print(content)
        break

if lines is None:
    print(f"Error: Could not decode file '{file_path}' with any of the supported encodings.")
```
