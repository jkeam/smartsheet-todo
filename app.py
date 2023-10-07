from dotenv import load_dotenv
from smartsheet import Smartsheet
from lib import Database, Todo
from os import environ
from datetime import datetime
from typing import List
load_dotenv()

def print_table(table:List) -> None:
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))

def parse_args(line:str) -> dict[str, str]:
    args = {}
    parts = line
    for _ in range(len(line.split(':')) - 1):
        parts = parts.split(':')
        key = parts[0]
        rest = ":".join(parts[1:])
        if rest[0] == "'":
            separator = "'"
            rest = "".join(rest[1:])
        elif rest[0] == '"':
            separator = '"'
            rest = "".join(rest[1:])
        else:
            separator = " "
        quotes = rest.split(separator)
        args[key.strip()] = quotes[0].strip()
        parts = separator.join(quotes[1:])
    return args

def find_matching(db:Database, id:str, table_name:str) -> Todo:
    return Todo.find_by_id(db.find_table(table_name), id)

def main(table_name:str|None=None) -> None:
    if table_name is None:
        print("Please configure a table name")
        return

    db = Database(Smartsheet())
    table = db.find_table(table_name)

    command = ""
    history:List[str] = []
    save_command = True
    while command != "quit":
        commands = str(input("> ")).strip().split(" ")
        command = commands[0]
        match command:
            case "list" | "ls":
                rows = Todo.rows(db.find_table(table_name))
                todos = list(map(lambda todo: [str(todo.id), str(todo.task), str(todo.due_date), str(todo.completed_at)], rows))
                todos.insert(0, ["Id", "Task", "Due_Date", "Completed_At"])
                print_table(todos)
            case "exit" | "quit":
                command = "quit"
            case "rm":
                found = find_matching(db, commands[1], table_name)
                if found is not None:
                    found.delete()
                else:
                    print(f"Unable to find with id {commands[1]}")
            case "finish":
                found = find_matching(db, commands[1], table_name)
                if found is not None:
                    found.finish()
                else:
                    print(f"Unable to find with id {commands[1]}")
            case "unfinish":
                found = find_matching(db, commands[1], table_name)
                if found is not None:
                    found.unfinish()
                else:
                    print(f"Unable to find with id {commands[1]}")
            case "set":
                id = commands[1]
                found = find_matching(db, id, table_name)
                args = parse_args(" ".join(commands[2:]))
                due_date = args.get("due_date", None)
                if due_date is None:
                    due_date = args.get("date", None)
                task = args.get("task", None)
                if found is None:
                    print(f"Unable to find with id {id}")
                    continue

                if due_date is not None:
                    found.update_due_date_as_str(due_date)
                if task is not None:
                    found.update_task(task)
            case "create":
                args = parse_args(" ".join(commands[1:]))
                due_date = args.get("due_date", None)
                if due_date is None:
                    due_date = args.get("date", None)
                if due_date is not None:
                    due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                task = args.get("task", None)
                if task is not None:
                    todo = Todo(table, task, due_date)
                    todo.save()
                else:
                    print("You need task and optionally due_date")
            case "history":
                save_command = False
                for x in history:
                    print(x)
            case "clear" | "reset" | "clear_history" | "reset_history":
                save_command = False
                history.clear()
            case _:
                help = ('''Commands:
    ls - list all todos
    create task:foo due_date:2023-12-12 - create todo
    set <id> due_date:2023-12-12 - set due date
    rm <id> - delete todo
    finish <id> - mark as completed
    unfinish <id> - mark as uncompleted
    history - see ephemeral command history
    clear - clear ephemeral command history''')
                print(help)
        if save_command:
            history.append(commands)
        else:
            save_command = True

if __name__ == "__main__":
    main(environ.get("SHEET_NAME", None))
