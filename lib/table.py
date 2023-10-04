from smartsheet import Smartsheet
from smartsheet.models import Sheet, DateObjectValue
from smartsheet.sheets import Sheets
from smartsheet.models.enums.column_type import ColumnType
from typing import List, Any
from datetime import date

class Table:
  """ Represents table """

  def __init__(self, smart:Smartsheet, sheet:Sheet) -> None:
    self.smart = smart
    self.sheet = sheet
    self.rows = sheet.rows
    self.name = sheet.name
    self.row_count = sheet.total_row_count
    self.title_to_id = {x.title:x.id for x in sheet.columns}

  def insert_row(self, row:dict[str, Any]) -> None:
    new_row = self.smart.models.Row()
    for col_name, col_value in row.items():
      new_cell = self.smart.models.Cell()
      new_cell.column_id = self.title_to_id[col_name]

      if isinstance(col_value, date):
        val = col_value.strftime('%m/%d/%Y')
        new_cell.object_value = {"objectType": "DATE", "value": val}
      else:
        new_cell.value = col_value
      new_row.cells.append(new_cell)
    self.sheet.add_rows([new_row])

  def delete_row(self, ids:List[str]) -> None:
    self.sheet.delete_rows(ids)
