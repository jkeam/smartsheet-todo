from smartsheet import Smartsheet
from typing import List
from . import Table

class Database:
  """ Represents datastore """

  def __init__(self, smart:Smartsheet) -> None:
    self.smart = smart

  def find_table(self, table_name:str) -> Table:
    response = self.smart.Sheets.list_sheets()
    todo = list(filter(lambda x: x.name == table_name, response.data))[0]
    return Table(self.smart, self.smart.Sheets.get_sheet(todo.id))

  def list_tables(self) -> List[str]:
    response = self.smart.Sheets.list_sheets()
    return (map(lambda x: x.name, response.data))
