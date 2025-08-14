# Developer Plan 01

## Plan
Research the Yola word 'gimlie' to identify its Latin root, then find the Spanish word that shares the same spelling as this Latin root. Focus on searching for Yola language dictionaries, etymological resources, or linguistic studies that document the word 'gimlie' and trace its etymology back to Latin origins.

## Description
This is the optimal first step because: (1) We need to establish the etymology of the Yola word 'gimlie' to identify its Latin root, (2) No previous research has been conducted on this multi-step linguistic task, (3) Expected outcome is to find the Latin root of 'gimlie' and identify the corresponding Spanish word with identical spelling, (4) This provides the foundation needed to then search the Collins Spanish-to-English dictionary for the 1994 example sentence and its source title

## Episodic Examples
### Development Step 3: Download words_alpha and Implement Boggle Solver for 4×4 Board, Return Longest Word

**Description**: Download the words_alpha dictionary from https://github.com/dwyl/english-words to workspace/words_alpha.txt and then implement a Boggle solver to find all valid words that can be formed from the given 4x4 board (ABRL/EITE/IONS/FPEI) using the downloaded dictionary. The solver should check all possible paths on the board where adjacent cells (including diagonally adjacent) can be visited exactly once per word, then identify the longest valid English word(s) and return the alphabetically first one if there are ties.

**Use Cases**:
- Real-time Boggle tournament assistant integrated into digital board game platforms to suggest optimal word paths and improve player strategies
- Automated quality assurance for mobile word games, verifying that each 4×4 puzzle grid has a valid solution and meets predefined difficulty criteria
- Educational spelling tool for elementary classrooms, generating customized letter boards and word lists to reinforce vocabulary and phonics lessons
- Puzzle difficulty calibration for tabletop game designers, analyzing letter distributions and longest word possibilities to balance game challenges before publication
- Cognitive training app for seniors, creating daily timed word-finding exercises with varying board configurations to maintain and assess mental agility
- Linguistic research on letter adjacency and lexical networks, applying the solver to large corpora of letter matrices extracted from historical manuscripts
- Marketing campaign ideation platform that transforms brand names into thematic Boggle boards and derives creative taglines or product descriptors
- Accessibility feature for visually impaired gamers, combining screen readers with the solver to vocalize found words and guide users through optimal letter paths

