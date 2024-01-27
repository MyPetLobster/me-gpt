import re
import json

def main():
    text_file_path = input("Enter the path to the text file: ")
    json_file = convert_text_to_json(text_file_path)
    file_name = text_file_path.split("/")[-1].split(".")[0]
    write_json_to_file(json_file, file_name)

def convert_text_format(text):
    # Replace date and time with an empty string
    date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
    text_cleaned = re.sub(date_time_pattern, '', text)

    # Remove (Read by...)
    text_cleaned = re.sub(r'\(Read by .*?\)', '', text_cleaned)
    
    # Replace "Me" with "assistant"
    text_cleaned = re.sub(r'\bMe\b', 'assistant', text_cleaned)

    # Replace phone numbers with "user"
    text_cleaned = re.sub(r'\+\d+', 'user', text_cleaned)

    # Replace every double new line with three asterisks to separate messages
    text_cleaned = re.sub(r'\n\n', '***', text_cleaned)

    return text_cleaned.strip()


def convert_text_to_json(text_file):
    # Read text file 
    with open(text_file, 'r') as file:
        text = file.read()

    # Remove timestamps and read by line and replace "Me" and phone numbers
    text_cleaned = convert_text_format(text)
    
    print("\n\n\n")
    print(text_cleaned)
    print("\n\n\n")

    # Split cleaned text into messages by "***"
    messages = text_cleaned.split("***")
   

    print("\n\n\n")
    print(messages)
    print("\n\n\n")

    # Define roles
    assistant_role = "assistant"
    user_role = "user"

    # Initialize the JSON format
    json_format = []

    # Determine the role for each message
    current_role = user_role
    for message in messages:
        if message.startswith("assistant") or message.startswith(" \nassistant"):
            current_role = assistant_role
        elif message.startswith("user") or message.startswith(" \nuser"):
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

if __name__ == "__main__":
    main()