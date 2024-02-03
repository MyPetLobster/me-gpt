import re
import json
import os

def main():
    text_file_path = input("Enter the path to the text file: ")
    json_file = convert_text_to_json(text_file_path)
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


def convert_text_to_json(text_file):
    with open(text_file, 'r') as file:
        text = file.read()

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
    with open("training/ready_text/" + file_name + "_user_only.txt", 'w') as file:
        for message in json_file:
            file.write(f'{message["role"]}: {message["content"]}\n')

if __name__ == "__main__":
    main()