# Developer Plan 01

## Plan
Search for and access the YouTube video titled 'The Thinking Machine (Artificial Intelligence in the 1960s)' to identify the scientists interviewed and analyze their predictions about when thinking machines or robots would be developed. Extract information about each scientist's timeline predictions and determine which scientist predicted the earliest or 'sooner' development of thinking machines compared to others interviewed in the same year.

## Description
This is the optimal first step because: (1) We need to locate and analyze the specific YouTube video to identify the scientists and their predictions, (2) No previous research has been conducted based on the empty HISTORY, (3) Expected outcome is to access the video content and extract scientist interviews with their timeline predictions for AI development, (4) This directly addresses the core TASK of finding which scientist made the most optimistic (sooner) prediction about thinking machines or robots

## Episodic Examples
### Development Step 2: Locate “Isn’t That Hot?” Dialogue in YouTube Video and Document Teal’c’s Exact Response

**Description**: Access and analyze the YouTube video at https://www.youtube.com/watch?v=1htKBjuUWec to locate the specific dialogue where someone asks 'Isn't that hot?' and identify Teal'c's exact response. Extract the audio/video content, transcribe the relevant dialogue section, and document Teal'c's reply to this question.

**Use Cases**:
- Corporate eLearning team retrieving and timestamping critical Q&A segments from training videos for onboarding documentation
- Legal eDiscovery specialists scanning and transcribing targeted dialogue from publicly posted deposition videos for case evidence preparation
- Marketing analysts monitoring influencer product reviews on YouTube, extracting and cataloging instances of brand mentions for sentiment tracking
- Academic linguistics researchers locating and transcribing specific phonetic phenomena in lecture videos to support corpus-based language studies
- Compliance officers identifying segments in financial webinars where regulatory requirements are discussed, to ensure accurate policy implementation
- Podcast producers automating extraction of sponsor-read ad segments from long-form video content to streamline editing and QC processes
- Accessibility coordinators generating precise transcripts of key interactions in educational videos to improve captioning accuracy for hearing-impaired students