```
import os
import requests
from collections import defaultdict
import time

# Define all helper functions at the very beginning to ensure global scope
def get_neighbors(row, col, rows, cols):
    """Get all adjacent cells (including diagonal) for a given position"""
    neighbors = []
    # Check all 8 directions: up, down, left, right, and 4 diagonals
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # up-left, up, up-right
        (0, -1),           (0, 1),   # left, right
        (1, -1),  (1, 0),  (1, 1)    # down-left, down, down-right
    ]
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    
    return neighbors

def find_words_from_position(board, dictionary, start_row, start_col, visited, current_word, found_words):
    """Recursively find all valid words starting from a given position"""
    rows, cols = len(board), len(board[0])
    
    # Add current letter to the word
    current_word += board[start_row][start_col].lower()
    
    # Mark current position as visited
    visited.add((start_row, start_col))
    
    # Check if current word is valid and has reasonable length (3+ letters)
    if len(current_word) >= 3 and current_word in dictionary:
        found_words.add(current_word)
        print(f'Found valid word: "{current_word}" (length: {len(current_word)})')
    
    # Continue searching if word length is reasonable (prevent excessive recursion)
    if len(current_word) < 15:  # Reasonable max word length
        # Get all adjacent neighbors
        neighbors = get_neighbors(start_row, start_col, rows, cols)
        
        for next_row, next_col in neighbors:
            # Only visit unvisited cells
            if (next_row, next_col) not in visited:
                # Create a new copy of visited set for this branch
                new_visited = visited.copy()
                find_words_from_position(board, dictionary, next_row, next_col, new_visited, current_word, found_words)

def solve_boggle(board, dictionary):
    """Solve the Boggle puzzle and return all valid words"""
    found_words = set()
    rows, cols = len(board), len(board[0])
    
    print(f'Starting Boggle solve for {rows}x{cols} board...')
    print(f'Dictionary size: {len(dictionary):,} words')
    
    # Start search from each position on the board
    for row in range(rows):
        for col in range(cols):
            print(f'\nSearching from position ({row},{col}) - letter "{board[row][col]}":')
            visited = set()
            find_words_from_position(board, dictionary, row, col, visited, '', found_words)
    
    return found_words

print('=== BOGGLE SOLVER IMPLEMENTATION - SCOPE FIXED VERSION ===')
print('All functions defined at global scope to fix execution issues\n')

# Ensure workspace directory exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# Check if dictionary already exists, if not download it
words_file_path = os.path.join(workspace, 'words_alpha.txt')

if not os.path.exists(words_file_path):
    print('Step 1: Downloading words_alpha dictionary from GitHub\n')
    
    words_url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
    print(f'Downloading dictionary from: {words_url}')
    print(f'Saving to: {words_file_path}')
    
    try:
        response = requests.get(words_url, timeout=30)
        print(f'Response status: {response.status_code}')
        
        if response.status_code == 200:
            with open(words_file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'✓ Dictionary downloaded successfully')
            print(f'File size: {len(response.text):,} characters')
            
            # Count number of words
            word_count = len(response.text.strip().split('\n'))
            print(f'Total words in dictionary: {word_count:,}')
            
        else:
            print(f'Error downloading dictionary: HTTP {response.status_code}')
            
    except Exception as e:
        print(f'Error downloading dictionary: {e}')
else:
    print('✓ Dictionary file already exists, skipping download')

print('\n=== STEP 2: LOADING DICTIONARY INTO MEMORY ===')

# Load the dictionary into a set for fast lookup
if os.path.exists(words_file_path):
    print(f'Loading dictionary from: {words_file_path}')
    
    with open(words_file_path, 'r', encoding='utf-8') as f:
        dictionary_words = set(word.strip().lower() for word in f if word.strip())
    
    print(f'✓ Dictionary loaded: {len(dictionary_words):,} unique words')
    
    # Check some common words to verify dictionary quality
    test_words = ['the', 'and', 'hello', 'world', 'python', 'boggle']
    print(f'\nTesting common words in dictionary:')
    for word in test_words:
        in_dict = word in dictionary_words
        print(f'  "{word}": {"✓" if in_dict else "✗"}')
else:
    print('Error: Dictionary file not found!')
    dictionary_words = set()

print('\n=== STEP 3: DEFINING THE 4x4 BOGGLE BOARD ===')

# Define the 4x4 Boggle board as given in the plan
# ABRL
# EITE  
# IONS
# FPEI

boggle_board = [
    ['A', 'B', 'R', 'L'],
    ['E', 'I', 'T', 'E'], 
    ['I', 'O', 'N', 'S'],
    ['F', 'P', 'E', 'I']
]

print('Boggle board:')
for i, row in enumerate(boggle_board):
    print(f'Row {i}: {" ".join(row)}')

print(f'\nBoard dimensions: {len(boggle_board)}x{len(boggle_board[0])}')

# Verify board structure
total_letters = sum(len(row) for row in boggle_board)
print(f'Total letters on board: {total_letters}')

# Count letter frequency
letter_count = defaultdict(int)
for row in boggle_board:
    for letter in row:
        letter_count[letter] += 1

print(f'Letter frequency: {dict(letter_count)}')

print('\n=== STEP 4: RUNNING BOGGLE SOLVER ===')

if dictionary_words:
    print('Starting Boggle word search...')
    start_time = time.time()
    
    # Solve the Boggle puzzle
    all_found_words = solve_boggle(boggle_board, dictionary_words)
    
    end_time = time.time()
    solve_time = end_time - start_time
    
    print(f'\n=== BOGGLE SOLVE COMPLETE ===')
    print(f'Solve time: {solve_time:.2f} seconds')
    print(f'Total valid words found: {len(all_found_words)}')
    
    if all_found_words:
        # Sort words by length (descending) then alphabetically
        sorted_words = sorted(all_found_words, key=lambda w: (-len(w), w))
        
        print(f'\n=== ALL FOUND WORDS (sorted by length, then alphabetically) ===')
        current_length = None
        for word in sorted_words:
            if len(word) != current_length:
                current_length = len(word)
                print(f'\n--- {current_length}-letter words ---')
            print(f'  {word}')
        
        # Find the longest word(s)
        max_length = max(len(word) for word in all_found_words)
        longest_words = [word for word in all_found_words if len(word) == max_length]
        longest_words.sort()  # Sort alphabetically
        
        print(f'\n=== LONGEST WORD(S) FOUND ===')
        print(f'Maximum word length: {max_length} letters')
        print(f'Number of longest words: {len(longest_words)}')
        print(f'Longest words: {longest_words}')
        
        # Return the alphabetically first longest word
        answer = longest_words[0]
        print(f'\n*** FINAL ANSWER: "{answer}" ***')
        print(f'Length: {len(answer)} letters')
        
        # Save results to file
        results_file = os.path.join(workspace, 'boggle_solver_results.txt')
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write('BOGGLE SOLVER RESULTS\n')
            f.write('=' * 50 + '\n\n')
            f.write('Board:\n')
            for row in boggle_board:
                f.write(' '.join(row) + '\n')
            f.write(f'\nTotal words found: {len(all_found_words)}\n')
            f.write(f'Longest word length: {max_length}\n')
            f.write(f'Longest word (alphabetically first): {answer}\n\n')
            f.write('All words by length:\n')
            f.write('-' * 30 + '\n')
            current_length = None
            for word in sorted_words:
                if len(word) != current_length:
                    current_length = len(word)
                    f.write(f'\n{current_length}-letter words:\n')
                f.write(f'  {word}\n')
        
        print(f'\n✓ Complete results saved to: {results_file}')
        
    else:
        print('No valid words found!')
else:
    print('Error: Dictionary not loaded, cannot solve Boggle puzzle')
```

