from dotenv import load_dotenv
from smartsheet import Smartsheet
from lib import Database, Todo, Util
from os import environ
from datetime import datetime
from typing import List
from operator import methodcaller
load_dotenv()

def find_matching(db:Database, id:str, table_name:str) -> Todo|None:
    return Todo.find_by_id(db.find_table(table_name), id)

def main(table_name:str|None=None) -> None:
    if table_name is None:
        print("Please configure a table name")
        return

    db = Database(Smartsheet())
    command = ""
    history:List[str] = []
    save_command = True
    while command != "quit":
        commands = str(input("> ")).strip().split(" ")
        command = commands[0]
        match command:
            case "list" | "ls" | "la":
                show_all = (command == "la") or (len(commands) > 1 and commands[1] == "-a")
                todos = Todo.create_print_table(db.find_table(table_name), show_all)
                Util.print_table(todos)
            case "see":
                found = find_matching(db, commands[1], table_name)
                if found is not None:
                    print(found.pretty_str())
                else:
                    print(f"Unable to find with id {commands[1]}")
            case "rm" | "finish" | "unfinish" | "delete" | "remove":
                found = find_matching(db, commands[1], table_name)
                if found is not None:
                    if command == "rm" or command == "remove":
                        command = "delete"
                    methodcaller(command)(found)
                else:
                    print(f"Unable to find with id {commands[1]}")
            case "set":
                id = commands[1]
                found = find_matching(db, id, table_name)
                if found is None:
                    print(f"Unable to find with id {id}")
                    continue

                args = Util.parse_args(" ".join(commands[2:]))
                due_date = args.get("due_date", None)
                if due_date is None:
                    due_date = args.get("date", None)
                task = args.get("task", None)
                notes = args.get("notes", None)
                if due_date is not None:
                    found.update_due_date_as_str(due_date)
                if task is not None:
                    found.update_task(task)
                if notes is not None:
                    found.update_notes(notes)
            case "create":
                args = Util.parse_args(" ".join(commands[1:]))
                due_date = args.get("due_date", None)
                if due_date is None:
                    due_date = args.get("date", None)
                if due_date is not None:
                    due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                task = args.get("task", None)
                if task is not None:
                    todo = Todo(db.find_table(table_name), task, due_date)
                    todo.save()
                else:
                    print("You need task and optionally due_date")
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
                help = ('''Commands:
    help - see this help
    ls - list completed todos
    la - list all todos
    see <id> - see the todo
    create task:foo due_date:2023-12-12 - create todo
    set <id> due_date:2023-12-12 - set due date
    set <id> task:"some task" - set task
    set <id> notes:"some notes" - set notes
    rm <id> - delete todo
    finish <id> - mark as completed
    unfinish <id> - mark as uncompleted
    history - see ephemeral command history
    clear - clear ephemeral command history''')
                print(help)
        if save_command:
            history.append(" ".join(commands))
        else:
            save_command = True

if __name__ == "__main__":
    main(environ.get("SHEET_NAME", None))