```
import os
import json

# First, let's inspect the workspace directory structure and files
print("=== WORKSPACE DIRECTORY INSPECTION ===\n")

# Check if workspace directory exists and list all files
if os.path.exists('workspace'):
    print("Workspace directory exists")
    all_files = []
    for root, dirs, files in os.walk('workspace'):
        for file in files:
            full_path = os.path.join(root, file)
            file_size = os.path.getsize(full_path)
            all_files.append((full_path, file_size))
    
    print(f"Found {len(all_files)} files in workspace:")
    for file_path, size in all_files:
        print(f"  - {file_path} ({size} bytes)")
else:
    print("Workspace directory does not exist")

# Check for video_info.json file mentioned in the history
info_file = 'workspace/video_info.json'
if os.path.exists(info_file):
    print(f"\n=== INSPECTING VIDEO INFO FILE ===\n")
    print(f"Found video info file: {info_file}")
    
    # First inspect the structure safely
    with open(info_file, 'r', encoding='utf-8') as f:
        try:
            video_info = json.load(f)
            print(f"JSON file loaded successfully")
            print(f"Top-level keys: {list(video_info.keys())}")
            
            # Display each key-value pair safely
            for key, value in video_info.items():
                if isinstance(value, str):
                    if len(value) > 100:
                        print(f"  {key}: <string of length {len(value)}, preview: '{value[:100]}...'>")
                    else:
                        print(f"  {key}: '{value}'")
                elif isinstance(value, (int, float)):
                    print(f"  {key}: {value}")
                elif isinstance(value, list):
                    print(f"  {key}: <list with {len(value)} items: {value}>")
                else:
                    print(f"  {key}: {type(value)} - {value}")
                    
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
else:
    print(f"\nVideo info file not found: {info_file}")

# Now let's look for the actual downloaded video files with different approaches
print(f"\n=== SEARCHING FOR DOWNLOADED VIDEO FILES ===\n")

# Method 1: Look for common video extensions
video_extensions = ['.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv']
video_files_found = []

if os.path.exists('workspace'):
    for root, dirs, files in os.walk('workspace'):
        for file in files:
            file_lower = file.lower()
            for ext in video_extensions:
                if file_lower.endswith(ext):
                    full_path = os.path.join(root, file)
                    file_size = os.path.getsize(full_path)
                    video_files_found.append((full_path, file_size))
                    break

if video_files_found:
    print(f"Found {len(video_files_found)} video files:")
    for file_path, size in video_files_found:
        size_mb = size / (1024 * 1024)
        print(f"  - {file_path} ({size_mb:.2f} MB)")
else:
    print("No video files found with common extensions")

# Method 2: Look for files containing the video ID
video_id = "1htKBjuUWec"
print(f"\nSearching for files containing video ID '{video_id}':")

id_files_found = []
if os.path.exists('workspace'):
    for root, dirs, files in os.walk('workspace'):
        for file in files:
            if video_id in file:
                full_path = os.path.join(root, file)
                file_size = os.path.getsize(full_path)
                id_files_found.append((full_path, file_size))

if id_files_found:
    print(f"Found {len(id_files_found)} files containing video ID:")
    for file_path, size in id_files_found:
        size_mb = size / (1024 * 1024)
        print(f"  - {file_path} ({size_mb:.2f} MB)")
else:
    print(f"No files found containing video ID '{video_id}'")

# Method 3: Look for any files that might be the video based on size
print(f"\nLooking for files that might be video based on size (>500KB):")

large_files = []
if os.path.exists('workspace'):
    for root, dirs, files in os.walk('workspace'):
        for file in files:
            full_path = os.path.join(root, file)
            file_size = os.path.getsize(full_path)
            if file_size > 500 * 1024:  # Files larger than 500KB
                large_files.append((full_path, file_size))

if large_files:
    print(f"Found {len(large_files)} large files:")
    for file_path, size in large_files:
        size_mb = size / (1024 * 1024)
        print(f"  - {file_path} ({size_mb:.2f} MB)")
else:
    print("No large files found")

# Method 4: List ALL files in workspace with full details
print(f"\n=== COMPLETE WORKSPACE FILE LISTING ===\n")

if os.path.exists('workspace'):
    print("Complete file listing with details:")
    for root, dirs, files in os.walk('workspace'):
        print(f"Directory: {root}")
        if not files:
            print("  (empty directory)")
        for file in files:
            full_path = os.path.join(root, file)
            file_size = os.path.getsize(full_path)
            size_mb = file_size / (1024 * 1024)
            print(f"  - {file} -> {full_path} ({file_size} bytes / {size_mb:.2f} MB)")
        if dirs:
            print(f"  Subdirectories: {dirs}")
        print()
else:
    print("Workspace directory does not exist")

# Based on the tester feedback, the video was downloaded (667KB) but not detected
# Let's also check if there are any hidden files or files with unusual names
print(f"=== CHECKING FOR UNUSUAL FILE PATTERNS ===\n")

if os.path.exists('workspace'):
    import glob
    
    # Check for any files with unusual patterns
    all_patterns = [
        'workspace/*',
        'workspace/.*',  # Hidden files
        'workspace/*.*',
        'workspace/**/*',  # Recursive
    ]
    
    for pattern in all_patterns:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            print(f"Pattern '{pattern}' matches:")
            for match in matches:
                if os.path.isfile(match):
                    size = os.path.getsize(match)
                    print(f"  - {match} ({size} bytes)")
            print()

print("*** FILE INSPECTION COMPLETE ***")
print("\nNext step: Based on the file inspection results, proceed with audio extraction from the located video file.")
```

### Development Step 5: Extract Teal’c’s response to “Isn’t that hot?” from YouTube video 1htKBjuUWec.

**Description**: Access and analyze the YouTube video at https://www.youtube.com/watch?v=1htKBjuUWec to locate the specific dialogue where someone asks 'Isn't that hot?' and identify Teal'c's exact response. Extract the audio/video content, transcribe the relevant dialogue section, and document Teal'c's reply to this question.

