import re

def main():
    file_name = input("Enter the name of the file: ")
    text_file = open(file_name, "r")
    total_messages = count_messages(text_file)

    messages_sent = count_messages_sent(text_file)
    messages_received = total_messages - messages_sent

    text_file.close()

    print(f"Total messages: {total_messages}")
    print(f"Messages sent: {messages_sent}")
    print(f"Messages received: {messages_received}")

def count_messages(text_file):
    date_time_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[APMapm]{2}\b')
    message_count = 0
    for line in text_file:
        if date_time_pattern.search(line):
            message_count += 1
    return message_count

def count_messages_sent(text_file):
    file_contents = text_file.read()
    sent_message_pattern = re.compile(r'^Me$', re.MULTILINE)
    message_count = len(re.findall(sent_message_pattern, file_contents))
    return message_count



if __name__ == "__main__":
    main()  