### Development Step 4: Implement 4x4 Boggle solver using words_alpha dictionary to find longest valid word

**Description**: Download the words_alpha dictionary from https://github.com/dwyl/english-words to workspace/words_alpha.txt and then implement a Boggle solver to find all valid words that can be formed from the given 4x4 board (ABRL/EITE/IONS/FPEI) using the downloaded dictionary. The solver should check all possible paths on the board where adjacent cells (including diagonally adjacent) can be visited exactly once per word, then identify the longest valid English word(s) and return the alphabetically first one if there are ties.

**Use Cases**:
- Real-time word validation and scoring engine integration for mobile Boggle-like game platforms
- Automated puzzle difficulty assessment and 4×4 board generation for weekly print and digital puzzle publications
- Student vocabulary enhancement and custom exercise creation for ESL classrooms using dynamic board solvers
- Cognitive psychology experiment design and participant response tracking for research into spatial word retrieval strategies
- Social media gamification and interactive marketing campaign deployment for brand engagement via word-search challenges
- NLP model benchmarking and vocabulary coverage analysis for evaluating large language models’ ability to find valid word paths
- Crossword clue suggestion and obscure word discovery for puzzle editors creating fresh content based on random letter matrices
- Accessibility tool development and dyslexia-friendly word practice for special needs educational software

