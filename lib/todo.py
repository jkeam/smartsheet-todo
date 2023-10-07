from smartsheet import Smartsheet
from smartsheet.models import Sheet, Row
from datetime import date, datetime
from typing import List, Self
from enum import Enum
from . import Table

class TodoFieldNames(Enum):
  """ Todo field names """
  TASK_NAME = "TaskName"
  DUE_DATE = "DueDate"
  ID = "Id"
  COMPLETED_AT = "CompletedAt"

class Todo:
  """ Todo """

  def __init__(self, table:Table|None=None, task:str|None=None, due_date:date|None=None) -> None:
    self.id = None
    self.row = None
    self.task_object = None
    self.due_date_object = None
    self.completed_at_object = None
    self.id_object = None
    self.table = table
    self.task = task
    self.due_date = due_date

  def __str__(self) -> str:
    return f"Todo: {{ id: {self.id}, task: {self.task}, due_date: {self.due_date}, completed_at: {self.completed_at} }}"

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
      self.due_date = datetime.strptime(value.value, '%Y-%m-%d').date()
    else:
      self.due_date = None

  @property
  def completed_at_object(self):
      return self._completed_at_object

  @completed_at_object.setter
  def completed_at_object(self, value):
    self._completed_at_object = value
    if value is not None and value.value is not None and value.value != "":
      self.completed_at = datetime.strptime(value.value, '%Y-%m-%d').date()
    else:
      self.completed_at = None

  def save(self) -> None:
    """ Save todo """
    if self.table is None:
        return
    data = { TodoFieldNames.TASK_NAME.value: self.task }
    if self.due_date is not None:
      data[TodoFieldNames.DUE_DATE.value] = self.due_date.strftime('%Y-%m-%d')
    self.table.insert_row(data)

  def delete(self) -> None:
    """ Delete todo """
    if self.table is None:
        return
    if self.row is None or self.row.id is None:
      print("Unable to delete, missing row id")
    else:
      self.table.delete_row([self.row.id])

  def finish(self) -> None:
    """ Mark as finished """
    if self.table is None:
        return
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    self.completed_at = datetime.now().date()
    self.table.update_field(self.row.id, TodoFieldNames.COMPLETED_AT.value, self.completed_at)

  def unfinish(self) -> None:
    """ Mark as not finished """
    if self.table is None:
        return
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    self.completed_at = None
    self.table.update_field(self.row.id, TodoFieldNames.COMPLETED_AT.value, self.completed_at)

  def update_due_date_as_str(self, due_date:str) -> None:
    """ Set due date """
    if self.table is None:
        return
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    if due_date is not None and due_date != "":
      self.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    else:
      self.due_date = None
    self.table.update_field(self.row.id, TodoFieldNames.DUE_DATE.value, self.due_date)

  def update_task(self, task:str) -> None:
    """ Set task """
    if self.table is None:
        return
    if self.row is None or self.row.id is None:
      print("Unable to mark, missing row id")
      return
    if task is not None and task != "":
      self.task = task
      self.table.update_field(self.row.id, TodoFieldNames.TASK_NAME.value, self.task)

  @staticmethod
  def find_by_id(table:Table, id:str) -> Self|None:
    """ Find todo by id """
    if table is not None:
      return table.find_by_id(Todo, Todo._field_name_mappings(), id)
    return None

  @staticmethod
  def rows(table:Table) -> List[Self]|None:
    """ Get all rows """
    if table is not None:
      return table.map_rows(Todo, Todo._field_name_mappings())
    return None

  """ Helper Methods """
  @staticmethod
  def _field_name_mappings() -> dict[str, str]:
    """ External to internal field names """
    return {
      TodoFieldNames.TASK_NAME.value: "task_object",
      TodoFieldNames.DUE_DATE.value: "due_date_object",
      TodoFieldNames.ID.value: "id_object",
      TodoFieldNames.COMPLETED_AT.value: "completed_at_object"
    }
