import tiktoken
import re


def main():
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    with open("training/ready_text/nick_curated_01.txt", 'r') as file:
        text = file.read()
    
    text_cleaned = convert_text_format(text)
    token_count = len(encoding.encode(text_cleaned))
    
    print(f"Token count: {token_count}")


def convert_text_format(text):
    # Replace date and time with an empty string
    date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
    text_cleaned = re.sub(date_time_pattern, '', text)

    # Remove (Read by...)
    text_cleaned = re.sub(r'\(Read by .*?\)', '', text_cleaned)
    
    # Set roles, and use -*-*- to split messages
    text_cleaned = re.sub(r'\bMe\b', '', text_cleaned)
    text_cleaned = re.sub(r'\+\d+', '', text_cleaned)

    # Replace new lines with ''
    text_cleaned = re.sub(r'\n\n', '', text_cleaned)
    text_cleaned = re.sub(r'\n', ' ', text_cleaned)

    # Add space after every period if there isn't one already
    text_cleaned = re.sub(r'(?<!\s)(\.)(?!\s)', r'\1 ', text_cleaned)

    return text_cleaned.strip()


if __name__ == "__main__":
    main()