```
import os
import requests
from collections import defaultdict
import time

print('=== BOGGLE SOLVER IMPLEMENTATION - CLASS-BASED APPROACH ===')
print('Using class-based structure to avoid function scope issues\n')

# Ensure workspace directory exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# Check if dictionary already exists, if not download it
words_file_path = os.path.join(workspace, 'words_alpha.txt')

if not os.path.exists(words_file_path):
    print('Step 1: Downloading words_alpha dictionary from GitHub\n')
    
    words_url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
    print(f'Downloading dictionary from: {words_url}')
    print(f'Saving to: {words_file_path}')
    
    try:
        response = requests.get(words_url, timeout=30)
        print(f'Response status: {response.status_code}')
        
        if response.status_code == 200:
            with open(words_file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'✓ Dictionary downloaded successfully')
            print(f'File size: {len(response.text):,} characters')
            
            # Count number of words
            word_count = len(response.text.strip().split('\n'))
            print(f'Total words in dictionary: {word_count:,}')
            
        else:
            print(f'Error downloading dictionary: HTTP {response.status_code}')
            
    except Exception as e:
        print(f'Error downloading dictionary: {e}')
else:
    print('✓ Dictionary file already exists, skipping download')

print('\n=== STEP 2: LOADING DICTIONARY INTO MEMORY ===')

# Load the dictionary into a set for fast lookup
if os.path.exists(words_file_path):
    print(f'Loading dictionary from: {words_file_path}')
    
    with open(words_file_path, 'r', encoding='utf-8') as f:
        dictionary_words = set(word.strip().lower() for word in f if word.strip())
    
    print(f'✓ Dictionary loaded: {len(dictionary_words):,} unique words')
    
    # Check some common words to verify dictionary quality
    test_words = ['the', 'and', 'hello', 'world', 'python', 'boggle']
    print(f'\nTesting common words in dictionary:')
    for word in test_words:
        in_dict = word in dictionary_words
        print(f'  "{word}": {"✓" if in_dict else "✗"}')
else:
    print('Error: Dictionary file not found!')
    dictionary_words = set()

print('\n=== STEP 3: DEFINING THE 4x4 BOGGLE BOARD ===')

# Define the 4x4 Boggle board as given in the plan
# ABRL
# EITE  
# IONS
# FPEI

boggle_board = [
    ['A', 'B', 'R', 'L'],
    ['E', 'I', 'T', 'E'], 
    ['I', 'O', 'N', 'S'],
    ['F', 'P', 'E', 'I']
]

print('Boggle board:')
for i, row in enumerate(boggle_board):
    print(f'Row {i}: {" ".join(row)}')

print(f'\nBoard dimensions: {len(boggle_board)}x{len(boggle_board[0])}')

# Verify board structure
total_letters = sum(len(row) for row in boggle_board)
print(f'Total letters on board: {total_letters}')

# Count letter frequency
letter_count = defaultdict(int)
for row in boggle_board:
    for letter in row:
        letter_count[letter] += 1

print(f'Letter frequency: {dict(letter_count)}')

print('\n=== STEP 4: IMPLEMENTING BOGGLE SOLVER CLASS ===')

class BoggleSolver:
    def __init__(self, board, dictionary):
        self.board = board
        self.dictionary = dictionary
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0
        self.found_words = set()
        
    def get_neighbors(self, row, col):
        """Get all adjacent cells (including diagonal) for a given position"""
        neighbors = []
        # Check all 8 directions: up, down, left, right, and 4 diagonals
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # up-left, up, up-right
            (0, -1),           (0, 1),   # left, right
            (1, -1),  (1, 0),  (1, 1)    # down-left, down, down-right
        ]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def find_words_from_position(self, start_row, start_col, visited, current_word):
        """Recursively find all valid words starting from a given position"""
        # Add current letter to the word
        current_word += self.board[start_row][start_col].lower()
        
        # Mark current position as visited
        visited.add((start_row, start_col))
        
        # Check if current word is valid and has reasonable length (3+ letters)
        if len(current_word) >= 3 and current_word in self.dictionary:
            self.found_words.add(current_word)
            print(f'Found valid word: "{current_word}" (length: {len(current_word)})')
        
        # Continue searching if word length is reasonable (prevent excessive recursion)
        if len(current_word) < 15:  # Reasonable max word length
            # Get all adjacent neighbors
            neighbors = self.get_neighbors(start_row, start_col)
            
            for next_row, next_col in neighbors:
                # Only visit unvisited cells
                if (next_row, next_col) not in visited:
                    # Create a new copy of visited set for this branch
                    new_visited = visited.copy()
                    self.find_words_from_position(next_row, next_col, new_visited, current_word)
    
    def solve(self):
        """Solve the Boggle puzzle and return all valid words"""
        print(f'Starting Boggle solve for {self.rows}x{self.cols} board...')
        print(f'Dictionary size: {len(self.dictionary):,} words')
        
        # Start search from each position on the board
        for row in range(self.rows):
            for col in range(self.cols):
                print(f'\nSearching from position ({row},{col}) - letter "{self.board[row][col]}":')
                visited = set()
                self.find_words_from_position(row, col, visited, '')
        
        return self.found_words

print('✓ BoggleSolver class defined successfully')

print('\n=== STEP 5: RUNNING BOGGLE SOLVER ===')

if dictionary_words:
    print('Starting Boggle word search...')
    start_time = time.time()
    
    # Create solver instance and solve the puzzle
    solver = BoggleSolver(boggle_board, dictionary_words)
    all_found_words = solver.solve()
    
    end_time = time.time()
    solve_time = end_time - start_time
    
    print(f'\n=== BOGGLE SOLVE COMPLETE ===')
    print(f'Solve time: {solve_time:.2f} seconds')
    print(f'Total valid words found: {len(all_found_words)}')
    
    if all_found_words:
        # Sort words by length (descending) then alphabetically
        sorted_words = sorted(all_found_words, key=lambda w: (-len(w), w))
        
        print(f'\n=== ALL FOUND WORDS (sorted by length, then alphabetically) ===')
        current_length = None
        for word in sorted_words:
            if len(word) != current_length:
                current_length = len(word)
                print(f'\n--- {current_length}-letter words ---')
            print(f'  {word}')
        
        # Find the longest word(s)
        max_length = max(len(word) for word in all_found_words)
        longest_words = [word for word in all_found_words if len(word) == max_length]
        longest_words.sort()  # Sort alphabetically
        
        print(f'\n=== LONGEST WORD(S) FOUND ===')
        print(f'Maximum word length: {max_length} letters')
        print(f'Number of longest words: {len(longest_words)}')
        print(f'Longest words: {longest_words}')
        
        # Return the alphabetically first longest word
        answer = longest_words[0]
        print(f'\n*** FINAL ANSWER: "{answer}" ***')
        print(f'Length: {len(answer)} letters')
        
        # Save results to file
        results_file = os.path.join(workspace, 'boggle_solver_results.txt')
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write('BOGGLE SOLVER RESULTS\n')
            f.write('=' * 50 + '\n\n')
            f.write('Board:\n')
            for row in boggle_board:
                f.write(' '.join(row) + '\n')
            f.write(f'\nTotal words found: {len(all_found_words)}\n')
            f.write(f'Longest word length: {max_length}\n')
            f.write(f'Longest word (alphabetically first): {answer}\n\n')
            f.write('All words by length:\n')
            f.write('-' * 30 + '\n')
            current_length = None
            for word in sorted_words:
                if len(word) != current_length:
                    current_length = len(word)
                    f.write(f'\n{current_length}-letter words:\n')
                f.write(f'  {word}\n')
        
        print(f'\n✓ Complete results saved to: {results_file}')
        
    else:
        print('No valid words found!')
else:
    print('Error: Dictionary not loaded, cannot solve Boggle puzzle')
```

