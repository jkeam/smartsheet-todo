# Smartsheets Todo App

Very simple todo app using Smartsheets as the persistent store.

## Prerequisite

1. Python 3.11+
2. Smartsheet with the right [schema](./lib/todo.py)
3. `.env` file like the following:
    ```env
    SMARTSHEET_ACCESS_TOKEN=samplesamplesample
    SHEET_NAME=Todo
    ```

## Setup

1. `pip install -r ./requirements.txt`
2. `python ./app.py`

## Usage

```shell
help - see this help
ls - list uncompleted todos
la - list all (uncompleted and completed) todos
see <id> - see the todo
create task:foo due_date:2023-12-12 notes:"Some notes" - create todo
set <id> due_date:2023-12-12 - set due date
set <id> task:"Do something" - update task
set <id> notes:"Some notes" - update notes
rm <id> - delete todo
finish <id> - mark as completed
unfinish <id> - mark as uncompleted
history - see ephemeral command history
clear - clear ephemeral command history
```
