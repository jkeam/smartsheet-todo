# Smartsheets Todo App

Very simple todo app using Smartsheets as the persistent store.
Sheet will automatically be created for you if it does not exist.

## Prerequisite

1. Python 3.11+
2. `.env` file like the following,
note that `SHEET_NAME` must be unique in the folder with `FOLDER_ID`
    ```env
    SMARTSHEET_ACCESS_TOKEN=samplesamplesample
    SHEET_NAME=Todo
    FOLDER_ID=3734419270854532
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