### Development Step 1: 4x4 Boggle Solver with words_alpha Dictionary to Find Longest Valid Word

**Description**: Download the words_alpha dictionary from https://github.com/dwyl/english-words to workspace/words_alpha.txt and then implement a Boggle solver to find all valid words that can be formed from the given 4x4 board (ABRL/EITE/IONS/FPEI) using the downloaded dictionary. The solver should check all possible paths on the board where adjacent cells (including diagonally adjacent) can be visited exactly once per word, then identify the longest valid English word(s) and return the alphabetically first one if there are ties.

**Use Cases**:
- ESL vocabulary assessment tool for educators: generate custom 4×4 boards aligned to lesson vocab lists, automatically solve them to create answer keys and track student progress
- Word-game app development and difficulty calibration: integrate the solver to validate player inputs in real time, ensure boards yield a target number of valid words, and dynamically adjust board complexity
- Linguistic pattern research and statistical analysis: analyze thousands of random Boggle boards to study word-length distribution, letter adjacency effects, and frequency of rare words in large English corpora
- Puzzle quality assurance in game design: automatically test proposed board layouts to verify minimum and maximum possible word lengths, ensuring puzzles are solvable and meet design criteria
- Competitive Boggle training and performance analytics: enable tournament players to upload board snapshots, receive full solution lists with scoring insights, and identify high-value word paths to refine strategy
- Assistive technology for visually impaired gamers: integrate the solver with voice-based interfaces to read out possible word paths and word lists, making Boggle accessible via screen readers
- Marketing and branding brainstorming: agencies input sets of campaign-specific letters to discover valid, memorable words and acronyms for product naming and slogan generation
- AI algorithm benchmarking and complexity testing: use Boggle solving as a standardized search and language-comprehension challenge to compare path-finding optimizations and dictionary lookup strategies