**Use Cases**:
- Consumer electronics review video summarization and hot phrase detection for product marketing teams
- Podcast episode transcription and targeted keyword extraction for journalism archives
- Court deposition video transcription and specific quote identification for legal case preparations
- Academic lecture video segment tagging and concept extraction for e-learning curriculum development
- Compliance training video review to locate mandatory disclaimers and policy acknowledgments in corporate audit workflows
- Media archiving and cataloging to index iconic catchphrases and scene metadata in television episode databases
- Social media influencer video analysis to extract brand mentions and measure sentiment for marketing research
- Accessibility enhancement by transcribing video content and generating precise caption segments for hearing-impaired audiences

```
import os
import json
from pydub import AudioSegment
import speech_recognition as sr

# First, let's confirm the video file is in workspace and fix the variable naming issue
print("=== CONFIRMING VIDEO FILE AND EXTRACTING AUDIO ===\n")

# Check workspace contents
workspace_files = []
for file in os.listdir("workspace"):
    full_path = os.path.join("workspace", file)
    if os.path.isfile(full_path):
        file_size = os.path.getsize(full_path)
        workspace_files.append((file, full_path, file_size))

print(f"Files in workspace:")
video_file = None
for file_name, full_path, size in workspace_files:
    size_mb = size / (1024 * 1024)
    print(f"  - {file_name} ({size_mb:.2f} MB)")
    
    # Identify the video file (fix the variable naming issue from history)
    if any(file_name.lower().endswith(ext) for ext in ['.mp4', '.mkv', '.webm', '.avi']):
        video_file = full_path
        print(f"    *** IDENTIFIED AS VIDEO FILE ***")

if not video_file:
    print("\n*** ERROR: No video file found ***")
else:
    print(f"\n=== VIDEO FILE CONFIRMED ===")
    print(f"Video file: {video_file}")
    print(f"File size: {os.path.getsize(video_file) / (1024 * 1024):.2f} MB")
    
    # Extract audio from the video
    print(f"\n=== EXTRACTING AUDIO FROM VIDEO ===")
    
    try:
        # Load video and extract audio
        print("Loading video file with pydub...")
        video = AudioSegment.from_file(video_file)
        print(f"Video loaded successfully: {len(video)} ms duration")
        
        # Convert to seconds for readability
        duration_seconds = len(video) / 1000
        print(f"Duration: {duration_seconds:.1f} seconds")
        
        # Export audio as WAV for speech recognition
        audio_file = "workspace/tealc_coffee_audio.wav"
        print(f"Exporting audio to: {audio_file}")
        
        # Export with optimal settings for speech recognition
        video.export(audio_file, format="wav", parameters=["-ar", "16000", "-ac", "1"])
        
        audio_size = os.path.getsize(audio_file)
        print(f"Audio file created: {audio_size} bytes")
        
        print(f"\n=== TRANSCRIBING AUDIO TO TEXT ===")
        
        # Initialize speech recognizer
        recognizer = sr.Recognizer()
        print("Speech recognizer initialized")
        
        # Load the audio file for transcription
        with sr.AudioFile(audio_file) as source:
            print("Loading audio file for transcription...")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Adjusted for ambient noise")
            
            # Record the audio data
            audio_data = recognizer.record(source)
            print("Audio data recorded for transcription")
            
            try:
                print("\nAttempting transcription with Google Speech Recognition...")
                
                # Transcribe the audio
                transcription = recognizer.recognize_google(audio_data, language='en-US')
                
                print(f"\n*** TRANSCRIPTION SUCCESSFUL ***")
                print(f"Transcribed text length: {len(transcription)} characters")
                print(f"\n=== TEAL'C COFFEE SCENE TRANSCRIPTION ===")
                print(f"'{transcription}'")
                
                # Save the transcription
                transcription_file = "workspace/tealc_coffee_transcription.txt"
                with open(transcription_file, 'w', encoding='utf-8') as f:
                    f.write("TEAL'C COFFEE SCENE TRANSCRIPTION\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(f"Source: {os.path.basename(video_file)}\n")
                    f.write(f"Duration: {duration_seconds:.1f} seconds\n")
                    f.write(f"Transcribed: {transcription}\n\n")
                
                print(f"\nTranscription saved to: {transcription_file}")
                
                # Now search for the specific dialogue
                print(f"\n=== SEARCHING FOR 'ISN'T THAT HOT?' DIALOGUE ===")
                
                transcription_lower = transcription.lower()
                
                # Look for variations of "isn't that hot?"
                hot_patterns = [
                    "isn't that hot",
                    "isnt that hot", 
                    "is that hot",
                    "isn't it hot",
                    "isnt it hot",
                    "that hot",
                    "too hot",
                    "very hot"
                ]
                
                found_hot_question = False
                hot_question_context = ""
                for pattern in hot_patterns:
                    if pattern in transcription_lower:
                        print(f"*** FOUND HOT QUESTION PATTERN: '{pattern}' ***")
                        found_hot_question = True
                        
                        # Find the position of this pattern
                        start_pos = transcription_lower.find(pattern)
                        end_pos = start_pos + len(pattern)
                        
                        # Get context around the question
                        context_start = max(0, start_pos - 50)
                        context_end = min(len(transcription), end_pos + 100)
                        hot_question_context = transcription[context_start:context_end]
                        
                        print(f"Context: '{hot_question_context}'")
                        break
                
                if not found_hot_question:
                    print("No direct 'isn't that hot?' pattern found in transcription")
                    print("Let's analyze the full transcription for Teal'c's dialogue...")
                
                # Look for Teal'c's characteristic responses
                print(f"\n=== ANALYZING FOR TEAL'C'S RESPONSE ===")
                
                # Teal'c often gives short, direct responses
                # Let's look for his typical speech patterns
                tealc_patterns = [
                    "indeed",
                    "it is",
                    "i do not",
                    "negative",
                    "affirmative",
                    "most",
                    "extremely"
                ]
                
                tealc_responses_found = []
                for pattern in tealc_patterns:
                    if pattern in transcription_lower:
                        tealc_responses_found.append(pattern)
                        print(f"Found Teal'c pattern: '{pattern}'")
                
                # Analyze the dialogue structure to identify speakers and responses
                print(f"\n=== DIALOGUE STRUCTURE ANALYSIS ===")
                
                # Split transcription into sentences/phrases
                import re
                sentences = re.split(r'[.!?]+', transcription)
                sentences = [s.strip() for s in sentences if s.strip()]
                
                print(f"Dialogue broken into {len(sentences)} parts:")
                for i, sentence in enumerate(sentences, 1):
                    print(f"  {i}. '{sentence}'")
                
                # Create detailed analysis
                analysis = {
                    'video_file': video_file,
                    'duration_seconds': duration_seconds,
                    'full_transcription': transcription,
                    'dialogue_sentences': sentences,
                    'hot_question_found': found_hot_question,
                    'hot_question_context': hot_question_context,
                    'tealc_patterns_found': tealc_responses_found,
                    'objective': "Find Teal'c's response to 'Isn't that hot?'"
                }
                
                # Save detailed analysis
                with open('workspace/tealc_dialogue_analysis.json', 'w', encoding='utf-8') as f:
                    json.dump(analysis, f, indent=2)
                
                print(f"\n=== ANALYSIS SUMMARY ===")
                print(f"Full transcription: '{transcription}'")
                print(f"Hot question found: {found_hot_question}")
                print(f"Teal'c patterns found: {tealc_responses_found}")
                print(f"Dialogue parts: {len(sentences)}")
                
                # Determine Teal'c's response based on the analysis
                print(f"\n*** IDENTIFYING TEAL'C'S RESPONSE ***")
                
                if found_hot_question:
                    print(f"Hot question context found: '{hot_question_context}'")
                    # Look for Teal'c's response after the hot question
                    response_analysis = "Based on the context, Teal'c's response appears to be in the dialogue."
                else:
                    print("No explicit 'isn't that hot?' found, but analyzing complete dialogue for Teal'c's response...")
                    response_analysis = "Analyzing complete dialogue to identify Teal'c's characteristic response."
                
                # Save the final answer
                with open('workspace/tealc_final_answer.txt', 'w', encoding='utf-8') as f:
                    f.write("TEAL'C'S RESPONSE TO 'ISN'T THAT HOT?'\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Scene: Teal'c trying coffee for the first time\n")
                    f.write(f"Video: {os.path.basename(video_file)}\n")
                    f.write(f"Duration: {duration_seconds:.1f} seconds\n\n")
                    f.write(f"Complete dialogue transcription:\n")
                    f.write(f"'{transcription}'\n\n")
                    f.write(f"Hot question found: {found_hot_question}\n")
                    if found_hot_question:
                        f.write(f"Hot question context: '{hot_question_context}'\n")
                    f.write(f"\nDialogue breakdown:\n")
                    for i, sentence in enumerate(sentences, 1):
                        f.write(f"  {i}. '{sentence}'\n")
                    f.write(f"\nTeal'c patterns identified: {tealc_responses_found}\n")
                    f.write(f"\nAnalysis: {response_analysis}\n")
                
                print(f"\nDetailed analysis saved to: workspace/tealc_dialogue_analysis.json")
                print(f"Final answer saved to: workspace/tealc_final_answer.txt")
                
                print(f"\n*** TRANSCRIPTION AND ANALYSIS COMPLETE ***")
                print(f"The complete dialogue from the Teal'c coffee scene has been transcribed and analyzed.")
                print(f"Check the saved files for detailed analysis of Teal'c's response to questions about the coffee being hot.")
                
            except sr.UnknownValueError:
                print("\n*** TRANSCRIPTION FAILED ***")
                print("Google Speech Recognition could not understand the audio")
                print("The audio may be unclear, contain background noise, or have no speech")
                
                # Still save what we can
                with open('workspace/transcription_failed.txt', 'w') as f:
                    f.write("TRANSCRIPTION FAILED\n")
                    f.write(f"Video: {video_file}\n")
                    f.write(f"Duration: {duration_seconds:.1f} seconds\n")
                    f.write("Reason: Google Speech Recognition could not understand the audio\n")
                
            except sr.RequestError as e:
                print(f"\n*** SPEECH RECOGNITION SERVICE ERROR ***")
                print(f"Could not request results from Google Speech Recognition: {e}")
        
    except Exception as e:
        print(f"\n*** ERROR DURING AUDIO PROCESSING ***")
        print(f"Error: {str(e)}")
        import traceback
        print(f"Full error details: {traceback.format_exc()}")

print("\n*** TEAL'C DIALOGUE ANALYSIS COMPLETE ***")
```

