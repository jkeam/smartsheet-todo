from smartsheet import Smartsheet
from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Self
from . import Table, Util

class TodoStatusType(Enum):
  BACKLOG = "Backlog"
  ACTIVE_SPRINT = "Active Sprint"
  IN_PROGRESS = "In Progress"
  DONE = "Done"
  OBE = "OBE"

class TodoFilterType(Enum):
  ALL = "ALL"
  WEEK = "WEEK"
  UNFINISHED = "UNFINISHED"

class TodoFieldNames(Enum):
  """ Todo Schema """
  TASK_NAME = "TaskName"
  TASK_NAME_TYPE = "TEXT_NUMBER"
  DUE_DATE = "DueDate"
  DUE_DATE_TYPE = "DATE"
  ID = "Id"
  ID_TYPE = "AUTO_NUMBER"
  COMPLETED_AT = "CompletedAt"
  COMPLETED_AT_TYPE = "DATE"
  NOTES = "Notes"
  NOTES_TYPE = "TEXT_NUMBER"
  STATUS = "Status"
  STATUS_TYPE = "PICKLIST"

class Todo:
  """ Todo """

  def __init__(self, table:Table, task:str|None=None, due_date:date|None=None, notes:str|None=None) -> None:
    self.id = None
    self.row = None
    self.task_object = None
    self.due_date_object = None
    self.completed_at_object = None
    self.id_object = None
    self.notes_object = None
    self.status_object = None
    self.table:Table = table
    self.task:str|None = task
    self.due_date:date|None = due_date
    self.notes:str|None = notes
    self.status:str = TodoStatusType.BACKLOG.value

  def __str__(self) -> str:
    return f"Todo: {{ id: {self.id}, task: {self.task}, due_date: {self.due_date}, completed_at: {self.completed_at}, notes: {self.notes} }}"

  def pretty_str(self) -> str:
    notes = self.notes
    if not notes:
      notes = ""
    return (f'''Todo
    id: {self.id}
    task: {self.task}
    due_date: {self.due_date}
    completed_at: {self.completed_at}
    status: {self.status}
    notes: {notes.replace(r'\n', '\n')}''')

  @property
  def id_object(self):
    return self._id_object

  @id_object.setter
  def id_object(self, value):
    if value is not None:
      self.id = value.display_value
    self._id_object = value

  @property
  def task_object(self):
    return self._task_object

  @task_object.setter
  def task_object(self, value):
    if value is not None:
      self.task = value.display_value
    self._task_object = value

  @property
  def due_date_object(self):
    return self._due_date_object

  @due_date_object.setter
  def due_date_object(self, value):
    self._due_date_object = value
    if value is not None and value.value is not None and value.value != "":
      self.due_date = Util.parse_date(value.value)
    else:
      self.due_date = None

  @property
  def completed_at_object(self):
    return self._completed_at_object

  @completed_at_object.setter
  def completed_at_object(self, value):
    self._completed_at_object = value
    if value is not None and value.value is not None and value.value != "":
      self.completed_at = Util.parse_date(value.value)
    else:
      self.completed_at = None

  @property
  def notes_object(self):
      return self._notes_object

  @notes_object.setter
  def notes_object(self, value):
    if value is not None:
      self.notes = value.display_value
    self._notes_object = value

  @property
  def status_object(self):
      return self._status_object

  @status_object.setter
  def status_object(self, value):
    if value is not None:
      self.status = value.display_value
    self._status_object = value

  def is_completed(self) -> bool:
    return self.completed_at is not None

  def save(self) -> None:
    """ Save todo """
    data = {
      TodoFieldNames.TASK_NAME.value: self.task
    }
    if self.notes is not None:
      data[TodoFieldNames.NOTES.value] = self.notes
    if self.due_date is not None:
      data[TodoFieldNames.DUE_DATE.value] = Util.date_as_str(self.due_date)
    if self.status is not None:
      data[TodoFieldNames.STATUS.value] = self.status
    self.table.insert_row(data)

  def delete(self) -> None:
    """ Delete todo """
    if self.row is None or self.row.id is None:
      print("Unable to delete, missing row id")
    else:
      self.table.delete_row([self.row.id])

  def finish(self) -> None:
    """ Mark as finished """
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    self.completed_at = datetime.now().date()
    self.table.update_field(self.row.id, TodoFieldNames.COMPLETED_AT.value, self.completed_at)

  def unfinish(self) -> None:
    """ Mark as not finished """
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    self.completed_at = None
    self.table.update_field(self.row.id, TodoFieldNames.COMPLETED_AT.value, self.completed_at)

  def update_due_date_as_str(self, due_date:str) -> None:
    """ Set due date """
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    if due_date is not None and due_date != "":
      self.due_date = Util.parse_date(due_date)
    else:
      self.due_date = None
    self.table.update_field(self.row.id, TodoFieldNames.DUE_DATE.value, self.due_date)

  def update_task(self, task:str) -> None:
    """ Set task """
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    if task is not None and task != "":
      self.task = task
      self.table.update_field(self.row.id, TodoFieldNames.TASK_NAME.value, self.task)

  def update_notes(self, notes:str) -> None:
    """ Set notes """
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    if notes is not None and notes != "":
      self.notes = notes
      self.table.update_field(self.row.id, TodoFieldNames.NOTES.value, self.notes)

  def update_status(self, status:str) -> None:
    """ Set status """
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    if status is not None and status != "":
      self.status = status
      self.table.update_field(self.row.id, TodoFieldNames.STATUS.value, self.status)

  @staticmethod
  def find_by_id(table:Table, id:str):
    """ Find todo by id """
    if table is not None:
      return table.find_by_id(Todo, Todo._field_name_mappings(), id)
    return None

  @staticmethod
  def create_print_table(table:Table, todo_filter:TodoFilterType=TodoFilterType.UNFINISHED) -> List[List[str]]:
    """ Filters all elements and creates structure for the todos to be nicely printed """
    rows = Todo._rows(table)
    if rows is None:
      todos = []
    else:
      match todo_filter:
        case TodoFilterType.ALL:
          filter_func = lambda todo: True
        case TodoFilterType.WEEK:
          filter_func = Todo._week_filter
        case TodoFilterType.UNFINISHED:
          filter_func = lambda todo: not todo.is_completed()
      max_date = date(3000, 1, 1)
      todos = sorted(filter(filter_func, rows), key=lambda t: max_date if t.due_date is None else t.due_date)
      todos = list(map(lambda todo: [str(todo.id), str(todo.task), str(todo.status), str(todo.due_date), str(todo.completed_at)], todos))
    todos.insert(0, ["Id", "Task", "Status", "Due_Date", "Completed_At"])
    return todos

  @staticmethod
  def create_table(smart:Smartsheet, table_name:str, folder_id:str) -> Table:
    sheet_spec = smart.models.Sheet({
      "name": table_name,
      "columns": [{
        "title": TodoFieldNames.ID.value,
        "type": "TEXT_NUMBER",
        "systemColumnType": TodoFieldNames.ID_TYPE.value,
        "autoNumberFormat": {
          "startingNumber": 1
        }
      }, {
        "title": TodoFieldNames.TASK_NAME.value,
        "type": TodoFieldNames.TASK_NAME_TYPE.value,
        "primary": True
      }, {
        "title": TodoFieldNames.DUE_DATE.value,
        "type": TodoFieldNames.DUE_DATE_TYPE.value
      }, {
        "title": TodoFieldNames.COMPLETED_AT.value,
        "type": TodoFieldNames.COMPLETED_AT_TYPE.value
      }, {
        "title": TodoFieldNames.NOTES.value,
        "type": TodoFieldNames.NOTES_TYPE.value
      }, {
        "title": TodoFieldNames.STATUS.value,
        "type": TodoFieldNames.STATUS_TYPE.value,
        "options": [TodoStatusType.BACKLOG.value, TodoStatusType.ACTIVE_SPRINT.value, TodoStatusType.IN_PROGRESS.value, TodoStatusType.DONE.value, TodoStatusType.OBE.value]
      }, {
        "title": "ModifiedAt",
        "type": "DATETIME",
        "systemColumnType": "MODIFIED_DATE"
      }, {
        "title": "ModifiedBy",
        "type": "CONTACT_LIST",
        "systemColumnType": "MODIFIED_BY"
      }, {
        "title": "CreatedAt",
        "type": "DATETIME",
        "systemColumnType": "CREATED_DATE"
      }, {
        "title": "CreatedBy",
        "type": "CONTACT_LIST",
        "systemColumnType": "CREATED_BY"
      }]
    })

    response = smart.Folders.create_sheet_in_folder(folder_id, sheet_spec)
    new_sheet = response.result
    return new_sheet

  """ Helper Methods """
  @staticmethod
  def _week_filter(todo:Self) -> bool:
    """ Things not yet done for this week """
    now = datetime.now()
    sunday = (now - timedelta(days = now.weekday() + 1)).date()
    saturday = (now - timedelta(days = now.weekday() - 5)).date()
    return todo.due_date is not None and not todo.is_completed() and todo.due_date >= sunday and todo.due_date <= saturday

  @staticmethod
  def _field_name_mappings() -> dict[str, str]:
    """ External to internal field names """
    return {
      TodoFieldNames.TASK_NAME.value: "task_object",
      TodoFieldNames.DUE_DATE.value: "due_date_object",
      TodoFieldNames.ID.value: "id_object",
      TodoFieldNames.COMPLETED_AT.value: "completed_at_object",
      TodoFieldNames.NOTES.value: "notes_object",
      TodoFieldNames.STATUS.value: "status_object",
    }

  @staticmethod
  def _rows(table:Table):
    """ Get all rows """
    if table is not None:
      return table.map_rows(Todo, Todo._field_name_mappings())
    return None
