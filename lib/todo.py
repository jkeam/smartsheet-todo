from smartsheet import Smartsheet
from smartsheet.models import Sheet, Row
from datetime import date
from typing import List, Self
from . import Table

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
    data = { "TaskName": self.task }
    if self.due_date is not None:
        data["DueDate"] = self.due_date
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
      task=row.get_column(id_lookup["TaskName"]),
      due_date=row.get_column(id_lookup["DueDate"]),
      id=row.get_column(id_lookup["Id"]),
      row_id=row.id
    )
