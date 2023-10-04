from smartsheet import Smartsheet
from smartsheet.models import Sheet
from datetime import date
from . import Table

class Todo:
  """ Todo """

  def __init__(self, table:Table, task:str = None, due_date: date = None) -> None:
    self.table = table
    self.task = task
    self.due_date = due_date
    self.id = None

  def save(self) -> None:
    data = { "TaskName": self.task }
    if self.due_date is not None:
        data["DueDate"] = self.due_date
    self.table.insert_row(data)

  def delete(self) -> None:
    self.table.delete_row([self.id])