```
import os
import requests
from collections import defaultdict
import time

print('=== BOGGLE SOLVER IMPLEMENTATION ===')
print('Step 1: Downloading words_alpha dictionary from GitHub\n')

# Ensure workspace directory exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# Download the words_alpha.txt file from GitHub
words_url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
words_file_path = os.path.join(workspace, 'words_alpha.txt')

print(f'Downloading dictionary from: {words_url}')
print(f'Saving to: {words_file_path}')

try:
    response = requests.get(words_url, timeout=30)
    print(f'Response status: {response.status_code}')
    
    if response.status_code == 200:
        with open(words_file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f'✓ Dictionary downloaded successfully')
        print(f'File size: {len(response.text):,} characters')
        
        # Count number of words
        word_count = len(response.text.strip().split('\n'))
        print(f'Total words in dictionary: {word_count:,}')
        
        # Show first few words as sample
        sample_words = response.text.strip().split('\n')[:10]
        print(f'Sample words: {sample_words}')
        
    else:
        print(f'Error downloading dictionary: HTTP {response.status_code}')
        print(f'Response: {response.text[:200]}...')
        
except Exception as e:
    print(f'Error downloading dictionary: {e}')

print('\n=== STEP 2: LOADING DICTIONARY INTO MEMORY ===')

# Load the dictionary into a set for fast lookup
if os.path.exists(words_file_path):
    print(f'Loading dictionary from: {words_file_path}')
    
    with open(words_file_path, 'r', encoding='utf-8') as f:
        dictionary_words = set(word.strip().lower() for word in f if word.strip())
    
    print(f'✓ Dictionary loaded: {len(dictionary_words):,} unique words')
    print(f'Sample words from loaded dictionary: {list(dictionary_words)[:10]}')
    
    # Check some common words to verify dictionary quality
    test_words = ['the', 'and', 'hello', 'world', 'python', 'boggle']
    print(f'\nTesting common words in dictionary:')
    for word in test_words:
        in_dict = word in dictionary_words
        print(f'  "{word}": {"✓" if in_dict else "✗"}')
else:
    print('Error: Dictionary file not found!')
    dictionary_words = set()

print('\n=== STEP 3: DEFINING THE 4x4 BOGGLE BOARD ===')

# Define the 4x4 Boggle board as given in the plan
# ABRL
# EITE  
# IONS
# FPEI

boggle_board = [
    ['A', 'B', 'R', 'L'],
    ['E', 'I', 'T', 'E'], 
    ['I', 'O', 'N', 'S'],
    ['F', 'P', 'E', 'I']
]

print('Boggle board:')
for i, row in enumerate(boggle_board):
    print(f'Row {i}: {" ".join(row)}')

print(f'\nBoard dimensions: {len(boggle_board)}x{len(boggle_board[0])}')

# Verify board structure
total_letters = sum(len(row) for row in boggle_board)
print(f'Total letters on board: {total_letters}')

# Count letter frequency
letter_count = defaultdict(int)
for row in boggle_board:
    for letter in row:
        letter_count[letter] += 1

print(f'Letter frequency: {dict(letter_count)}')

print('\n=== STEP 4: IMPLEMENTING BOGGLE SOLVER ALGORITHM ===')

def get_neighbors(row, col, rows, cols):
    """Get all adjacent cells (including diagonal) for a given position"""
    neighbors = []
    # Check all 8 directions: up, down, left, right, and 4 diagonals
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # up-left, up, up-right
        (0, -1),           (0, 1),   # left, right
        (1, -1),  (1, 0),  (1, 1)    # down-left, down, down-right
    ]
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    
    return neighbors

def find_words_from_position(board, dictionary, start_row, start_col, visited, current_word, found_words):
    """Recursively find all valid words starting from a given position"""
    rows, cols = len(board), len(board[0])
    
    # Add current letter to the word
    current_word += board[start_row][start_col].lower()
    
    # Mark current position as visited
    visited.add((start_row, start_col))
    
    # Check if current word is valid and has reasonable length (3+ letters)
    if len(current_word) >= 3 and current_word in dictionary:
        found_words.add(current_word)
        print(f'Found valid word: "{current_word}" (length: {len(current_word)})')
    
    # Continue searching if word length is reasonable (prevent excessive recursion)
    if len(current_word) < 15:  # Reasonable max word length
        # Get all adjacent neighbors
        neighbors = get_neighbors(start_row, start_col, rows, cols)
        
        for next_row, next_col in neighbors:
            # Only visit unvisited cells
            if (next_row, next_col) not in visited:
                find_words_from_position(board, dictionary, next_row, next_col, visited.copy(), current_word, found_words)

def solve_boggle(board, dictionary):
    """Solve the Boggle puzzle and return all valid words"""
    found_words = set()
    rows, cols = len(board), len(board[0])
    
    print(f'Starting Boggle solve for {rows}x{cols} board...')
    print(f'Dictionary size: {len(dictionary):,} words')
    
    # Start search from each position on the board
    for row in range(rows):
        for col in range(cols):
            print(f'\nSearching from position ({row},{col}) - letter "{board[row][col]}":')
            visited = set()
            find_words_from_position(board, dictionary, row, col, visited, '', found_words)
    
    return found_words

print('\n=== STEP 5: RUNNING BOGGLE SOLVER ===')

if dictionary_words:
    print('Starting Boggle word search...')
    start_time = time.time()
    
    # Solve the Boggle puzzle
    all_found_words = solve_boggle(boggle_board, dictionary_words)
    
    end_time = time.time()
    solve_time = end_time - start_time
    
    print(f'\n=== BOGGLE SOLVE COMPLETE ===')
    print(f'Solve time: {solve_time:.2f} seconds')
    print(f'Total valid words found: {len(all_found_words)}')
    
    if all_found_words:
        # Sort words by length (descending) then alphabetically
        sorted_words = sorted(all_found_words, key=lambda w: (-len(w), w))
        
        print(f'\n=== ALL FOUND WORDS (sorted by length, then alphabetically) ===')
        current_length = None
        for word in sorted_words:
            if len(word) != current_length:
                current_length = len(word)
                print(f'\n--- {current_length}-letter words ---')
            print(f'  {word}')
        
        # Find the longest word(s)
        max_length = max(len(word) for word in all_found_words)
        longest_words = [word for word in all_found_words if len(word) == max_length]
        longest_words.sort()  # Sort alphabetically
        
        print(f'\n=== LONGEST WORD(S) FOUND ===')
        print(f'Maximum word length: {max_length} letters')
        print(f'Number of longest words: {len(longest_words)}')
        print(f'Longest words: {longest_words}')
        
        # Return the alphabetically first longest word
        answer = longest_words[0]
        print(f'\n*** FINAL ANSWER: "{answer}" ***')
        print(f'Length: {len(answer)} letters')
        
        # Save results to file
        results_file = os.path.join(workspace, 'boggle_solver_results.txt')
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write('BOGGLE SOLVER RESULTS\n')
            f.write('=' * 50 + '\n\n')
            f.write('Board:\n')
            for row in boggle_board:
                f.write(' '.join(row) + '\n')
            f.write(f'\nTotal words found: {len(all_found_words)}\n')
            f.write(f'Longest word length: {max_length}\n')
            f.write(f'Longest word (alphabetically first): {answer}\n\n')
            f.write('All words by length:\n')
            f.write('-' * 30 + '\n')
            current_length = None
            for word in sorted_words:
                if len(word) != current_length:
                    current_length = len(word)
                    f.write(f'\n{current_length}-letter words:\n')
                f.write(f'  {word}\n')
        
        print(f'\n✓ Complete results saved to: {results_file}')
        
    else:
        print('No valid words found!')
else:
    print('Error: Dictionary not loaded, cannot solve Boggle puzzle')
```

