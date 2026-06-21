import json
import re
import random

# Load the raw text copied from your PDF
with open('vocab_data.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Regex pattern to match the structure in your PDF
# Example: Abase To humiliate Synonyms Degrade... Antonyms Regard...
pattern = re.compile(r'([A-Z][a-z]+)\s+(.*?)\s+Synonyms\s+(.*?)\s+Antonyms\s+(.*?)(?=\n[A-Z][a-z]+\s|$)', re.DOTALL)

matches = pattern.findall(text)

synonym_questions = []
antonym_questions = []

# Extract all possible options to act as wrong answers (distractors)
all_synonyms = []
all_antonyms = []

for match in matches:
    word = match[0].strip()
    syns = [s.strip() for s in match[2].split(',')]
    ants = [a.strip() for a in match[3].split(',')]
    
    if syns and syns[0]: all_synonyms.extend(syns)
    if ants and ants[0]: all_antonyms.extend(ants)

# Remove duplicates
all_synonyms = list(set(all_synonyms))
all_antonyms = list(set(all_antonyms))

# Generate Questions
for match in matches:
    word = match[0].strip()
    syns = [s.strip() for s in match[2].split(',')]
    ants = [a.strip() for a in match[3].split(',')]
    
    # --- SYNONYM QUESTION GENERATOR ---
    if syns and syns[0]:
        correct_answer = syns[0].replace('\n', '')
        # Pick 3 random wrong answers
        wrong_answers = random.sample([s for s in all_synonyms if s not in syns], 3)
        options = wrong_answers + [correct_answer]
        random.shuffle(options)
        
        synonym_questions.append({
            "question": f"What is the synonym of '{word}'?",
            "options": [opt.replace('\n', '') for opt in options],
            "answer": correct_answer
        })

    # --- ANTONYM QUESTION GENERATOR ---
    if ants and ants[0]:
        correct_answer = ants[0].replace('\n', '')
        # Pick 3 random wrong answers
        wrong_answers = random.sample([a for a in all_antonyms if a not in ants], 3)
        options = wrong_answers + [correct_answer]
        random.shuffle(options)
        
        antonym_questions.append({
            "question": f"What is the antonym of '{word}'?",
            "options": [opt.replace('\n', '') for opt in options],
            "answer": correct_answer
        })

# Format into the JSON structure your HTML expects
final_database = {
    "synonyms": synonym_questions,
    "antonyms": antonym_questions,
    "grammar": [], # Add your grammar questions manually later
    "jumbles": [], # Add your jumble questions manually later
    "comprehension": [] # Add your RC passages manually later
}

# Save to a JSON file
with open('eng_vocab.json', 'w', encoding='utf-8') as outfile:
    json.dump(final_database, outfile, indent=4)

print(f"Successfully generated {len(synonym_questions)} Synonym questions and {len(antonym_questions)} Antonym questions!")
print("Check the 'eng_vocab.json' file in your folder.")
