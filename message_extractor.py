'''
Application to extract the user messages from ChatGPT chat history

Input format (copy pasted from exported 'chat.html'):

User
You are an expert with regular expressions, with a specific expertise in Python Regex. Can you help me figure out a problem with my code?

Take your time reading all my messages.
ChatGPT
Of course! I'd be happy to help you with your Python regular expression issue. Please provide me with the details of the problem you're encountering, along with your code snippet if possible.
User
I'm working on some Python code to convert Markdown to HTML. Here is the regular expression that I am using to convert headers (# to <h1>). Here is the function that I have now -- 
ChatGPT
I see. Could you please provide me with the code snippet you're using for the conversion? It would help me understand the issue better.

Expected output format:

Cory: You are an expert with regular expressions, with a specific expertise in Python Regex. Can you help me figure out a problem with my code? 

Take your time reading all my messages.
Cory: I'm working....
'''

import re

def main():
    print("Input file must be in 'training/raw_messages/' directory.")
    print("Output file will be written to 'training/ready_text/<input_file>_user_only.txt'")
    input_file = input("Enter the name of the file to extract user messages from: ")
    
    with open(f"training/raw_messages/{input_file}", 'r') as file:
        chat = file.read()

    # Use RE to match all text between 'User' and 'ChatGPT'
    user_messages = re.findall(r'User\n(.*?\n)ChatGPT', chat, re.DOTALL)

    with open(f"training/ready_text/{input_file.split(".")[0]}_user_only.txt", 'w') as file:
        for message in user_messages:
            file.write(f'Cory: {message}\n')

if __name__ == "__main__":
    main()