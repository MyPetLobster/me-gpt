import re
import json
import os
from rich import print as rich_print
from rich.console import Console
from rich import box
from rich.table import Table

console = Console()

def main():
    intro_table = Table(box=box.SQUARE_DOUBLE_HEAD, min_width=100)
    intro_table.add_column("Welcome to iMessage Converter", header_style="bold cyan", justify="center")
    intro_table.add_row('''[italic]This program will convert an exported iMessage chat into\nChatGPT prompt format. By default the program will assign the\n'assistant' role to your messages (aka "Me") and the person you\nare talking to will be assigned the 'user' role.[/]''')
    intro_table.add_row(' ')
    intro_table.add_row('[italic]The program will also remove all dates, time stamps, and read receipts.\n[/]')
    intro_table.add_row(' ')
    intro_table.add_row('[italic]The program will then write the JSON format to a file in the directory\n"training/json_messages" and copy the contents of the JSON file into a text file with the same name\n[/]')
    intro_table.add_row('[bold deep_pink4]iMessage Converter - By Cory Suzuki[/]')
    intro_table.add_row(' ')
    intro_table.add_row('[bold chartreuse3] https://github.com/MyPetLobster/me-gpt[/]')

    rich_print("\n")
    rich_print(intro_table)
    rich_print("\n")

    text_file_path = console.input("[bold light_slate_grey]Enter the path to the text file: [/]")
    rich_print("\n")

    with open(text_file_path, 'r') as file:
        text = file.read()

    json_file = convert_text_to_json(text)
    file_name = os.path.basename(text_file_path).split(".")[0]
    write_json_to_file(json_file, file_name)
    copy_json_to_text(json.loads(json_file), file_name)


# Process the message file. Remove timestamps, read-receipts, and set roles
def convert_text_format(text):
    # Replace date and time with an empty string
    date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
    text_cleaned = re.sub(date_time_pattern, '', text)

    # Remove (Read by...)
    text_cleaned = re.sub(r'\(Read by .*?\)', '', text_cleaned)
    
    # Set roles, and use -*-*- to split messages
    text_cleaned = re.sub(r'\bMe\b', '-*-*- assistant', text_cleaned)
    text_cleaned = re.sub(r'\+\d+', '-*-*- user', text_cleaned)

    # Replace double new lines with ''
    text_cleaned = re.sub(r'\n\n', '', text_cleaned)

    # Add space after every period if there isn't one already
    text_cleaned = re.sub(r'(?<!\s)(\.)(?!\s)', r'\1 ', text_cleaned)

    return text_cleaned.strip()


def convert_text_to_json(text):
    # Remove timestamps and read-receipts. Set roles
    text_cleaned = convert_text_format(text)

    # Split on dashing stars to get list of messages
    messages = text_cleaned.split("-*-*- ")

    assistant_role = "assistant"
    user_role = "user"

    json_format = []

    # Determine the role for each message
    current_role = user_role
    for message in messages:
        if message:
            if message.startswith("assistant"):
                current_role = assistant_role
            elif message.startswith("user"):
                current_role = user_role

        # Extract the message content, looking for "Me" or "+1234567890"
        content = re.sub(r'assistant|user', '', message).strip()

        # Add the message to the JSON format, skip if empty
        if content:
            json_format.append({"role": current_role, "content": content})
    

    return json.dumps(json_format, indent=2)


# Write the JSON format to a file in directory called "training/json_messages"
def write_json_to_file(json_file, file_name):
    with open("training/json_messages/" + file_name + ".json", 'w') as file:
        file.write(json_file)

# Copy the contents of the JSON file into a new text file (.txt)
def copy_json_to_text(json_file, file_name):
    with open("training/ready_text/" + file_name +  "_json.txt", 'w') as file:
        file.write('[\n')
        for message in json_file:
            file.write(f'''  {{\n    "role": {message["role"]}\n    "content":{message["content"]} \n  }},\n''')
        file.write(']')

if __name__ == "__main__":
    main()