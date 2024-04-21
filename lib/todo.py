from datetime import date, datetime
from enum import Enum
from typing import List
from . import Table, Util

class TodoFieldNames(Enum):
  """ Todo Schema """
  TASK_NAME = "TaskName"        # Text/Number
  DUE_DATE = "DueDate"          # Date
  ID = "Id"                     # Auto Number
  COMPLETED_AT = "CompletedAt"  # Date
  NOTES = "Notes"               # Text/Number

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
    self.table = table
    self.task = task
    self.due_date = due_date
    self.notes = notes

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

  def is_completed(self) -> bool:
    return self.completed_at is not None

  def save(self) -> None:
    """ Save todo """
    data = {
      TodoFieldNames.TASK_NAME.value: self.task
    }
    if self.notes is not None:
      data[TodoFieldNames.NOTES.value]: self.notes
    if self.due_date is not None:
      data[TodoFieldNames.DUE_DATE.value] = Util.date_as_str(self.due_date)
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

  @staticmethod
  def find_by_id(table:Table, id:str):
    """ Find todo by id """
    if table is not None:
      return table.find_by_id(Todo, Todo._field_name_mappings(), id)
    return None

  @staticmethod
  def create_print_table(table:Table, show_all:bool=False) -> List[List[str]]:
    rows = Todo._rows(table)
    if rows is None:
        todos = []
    else:
      if show_all:
        filter_func = lambda todo: True
      else:
        filter_func = lambda todo: not todo.is_completed()
      max_date = date(3000, 1, 1)
      todos = sorted(filter(filter_func, rows), key=lambda t: max_date if t.due_date is None else t.due_date)
      todos = list(map(lambda todo: [str(todo.id), str(todo.task), str(todo.due_date), str(todo.completed_at)], todos))

    todos.insert(0, ["Id", "Task", "Due_Date", "Completed_At"])
    return todos

  """ Helper Methods """
  @staticmethod
  def _field_name_mappings() -> dict[str, str]:
    """ External to internal field names """
    return {
      TodoFieldNames.TASK_NAME.value: "task_object",
      TodoFieldNames.DUE_DATE.value: "due_date_object",
      TodoFieldNames.ID.value: "id_object",
      TodoFieldNames.COMPLETED_AT.value: "completed_at_object",
      TodoFieldNames.NOTES.value: "notes_object"
    }

  @staticmethod
  def _rows(table:Table):
    """ Get all rows """
    if table is not None:
      return table.map_rows(Todo, Todo._field_name_mappings())
    return None
