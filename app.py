from dotenv import load_dotenv
from smartsheet import Smartsheet
from lib import Database, Todo
from datetime import date
from os import environ
from typing import List
load_dotenv()

def print_table(table:List) -> List[List[str]]:
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))

def parse_arg(part:str, field_name:str, optional:bool) -> None:
    parts = part.split(':')
    if parts[0] == field_name:
        return parts[1]
    else:
        if not optional:
            print(f"{field_name} is required")
    return None

def find_matching(db:Database, id:str, table_name:str) -> Todo:
    table = db.find_table(table_name)
    found = next(x for x in Todo.rows(table) if x.id == id)
    return found

def main(table_name:str=None) -> None:
    if table_name is None:
        print("Please configure a table name")
        return

    db = Database(Smartsheet())
    table = db.find_table(table_name)

    command = ""
    while command != "quit":
        commands = str(input("> ")).strip().split(' ')
        command = commands[0]
        match command:
            case "list" | "ls":
                table = db.find_table(table_name)
                l = list(map(lambda todo: [str(todo.id), str(todo.task), str(todo.due_date), str(todo.completed_at)], Todo.rows(table)))
                l.insert(0, ["Id", "Task", "Due_Date", "Completed_At"])
                print_table(l)
            case "exit" | "quit":
                command = "quit"
            case "rm":
                found = find_matching(db, commands[1], table_name)
                found.delete()
            case "finish":
                found = find_matching(db, commands[1], table_name)
                found.finish()
            case "unfinish":
                found = find_matching(db, commands[1], table_name)
                found.unfinish()
            case "create":
                task = None
                due_date = None
                if len(commands) == 3:
                    task = parse_arg(commands[1], "task", True)
                    if task is None:
                        task = parse_arg(commands[2], "task", True)
                    if task is None:
                        print("task is required")

                    due_date = parse_arg(commands[1], "due_date", True)
                    if due_date is None:
                        due_date = parse_arg(commands[2], "due_date", True)
                    # turning this off in case we add more args later
                    # if due_date is None:
                        # print("due_date is required")

                elif len(commands) == 2:
                    task = parse_arg(commands[1], "task", False)
                else:
                    print("You need task and optionally due_date")

                if task is not None:
                    todo = Todo(table, task, due_date)
                    todo.save()
            case _:
                help = ("Commands\n"
                    "\tls - list all todos\n"
                    "\tcreate task:foo due_date:2023-12-12 - create todo")
                print(help)

    # print(f"The sheets are {', '.join(db.list_tables())}")
    # print(f"The sheet {table.name} has {table.row_count} rows")
    # print(table.title_to_id)

    # delete
    # todo = Todo(table)
    # todo.id = "8538751117332356"
    # todo.delete()

if __name__ == "__main__":
    main(environ.get("SHEET_NAME", None))
