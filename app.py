from dotenv import load_dotenv
from smartsheet import Smartsheet
from lib import Database, Todo
from datetime import date
load_dotenv()

def main() -> None:
    db = Database(Smartsheet())
    print(f"The sheets are {', '.join(db.list_tables())}")

    table = db.find_table("Todo")
    print(f"The sheet {table.name} has {table.row_count} rows")
    print(table.title_to_id)
    # print(list(map(lambda x: x.id, table.rows)))

    # create
    # todo = Todo(table, "test1", date(2023, 11, 10))
    # todo = Todo(table, "test")
    # todo.save()

    # delete
    # todo = Todo(table)
    # todo.id = "8538751117332356"
    # todo.delete()

if __name__ == "__main__":
    main()
