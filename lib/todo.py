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

  def __init__(self, table:Table, task:str=None, due_date:date=None) -> None:
    self.table = table
    self._task = None
    self._due_date = None
    self._id = None
    self.task = task
    self.due_date = due_date
    self.id = None
    self.row_id = None
    self.row = None
    self.completed_at = None
    self._completed_at = None

  def from_smartsheets(self, _task:str=None, _due_date:date=None, _completed_at:date=None, _id:str=None, row:object=None) -> Self:
    self._task = _task
    self.task = _task.display_value
    self._id = _id
    self.id = _id.display_value
    self._due_date = _due_date
    if _due_date.value is not None and _completed_at.value != "":
      self.due_date = datetime.strptime(_due_date.value, '%Y-%m-%d').date()
    else:
      self.due_date = None
    self.row = row
    self.row_id = row.id
    self._completed_at = _completed_at
    if _completed_at.value is not None and _completed_at.value != "":
      self.completed_at = datetime.strptime(_completed_at.value, '%Y-%m-%d').date()
    else:
      self.completed_at = None
    return self

  def __str__(self) -> str:
    return f"Todo: {{ id: {self.id}, row_id: {self.row_id} }}"

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
  def rows(table:Table) -> List[Self]:
    return list(map(lambda x: Todo._map(table, x), table.rows))

  @staticmethod
  def _map(table:Table, row:Row) -> Self:
    id_lookup = table.title_to_id
    todo = Todo(table)
    return todo.from_smartsheets(
      _task=row.get_column(id_lookup[TodoFieldNames.TASK_NAME.value]),
      _due_date=row.get_column(id_lookup[TodoFieldNames.DUE_DATE.value]),
      _completed_at=row.get_column(id_lookup[TodoFieldNames.COMPLETED_AT.value]),
      _id=row.get_column(id_lookup[TodoFieldNames.ID.value]),
      row=row
    )