### Development Step 1: AI Regulation Papers from arXiv (June 2022): Extract Axis Label Words from Three-Axis Figure

**Description**: Search arXiv.org for AI regulation papers originally submitted in June 2022. Focus on identifying papers that discuss artificial intelligence regulation, policy, governance, or related topics. Look for papers with submission dates in June 2022 and examine their content to find one containing a figure with three axes where each axis has label words at both ends. Extract the specific words used as axis labels in this figure.

**Use Cases**:
- Academic literature review for a university research team studying the evolution of AI regulation frameworks in mid-2022
- Automated policy landscape mapping for a government agency evaluating global trends in AI governance
- Corporate compliance team tracking recent scholarly discussions on AI ethics and regulatory challenges for risk assessment
- Legal analysts identifying precedent-setting academic papers on AI policy to inform technology law cases
- Think tank researchers extracting multidimensional frameworks from figures in AI regulation papers to visualize governance models
- Data scientists building a curated dataset of AI regulation literature with annotated axis labels for machine learning model training
- Journal editors screening June 2022 submissions for innovative visualizations of AI governance concepts
- Educational content creators sourcing authoritative diagrams from academic papers to illustrate AI policy concepts in online courses

```
import os
import requests
import json
from datetime import datetime
import time

print('=== SEARCHING ARXIV FOR AI REGULATION PAPERS FROM JUNE 2022 ===')
print('Objective: Find papers on AI regulation/policy/governance submitted in June 2022')
print('Target: Locate paper with figure having three axes with label words at both ends\n')

# Ensure workspace exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# arXiv API base URL
arxiv_base_url = 'http://export.arxiv.org/api/query'

# Search terms for AI regulation papers
search_queries = [
    'artificial intelligence regulation',
    'AI policy governance', 
    'artificial intelligence policy',
    'AI regulation framework',
    'machine learning governance',
    'AI ethics policy',
    'artificial intelligence governance'
]

print('=== STEP 1: SEARCHING ARXIV WITH MULTIPLE QUERY TERMS ===')

all_papers = []
search_results = {}

for i, query in enumerate(search_queries, 1):
    print(f'\nSearch {i}/{len(search_queries)}: "{query}"')
    
    # arXiv search parameters
    params = {
        'search_query': f'all:"{query}"',
        'start': 0,
        'max_results': 50,  # Get more results to filter by date
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    try:
        response = requests.get(arxiv_base_url, params=params, timeout=30)
        print(f'Status code: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw XML response
            xml_file = os.path.join(workspace, f'arxiv_search_{i}_{query.replace(" ", "_")}.xml')
            with open(xml_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f'✓ Raw XML saved to: {xml_file}')
            
            # Parse XML to extract paper information
            import xml.etree.ElementTree as ET
            
            try:
                root = ET.fromstring(response.text)
                
                # Define XML namespaces
                namespaces = {
                    'atom': 'http://www.w3.org/2005/Atom',
                    'arxiv': 'http://arxiv.org/schemas/atom'
                }
                
                entries = root.findall('atom:entry', namespaces)
                print(f'Found {len(entries)} papers for query "{query}"')
                
                query_papers = []
                
                for entry in entries:
                    # Extract paper details
                    title_elem = entry.find('atom:title', namespaces)
                    title = title_elem.text.strip() if title_elem is not None else 'No title'
                    
                    summary_elem = entry.find('atom:summary', namespaces)
                    summary = summary_elem.text.strip() if summary_elem is not None else 'No summary'
                    
                    published_elem = entry.find('atom:published', namespaces)
                    published = published_elem.text.strip() if published_elem is not None else 'No date'
                    
                    # Get arXiv ID and PDF link
                    id_elem = entry.find('atom:id', namespaces)
                    arxiv_id = id_elem.text.strip() if id_elem is not None else 'No ID'
                    
                    # Extract arXiv ID from URL
                    if 'arxiv.org/abs/' in arxiv_id:
                        arxiv_id = arxiv_id.split('/')[-1]
                    
                    # Construct PDF URL
                    pdf_url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'
                    
                    # Get authors
                    authors = []
                    author_elems = entry.findall('atom:author', namespaces)
                    for author_elem in author_elems:
                        name_elem = author_elem.find('atom:name', namespaces)
                        if name_elem is not None:
                            authors.append(name_elem.text.strip())
                    
                    paper_info = {
                        'title': title,
                        'authors': authors,
                        'summary': summary,
                        'published': published,
                        'arxiv_id': arxiv_id,
                        'pdf_url': pdf_url,
                        'search_query': query
                    }
                    
                    query_papers.append(paper_info)
                    all_papers.append(paper_info)
                
                search_results[query] = query_papers
                print(f'✓ Extracted {len(query_papers)} papers from XML')
                
            except ET.ParseError as e:
                print(f'Error parsing XML for query "{query}": {str(e)}')
                continue
        
        else:
            print(f'Failed to search arXiv: {response.status_code}')
            continue
    
    except Exception as e:
        print(f'Error searching for "{query}": {str(e)}')
        continue
    
    # Small delay between requests to be respectful to arXiv
    time.sleep(1)

print(f'\n=== STEP 2: FILTERING PAPERS BY JUNE 2022 SUBMISSION DATE ===')
print(f'Total papers found across all queries: {len(all_papers)}')

# Filter papers by June 2022 submission date
june_2022_papers = []

for paper in all_papers:
    published_date = paper['published']
    
    # Parse the date (arXiv format: 2022-06-15T17:59:59Z)
    try:
        if published_date and published_date != 'No date':
            # Extract year and month from date string
            if published_date.startswith('2022-06'):
                june_2022_papers.append(paper)
                print(f'✓ June 2022 paper found: "{paper["title"][:80]}..."')
                print(f'  Published: {published_date}')
                print(f'  arXiv ID: {paper["arxiv_id"]}')
                print(f'  Authors: {", ".join(paper["authors"][:3])}{", ..." if len(paper["authors"]) > 3 else ""}')
                print()
    
    except Exception as e:
        print(f'Error parsing date for paper: {str(e)}')
        continue

print(f'\n=== FILTERING RESULTS ===')
print(f'Papers from June 2022: {len(june_2022_papers)}')

if june_2022_papers:
    # Save June 2022 papers for detailed analysis
    june_papers_file = os.path.join(workspace, 'arxiv_june_2022_ai_regulation_papers.json')
    with open(june_papers_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_date': datetime.now().isoformat(),
            'total_papers_found': len(all_papers),
            'june_2022_papers_count': len(june_2022_papers),
            'search_queries_used': search_queries,
            'june_2022_papers': june_2022_papers
        }, f, indent=2, ensure_ascii=False)
    
    print(f'✓ June 2022 papers saved to: {june_papers_file}')
    
    # Display summary of June 2022 papers
    print(f'\n=== JUNE 2022 AI REGULATION PAPERS SUMMARY ===')
    for i, paper in enumerate(june_2022_papers, 1):
        print(f'\n{i}. Title: {paper["title"]}')
        print(f'   arXiv ID: {paper["arxiv_id"]}')
        print(f'   Published: {paper["published"]}')
        print(f'   Authors: {", ".join(paper["authors"][:2])}{", ..." if len(paper["authors"]) > 2 else ""}')
        print(f'   PDF: {paper["pdf_url"]}')
        print(f'   Summary preview: {paper["summary"][:200]}...')
    
    print(f'\n=== NEXT STEPS ===')
    print(f'✓ Found {len(june_2022_papers)} AI regulation papers from June 2022')
    print(f'✓ Ready to download and analyze PDFs for figures with three axes')
    print(f'✓ Will search for figures with axis labels at both ends')
    
else:
    print('\n⚠ No papers found from June 2022 with current search terms')
    print('May need to try broader search terms or different date filtering approach')
    
    # Save all search results for analysis
    all_results_file = os.path.join(workspace, 'arxiv_all_search_results.json')
    with open(all_results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_date': datetime.now().isoformat(),
            'total_papers_found': len(all_papers),
            'search_queries_used': search_queries,
            'all_papers': all_papers[:20]  # Save first 20 for inspection
        }, f, indent=2, ensure_ascii=False)
    
    print(f'All search results saved to: {all_results_file}')
    print('Will analyze date patterns and try alternative approaches')

print('\n*** ARXIV SEARCH PHASE COMPLETE ***')
```

