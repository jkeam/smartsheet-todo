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

  def __init__(self, table:Table=None, task:str=None, due_date:date=None) -> None:
    self.id = None
    self.row_id = None
    self.row = None
    self.task_object = None
    self.due_date_object = None
    self.completed_at_object = None
    self.id_object = None
    self.table = table
    self.task = task
    self.due_date = due_date

  def __str__(self) -> str:
    return f"Todo: {{ id: {self.id}, row_id: {self.row_id} }}"

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
  def row(self):
      return self._row

  @row.setter
  def row(self, value):
    if value is not None:
      self.row_id = value.id
    self._row = value

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
    data = { TodoFieldNames.TASK_NAME.value: self.task }
    if self.due_date is not None:
      data[TodoFieldNames.DUE_DATE.value] = self.due_date
    self.table.insert_row(data)

  def delete(self) -> None:
    if self.row_id is None:
      print("Unable to delete, missing row_id")
    else:
      self.table.delete_row([self.row_id])

  def finish(self) -> None:
    self.completed_at = datetime.now().date()
    self.table.update_field(self.row_id, TodoFieldNames.COMPLETED_AT.value, self.completed_at)

  def unfinish(self) -> None:
    self.completed_at = None
    self.table.update_field(self.row_id, TodoFieldNames.COMPLETED_AT.value, self.completed_at)

  @staticmethod
  def field_names() -> List[str]:
    return [TodoFieldNames.TASK_NAME.value, TodoFieldNames.DUE_DATE.value, TodoFieldNames.ID.value, TodoFieldNames.COMPLETED_AT.value]

  @staticmethod
  def field_name_mappings() -> dict[str, str]:
    return {
      TodoFieldNames.TASK_NAME.value: "task_object",
      TodoFieldNames.DUE_DATE.value: "due_date_object",
      TodoFieldNames.ID.value: "id_object",
      TodoFieldNames.COMPLETED_AT.value: "completed_at_object"
    }
