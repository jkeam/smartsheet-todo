from dotenv import load_dotenv
from smartsheet import Smartsheet
from lib import Database, Todo, Util, Controller
from os import environ
from datetime import datetime
from typing import List
from operator import methodcaller
# https://stackoverflow.com/questions/8469122/maximum-characters-that-can-be-stuffed-into-raw-input-in-python
import readline  # raises the input buffer
load_dotenv()

def main(table_name:str|None=None, folder_id:str|None=None) -> None:
    try:
        if table_name is None:
            print("Please configure a table name")
            return

        controller = Controller(Database(Smartsheet()), table_name, folder_id)
        history:List[str] = []
        save_command = True
        command = ""
        while command != "quit":
            commands = str(input("> ")).strip().split(" ")
            command = commands[0]
            match command:
                case "list" | "ls" | "la":
                    controller.list(commands)
                case "see":
                    controller.see(commands[1])
                case "rm" | "finish" | "unfinish" | "delete" | "remove":
                    controller.run_generic_command(command, commands[1])
                case "set":
                    controller.set_attribute(commands)
                case "create":
                    controller.create(commands)
                case "history":
                    save_command = False
                    {print(x) for x in history}
                case "clear" | "reset" | "clear_history" | "reset_history":
                    save_command = False
                    history.clear()
                case "exit" | "quit":
                    save_command = False
                    command = "quit"
                case _:
                    controller.help()
            if save_command:
                history.append(" ".join(commands))
            else:
                save_command = True
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main(environ.get("SHEET_NAME", None), environ.get("FOLDER_ID", None))