### Development Step 2: Build Boggle solver using words_alpha dictionary to find longest word on 4x4 board

**Description**: Download the words_alpha dictionary from https://github.com/dwyl/english-words to workspace/words_alpha.txt and then implement a Boggle solver to find all valid words that can be formed from the given 4x4 board (ABRL/EITE/IONS/FPEI) using the downloaded dictionary. The solver should check all possible paths on the board where adjacent cells (including diagonally adjacent) can be visited exactly once per word, then identify the longest valid English word(s) and return the alphabetically first one if there are ties.

**Use Cases**:
- Mobile game QA and level design validation to ensure every 4×4 Boggle board has at least one solution and identify the optimal longest word before release
- Educational app vocabulary exercises that generate random letter grids for ESL students and automatically retrieve valid word lists to support lesson plans
- Real-time word verification and scoring engine for Boggle tournaments and online competitions, enabling instant feedback and accurate leaderboards
- Cognitive psychology research tool to analyze board complexity by computing distributions of word lengths and branching paths for human performance studies
- Accessibility assistant for visually impaired players that converts spoken or tactile Boggle boards into text and uses the solver to read out possible words and hints
- Social media engagement feature that publishes daily Boggle puzzles with precomputed solution sets to boost community interaction and shareability
- Chatbot or virtual assistant integration that solves user-submitted 4×4 letter puzzles on demand, enhancing conversational game experiences
- Marketing campaign gamification that embeds custom word-finding challenges in newsletters or microsites with automated answer validation and prize entry mechanisms

