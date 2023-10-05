from smartsheet import Smartsheet
from smartsheet.models import Sheet, Row
from datetime import date
from typing import List, Self
from enum import Enum
from . import Table


class TodoFieldNames(Enum):
  """ Todo field names """
  TASK_NAME = "TaskName"
  DUE_DATE = "DueDate"
  ID = "Id"

class Todo:
  """ Todo """

  def __init__(self, table:Table, task:str=None, due_date:date=None, id:str=None, row_id:str=None) -> None:
    self.table = table
    self.task = task
    self.due_date = due_date
    self.id = id
    self.row_id = row_id

  def __str__(self) -> str:
    return f"Todo: {{ id: {self.id.display_value}, row_id: {self.row_id} }}"

  def save(self) -> None:
    data = { TodoFieldNames.TASK_NAME.value: self.task }
    if self.due_date is not None:
        data[TodoFieldNames.DUE_DATE.value] = self.due_date
    self.table.insert_row(data)

  def delete(self) -> None:
    self.table.delete_row([self.row_id])

  @staticmethod
  def rows(table:Table) -> List[Self]:
    return list(map(lambda x: Todo._map(table, x), table.rows))

  @staticmethod
  def _map(table:Table, row:Row) -> Self:
    id_lookup = table.title_to_id
    return Todo(
      table,
      task=row.get_column(id_lookup[TodoFieldNames.TASK_NAME.value]),
      due_date=row.get_column(id_lookup[TodoFieldNames.DUE_DATE.value]),
      id=row.get_column(id_lookup[TodoFieldNames.ID.value]),
      row_id=row.id
    )
