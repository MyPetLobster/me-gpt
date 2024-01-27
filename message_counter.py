import re

## Accepts a text file in the format of iMessage database files
## I extracted iMessage data using imessage-exporter 

def main():
    file_name = input("Enter the name of the file: ")
    with open(file_name, "r") as text_file:
        file_contents = text_file.read()

    total_messages = count_messages(file_contents)
    messages_sent = count_messages_sent(file_contents)
    messages_received = total_messages - messages_sent

    print(f"Total messages: {total_messages}")
    print(f"Messages sent: {messages_sent}")
    print(f"Messages received: {messages_received}")

    count_total_words(file_contents)

def count_messages(file_contents):
    date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
    message_count = len(re.findall(date_time_pattern, file_contents))
    return message_count


def count_messages_sent(file_contents):
    sent_message_pattern = re.compile(r'^Me$', re.MULTILINE)
    message_count = len(re.findall(sent_message_pattern, file_contents))
    return message_count


def count_total_words(file_contents):
    # Replace date and time with an empty string
    date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
    text_cleaned = re.sub(date_time_pattern, '', file_contents)
    
    # Remove (Read by...)
    text_cleaned = re.sub(r'\(Read by .*?\)', '', text_cleaned)
    
    # Remove "Me"
    text_cleaned = re.sub(r'\bMe\b', '-*-*- sent', text_cleaned)

    # Remove phone numbers
    text_cleaned = re.sub(r'\+\d+', '-*-*- received', text_cleaned)

    # Split at double new lines for list of all messages
    messages = [message.strip() for message in text_cleaned.split("-*-*-") if message.strip()]

    sent_messages = []
    received_messages = []

    sent_words = 0
    received_words = 0

    for message in messages:
        if message.startswith("sent"):
            sent_messages.append(message)
        elif message.startswith("received"):
            received_messages.append(message)

    for message in sent_messages:
        sent_words += len(message.split(" "))
    for message in received_messages:
        received_words += len(message.split(" "))

    total_words = sent_words + received_words

    print("Word Count")
    print(f"Total words: {total_words}")
    print(f"Words sent: {sent_words}")
    print(f"Words received: {received_words}")


if __name__ == "__main__":
    main()











# def total_words_test(file_contents):
#     # Replace date and time with an empty string
#     date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
#     text_cleaned = re.sub(date_time_pattern, '', file_contents)
    
#     # Remove (Read by...)
#     text_cleaned = re.sub(r'\(Read by .*?\)', '', text_cleaned)
    
#     # Remove sender names
#     text_cleaned = re.sub(r'\bMe\b', '', text_cleaned)  # Assuming sender's name is "Me"

#     # Remove phone numbers
#     text_cleaned = re.sub(r'\+\d+', '', text_cleaned)
    
#     # Split the content into words using whitespace as a delimiter
#     words = text_cleaned.split()

#     # Count the number of words
#     total_words = len(words)

#     return total_words


# def count_total_words_filtered(file_contents):
#     # Replace date and time with an empty string
#     date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
#     text_cleaned = re.sub(date_time_pattern, '', file_contents)
    
#     # Remove (Read by...)
#     text_cleaned = re.sub(r'\(Read by .*?\)', '', text_cleaned)
    
#     # Remove sender names
#     text_cleaned = re.sub(r'\bMe\b', '', text_cleaned)  # Assuming sender's name is "Me"

#     # Remove phone numbers
#     text_cleaned = re.sub(r'\+\d+', '', text_cleaned)
    
#     # Split the content into messages based on the pattern (date/time or sender name)
#     messages = re.split(r'\n(?=(?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b|\bMe\b))', text_cleaned)

#     sent_messages = []
#     received_messages = []

#     for message in messages:
#         if message.startswith("sent") or message.startswith(" \nsent"):
#             sent_messages.append(message)
#         elif message.startswith("received") or message.startswith(" \nreceived"):
#             received_messages.append(message)

#     sent_words = sum(len(message.split()) for message in sent_messages)
#     received_words = sum(len(message.split()) for message in received_messages)

#     total_words = sent_words + received_words

#     print(f"Total words: {total_words}")
#     print(f"Words sent: {sent_words}")
#     print(f"Words received: {received_words}")
