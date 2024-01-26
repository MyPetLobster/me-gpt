import re
import json

def convert_text_to_json(text_file):
    # Read text file 
    with open(text_file, 'r') as file:
        text = file.read()

    # Remove timestamps and read by line
    text_cleaned = re.sub(r'\w+ \d{2}, \d{4} \d{2}:\d{2}:\d{2} (AM|PM)|\(Read by .*?\)', '', text)

    # Split cleaned text into messages
    messages = re.split(r'\n\n', text_cleaned.strip())

    # Define roles
    assistant_role = "assistant"
    user_role = "user"

    # Initialize the JSON format
    