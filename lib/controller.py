from . import Database, Todo, Util, TodoFilterType
from typing import List
from operator import methodcaller

class Controller:

    def __init__(self, db:Database, table_name:str, folder_id:str|None=None) -> None:
        self.db = db
        self.table_name = table_name
        self.folder_id = folder_id
        # if folder is set and table does not exist, create sheet
        table = self.db.find_table(self.table_name)
        if self.folder_id and table is None:
            print("Creating table/sheet in that folder...")
            Todo.create_table(self.db.smart, self.table_name, self.folder_id)

    def list(self, commands:List[str]) -> None:
        if (commands[0] == "la") or (len(commands) > 1 and commands[1] == "-a"):
            todo_filter = TodoFilterType.ALL
        elif (commands[0] == "week"):
            todo_filter = TodoFilterType.WEEK
        else:
            todo_filter = TodoFilterType.UNFINISHED

        todos = Todo.create_print_table(self.db.find_table(self.table_name), todo_filter)
        Util.print_table(todos)

    def see(self, id:str) -> None:
        found = self._find_matching(self.db, id, self.table_name)
        if found is not None:
            print(found.pretty_str())
        else:
            print(f"Unable to find with id {id}")

    def run_generic_command(self, command:str, id:str) -> None:
        found = self._find_matching(self.db, id, self.table_name)
        if found is not None:
            if command == "rm" or command == "remove":
                command = "delete"
            methodcaller(command)(found)
        else:
            print(f"Unable to find with id {id}")

    def set_attribute(self, commands:List[str]) -> None:
        id = commands[1]
        found = self._find_matching(self.db, id, self.table_name)
        if found is None:
            print(f"Unable to find with id {id}")
            return

        args = Util.parse_args(" ".join(commands[2:]))
        due_date = args.get("due_date", None)
        if due_date is None:
            due_date = args.get("date", None)
        task = args.get("task", None)
        notes = args.get("notes", None)
        status = args.get("status", None)
        if due_date is not None:
            found.update_due_date_as_str(due_date)
        if task is not None:
            found.update_task(task)
        if notes is not None:
            found.update_notes(notes)
        if status is not None:
            found.update_status(status)

    def create(self, commands:List[str]) -> None:
        args = Util.parse_args(" ".join(commands[1:]))
        notes = args.get("notes", None)
        task = args.get("task", None)
        due_date = args.get("due_date", None)
        if due_date is None:
            due_date = args.get("date", None)
        if due_date is not None:
            due_date = Util.parse_date(due_date)
        if task is not None:
            todo = Todo(self.db.find_table(self.table_name), task, due_date, notes)
            todo.save()
        else:
            print("You need task and optionally due_date")

    def help(self) -> None:
        help = ('''Commands:
        help - see this help
        ls - list uncompleted todos
        la - list all (uncompleted and completed) todos
        week - list uncompleted todos that are due this week
        see <id> - see the todo
        create task:foo due_date:2023-12-12 notes:"Some notes" - create todo
        set <id> due_date:2023-12-12 - set due date
        set <id> task:"Do something" - set task
        set <id> notes:"Some notes" - set notes
        set <id> status:"Backlog" - valid vales are ["Backlog", "Active Sprint", "In Progress", "Done", "OBE"]
        rm <id> - delete todo
        finish <id> - mark as completed
        unfinish <id> - mark as uncompleted
        history - see ephemeral command history
        clear - clear ephemeral command history''')
        print(help)
        
    # Helpers

    def _find_matching(self, db:Database, id:str, table_name:str) -> Todo|None:
        return Todo.find_by_id(db.find_table(table_name), id)
