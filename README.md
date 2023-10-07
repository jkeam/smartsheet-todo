# Smartsheets Todo App

Very simple todo app using Smartsheets as the persistent store.

## Prerequisite

1. Python 3.11+

## Setup

1. `pip install -r ./requirements.txt`
2. `python ./app.py`

## Usage

```shell
ls - list all todos
see <id> - see the todo
create task:foo due_date:2023-12-12 - create todo
set <id> due_date:2023-12-12 - set due date
set <id> task:"Something something" - update task
set <id> notes:"Something something" - update notes
rm <id> - delete todo
finish <id> - mark as completed
unfinish <id> - mark as uncompleted
history - see ephemeral command history
clear - clear ephemeral command history
```