### Development Step 3: Find and Transcribe Teal’c’s Response to “Isn’t That Hot?” in YouTube Video

**Description**: Access and analyze the YouTube video at https://www.youtube.com/watch?v=1htKBjuUWec to locate the specific dialogue where someone asks 'Isn't that hot?' and identify Teal'c's exact response. Extract the audio/video content, transcribe the relevant dialogue section, and document Teal'c's reply to this question.

**Use Cases**:
- Fan-driven Stargate quote archive: automatically download key scenes from YouTube, extract Teal’c’s “Isn’t that hot?” response, transcribe the dialogue and timestamp for inclusion in a community-maintained quote database
- Linguistic analysis of fictional dialects: pull audio clips of Teal’c’s speech from YouTube, transcribe targeted question-and-answer exchanges, and analyze phonetic patterns for a research paper on constructed languages
- Streaming subtitle generation and localization: isolate the “Isn’t that hot?” segment, produce a precise transcript of Teal’c’s reply, and feed it into a translation workflow to create accurate subtitles in multiple languages
- AI chatbot persona training for Sci-Fi characters: collect authentic Teal’c responses by downloading and transcribing specific lines, then integrate them into a chatbot to emulate his speech style in interactive fan applications
- Compliance audit for clip licensing: extract and document exact dialogue segments from YouTube videos, log Teal’c’s reply verbatim, and attach metadata for legal review when securing broadcast rights
- Podcast episode highlight reel: automate the download, audio extraction, and transcription of fan-favorite Teal’c lines like his response to “Isn’t that hot?”, then assemble them into a curated nostalgia segment
- Quality assurance for automatic captioning services: use the known “Isn’t that hot?” exchange to verify the accuracy of speech-to-text algorithms by comparing the system’s output to the manually extracted transcript
- Educational media analysis in film studies: retrieve and transcribe Teal’c’s concise responses from selected YouTube scenes, enabling film students to examine character development through repeated dialogue patterns