```
import os
import requests
from collections import defaultdict
import time

print('=== BOGGLE SOLVER IMPLEMENTATION - FIXED VERSION ===')
print('Fixing function scope issue from previous attempt\n')

# Ensure workspace directory exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# Check if dictionary already exists, if not download it
words_file_path = os.path.join(workspace, 'words_alpha.txt')

if not os.path.exists(words_file_path):
    print('Step 1: Downloading words_alpha dictionary from GitHub\n')
    
    words_url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
    print(f'Downloading dictionary from: {words_url}')
    print(f'Saving to: {words_file_path}')
    
    try:
        response = requests.get(words_url, timeout=30)
        print(f'Response status: {response.status_code}')
        
        if response.status_code == 200:
            with open(words_file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'✓ Dictionary downloaded successfully')
            print(f'File size: {len(response.text):,} characters')
            
            # Count number of words
            word_count = len(response.text.strip().split('\n'))
            print(f'Total words in dictionary: {word_count:,}')
            
        else:
            print(f'Error downloading dictionary: HTTP {response.status_code}')
            
    except Exception as e:
        print(f'Error downloading dictionary: {e}')
else:
    print('✓ Dictionary file already exists, skipping download')

print('\n=== STEP 2: LOADING DICTIONARY INTO MEMORY ===')

# Load the dictionary into a set for fast lookup
if os.path.exists(words_file_path):
    print(f'Loading dictionary from: {words_file_path}')
    
    with open(words_file_path, 'r', encoding='utf-8') as f:
        dictionary_words = set(word.strip().lower() for word in f if word.strip())
    
    print(f'✓ Dictionary loaded: {len(dictionary_words):,} unique words')
    
    # Check some common words to verify dictionary quality
    test_words = ['the', 'and', 'hello', 'world', 'python', 'boggle']
    print(f'\nTesting common words in dictionary:')
    for word in test_words:
        in_dict = word in dictionary_words
        print(f'  "{word}": {"✓" if in_dict else "✗"}')
else:
    print('Error: Dictionary file not found!')
    dictionary_words = set()

print('\n=== STEP 3: DEFINING THE 4x4 BOGGLE BOARD ===')

# Define the 4x4 Boggle board as given in the plan
# ABRL
# EITE  
# IONS
# FPEI

boggle_board = [
    ['A', 'B', 'R', 'L'],
    ['E', 'I', 'T', 'E'], 
    ['I', 'O', 'N', 'S'],
    ['F', 'P', 'E', 'I']
]

print('Boggle board:')
for i, row in enumerate(boggle_board):
    print(f'Row {i}: {" ".join(row)}')

print(f'\nBoard dimensions: {len(boggle_board)}x{len(boggle_board[0])}')

# Verify board structure
total_letters = sum(len(row) for row in boggle_board)
print(f'Total letters on board: {total_letters}')

# Count letter frequency
letter_count = defaultdict(int)
for row in boggle_board:
    for letter in row:
        letter_count[letter] += 1

print(f'Letter frequency: {dict(letter_count)}')

print('\n=== STEP 4: DEFINING HELPER FUNCTIONS ===')

# Define helper functions at global scope to fix the scope issue
def get_neighbors(row, col, rows, cols):
    """Get all adjacent cells (including diagonal) for a given position"""
    neighbors = []
    # Check all 8 directions: up, down, left, right, and 4 diagonals
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # up-left, up, up-right
        (0, -1),           (0, 1),   # left, right
        (1, -1),  (1, 0),  (1, 1)    # down-left, down, down-right
    ]
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    
    return neighbors

def find_words_from_position(board, dictionary, start_row, start_col, visited, current_word, found_words):
    """Recursively find all valid words starting from a given position"""
    rows, cols = len(board), len(board[0])
    
    # Add current letter to the word
    current_word += board[start_row][start_col].lower()
    
    # Mark current position as visited
    visited.add((start_row, start_col))
    
    # Check if current word is valid and has reasonable length (3+ letters)
    if len(current_word) >= 3 and current_word in dictionary:
        found_words.add(current_word)
        print(f'Found valid word: "{current_word}" (length: {len(current_word)})')
    
    # Continue searching if word length is reasonable (prevent excessive recursion)
    if len(current_word) < 15:  # Reasonable max word length
        # Get all adjacent neighbors
        neighbors = get_neighbors(start_row, start_col, rows, cols)
        
        for next_row, next_col in neighbors:
            # Only visit unvisited cells
            if (next_row, next_col) not in visited:
                # Create a new copy of visited set for this branch
                new_visited = visited.copy()
                find_words_from_position(board, dictionary, next_row, next_col, new_visited, current_word, found_words)

def solve_boggle(board, dictionary):
    """Solve the Boggle puzzle and return all valid words"""
    found_words = set()
    rows, cols = len(board), len(board[0])
    
    print(f'Starting Boggle solve for {rows}x{cols} board...')
    print(f'Dictionary size: {len(dictionary):,} words')
    
    # Start search from each position on the board
    for row in range(rows):
        for col in range(cols):
            print(f'\nSearching from position ({row},{col}) - letter "{board[row][col]}":')
            visited = set()
            find_words_from_position(board, dictionary, row, col, visited, '', found_words)
    
    return found_words

print('✓ Helper functions defined successfully')

print('\n=== STEP 5: RUNNING BOGGLE SOLVER ===')

if dictionary_words:
    print('Starting Boggle word search...')
    start_time = time.time()
    
    # Solve the Boggle puzzle
    all_found_words = solve_boggle(boggle_board, dictionary_words)
    
    end_time = time.time()
    solve_time = end_time - start_time
    
    print(f'\n=== BOGGLE SOLVE COMPLETE ===')
    print(f'Solve time: {solve_time:.2f} seconds')
    print(f'Total valid words found: {len(all_found_words)}')
    
    if all_found_words:
        # Sort words by length (descending) then alphabetically
        sorted_words = sorted(all_found_words, key=lambda w: (-len(w), w))
        
        print(f'\n=== ALL FOUND WORDS (sorted by length, then alphabetically) ===')
        current_length = None
        for word in sorted_words:
            if len(word) != current_length:
                current_length = len(word)
                print(f'\n--- {current_length}-letter words ---')
            print(f'  {word}')
        
        # Find the longest word(s)
        max_length = max(len(word) for word in all_found_words)
        longest_words = [word for word in all_found_words if len(word) == max_length]
        longest_words.sort()  # Sort alphabetically
        
        print(f'\n=== LONGEST WORD(S) FOUND ===')
        print(f'Maximum word length: {max_length} letters')
        print(f'Number of longest words: {len(longest_words)}')
        print(f'Longest words: {longest_words}')
        
        # Return the alphabetically first longest word
        answer = longest_words[0]
        print(f'\n*** FINAL ANSWER: "{answer}" ***')
        print(f'Length: {len(answer)} letters')
        
        # Save results to file
        results_file = os.path.join(workspace, 'boggle_solver_results.txt')
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write('BOGGLE SOLVER RESULTS\n')
            f.write('=' * 50 + '\n\n')
            f.write('Board:\n')
            for row in boggle_board:
                f.write(' '.join(row) + '\n')
            f.write(f'\nTotal words found: {len(all_found_words)}\n')
            f.write(f'Longest word length: {max_length}\n')
            f.write(f'Longest word (alphabetically first): {answer}\n\n')
            f.write('All words by length:\n')
            f.write('-' * 30 + '\n')
            current_length = None
            for word in sorted_words:
                if len(word) != current_length:
                    current_length = len(word)
                    f.write(f'\n{current_length}-letter words:\n')
                f.write(f'  {word}\n')
        
        print(f'\n✓ Complete results saved to: {results_file}')
        
    else:
        print('No valid words found!')
else:
    print('Error: Dictionary not loaded, cannot solve Boggle puzzle')
```

## Created Time
2025-08-09 05:49:19
