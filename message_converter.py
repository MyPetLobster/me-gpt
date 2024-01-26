import re
import json

def main():
    text_file_path = "training/raw_messages/raw_test_100ln.txt"
    json_file = convert_text_to_json(text_file_path)
    print(json_file)



def convert_text_format(text):

    date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
    # Replace date and time with an empty string
    text_cleaned = re.sub(date_time_pattern, '', text)

    # Remove (Read by...)
    text_cleaned = re.sub(r'\(Read by .*?\)', '', text_cleaned)
    
    # Replace "Me" with "assistant"
    text_cleaned = re.sub(r'\bMe\b', 'assistant', text_cleaned)

    # Replace phone numbers with "user"
    text_cleaned = re.sub(r'\+\d+', 'user', text_cleaned)

    # Separate conversations with three asterisks
    text_formatted = re.sub(r'(?<=\n)\n+', '\n\n', text_cleaned)

    return text_formatted.strip()


def convert_text_to_json(text_file):
    # Read text file 
    with open(text_file, 'r') as file:
        text = file.read()

    # Remove timestamps and read by line and replace "Me" and phone numbers
    text_cleaned = convert_text_format(text)

    print(text_cleaned)
    print("\n\n\n")
    
    # Split cleaned text into messages
    messages = re.split(r'\n\n', text_cleaned.strip())

    print(messages)

    # Define roles
    assistant_role = "assistant"
    user_role = "user"

    # Initialize the JSON format
    json_format = []

    # Determine the role for each message
    current_role = user_role
    for message in messages:
        if message.startswith("assistant"):
            current_role = assistant_role
        elif message.startswith("user"):
            current_role = user_role

        # Extract the message content, looking for "Me" or "+1234567890"
        content = re.sub(r'Me|(\+\d+)', '', message).strip()

        # Add the message to the JSON format, skip if empty
        if content:
            json_format.append({"role": current_role, "content": content})

    return json.dumps(json_format, indent=2)


if __name__ == "__main__":
    main()