```
import os
import yt_dlp
import json
from urllib.parse import urlparse, parse_qs

# The issue is clear: the video was downloaded to a different workspace directory
# Let's re-download the video to the current workspace and then extract audio

url = "https://www.youtube.com/watch?v=1htKBjuUWec"
video_id = "1htKBjuUWec"

print("=== RE-DOWNLOADING TEAL'C VIDEO TO CURRENT WORKSPACE ===")
print(f"Target URL: {url}")
print(f"Video ID: {video_id}")
print("Objective: Download video, extract audio, and find Teal'c's response to 'Isn't that hot?'\n")

# Ensure current workspace directory exists
os.makedirs("workspace", exist_ok=True)
print(f"Workspace directory confirmed: {os.path.abspath('workspace')}")

# Set up download options to get the video in current workspace
output_template = os.path.join("workspace", f"{video_id}_%(title)s.%(ext)s")
print(f"Output template: {output_template}\n")

ydl_opts = {
    'format': 'best[height<=720]',  # Download reasonable quality video
    'outtmpl': output_template,
    'quiet': False,  # Show download progress
    'no_warnings': False,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract info first
        print("=== EXTRACTING VIDEO INFORMATION ===")
        info = ydl.extract_info(url, download=False)
        
        print(f"Video Title: {info.get('title', 'N/A')}")
        print(f"Duration: {info.get('duration', 'N/A')} seconds")
        print(f"Uploader: {info.get('uploader', 'N/A')}")
        
        # Confirm this is the Teal'c coffee video
        title = info.get('title', '').lower()
        if 'teal' in title and 'coffee' in title:
            print("*** CONFIRMED: This is the Teal'c coffee video ***\n")
        else:
            print(f"*** WARNING: Title doesn't clearly indicate Teal'c coffee content ***\n")
        
        # Now download the video
        print("=== DOWNLOADING VIDEO ===")
        ydl.download([url])
        print("\nVideo download completed!\n")
        
        # Check what files were actually created
        print("=== CHECKING DOWNLOADED FILES ===")
        workspace_files = []
        for file in os.listdir("workspace"):
            full_path = os.path.join("workspace", file)
            if os.path.isfile(full_path):
                file_size = os.path.getsize(full_path)
                workspace_files.append((file, full_path, file_size))
        
        print(f"Files in workspace after download:")
        video_file = None
        for filename, full_path, size in workspace_files:
            size_mb = size / (1024 * 1024)
            print(f"  - {filename} ({size_mb:.2f} MB)")
            
            # Identify the video file
            if any(filename.lower().endswith(ext) for ext in ['.mp4', '.mkv', '.webm', '.avi']):
                video_file = full_path
                print(f"    *** IDENTIFIED AS VIDEO FILE ***")
        
        if video_file:
            print(f"\n=== VIDEO FILE LOCATED ===")
            print(f"Video file path: {video_file}")
            print(f"File size: {os.path.getsize(video_file) / (1024 * 1024):.2f} MB")
            
            # Save video info for reference
            video_info = {
                'url': url,
                'video_id': video_id,
                'title': info.get('title', 'N/A'),
                'duration_seconds': info.get('duration', 0),
                'uploader': info.get('uploader', 'N/A'),
                'video_file_path': video_file,
                'file_size_mb': os.path.getsize(video_file) / (1024 * 1024),
                'objective': "Find Teal'c's response to 'Isn't that hot?'"
            }
            
            with open('workspace/tealc_video_info.json', 'w', encoding='utf-8') as f:
                json.dump(video_info, f, indent=2)
            
            print(f"Video info saved to: workspace/tealc_video_info.json")
            
            print(f"\n=== READY FOR AUDIO EXTRACTION ===")
            print("Video successfully downloaded and located.")
            print("Next step: Extract audio from video for dialogue transcription.")
            
        else:
            print(f"\n*** ERROR: No video file found after download ***")
            print("Available files:")
            for filename, full_path, size in workspace_files:
                print(f"  - {filename} ({size} bytes)")
            
except Exception as e:
    print(f"\n*** ERROR DURING VIDEO DOWNLOAD ***")
    print(f"Error: {str(e)}")
    import traceback
    print(f"Full error details: {traceback.format_exc()}")

print("\n*** VIDEO DOWNLOAD PHASE COMPLETE ***")
```

## Created Time
2025-08-14 02:17:47
