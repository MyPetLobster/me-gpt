import tiktoken
from message_converter import convert_text_to_json
from rich import print as rich_print
from rich.console import Console
from rich import box
from rich.table import Table


console = Console()


def main():
    intro_table = Table(box=box.SQUARE_DOUBLE_HEAD, min_width=100)
    intro_table.add_column("Welcome to Token Counter", header_style="bold cyan", justify="center")
    intro_table.add_row('''[italic]This program will count the number of tokens in a given text file.\nYou just have to provide the file path and the encoding model,\nand it will return the token count.[/]''')
    intro_table.add_row(' ')
    intro_table.add_row('If the file is in iMessage chat format, the program will\noptionally remove all dates, time stamps, and read receipts.\n')
    intro_table.add_row('[bold deep_pink4]Token Counter - By Cory Suzuki[/]')
    intro_table.add_row(' ')
    intro_table.add_row('[bold chartreuse3] https://github.com/MyPetLobster/me-gpt[/]')

    rich_print("\n")
    rich_print(intro_table)
    rich_print("\n")

    rich_print("[light_slate_grey]Please note that this program is designed to work with text files only.[/]\n")
    rich_print("[bold grey63]Encoding Models:[/] [rosy_brown]gpt-4, gpt-3.5-turbo, davinci-002, davinci-003, text-embedding-ada-002[/]\n")

    file_path = console.input("[bold green]Enter the name of the file to count tokens for: [/]")
    encoding_model = console.input("[bold deep_pink4]Enter the encoding model to use: [/]")
    iMessage_format = console.input("[bold cyan]Is the file in iMessage format? (y/n): [/]")
    rich_print("\n")

    if iMessage_format.lower() == 'y' or iMessage_format.lower() == 'yes':
        iMessage_format = True
    else:
        iMessage_format = False

    encoding = tiktoken.encoding_for_model(f"{encoding_model}")

    with open(f"{file_path}", 'r') as file:
        text = file.read()
    
    if iMessage_format:
        text = convert_text_to_json(text)
    
    token_count = len(encoding.encode(text))
    
    rich_print(f"[bold deep_pink3]Token count:[/] [bold light_cyan1]{token_count}[/]")
    rich_print("\n")


if __name__ == "__main__":
    main()



