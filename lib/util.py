from typing import List
from datetime import datetime, date

class Util:
    """ Utility object """

    @staticmethod
    def parse_date(date_str:str) -> date:
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    @staticmethod
    def date_as_str(date_obj:date) -> str:
        return date_obj.strftime('%Y-%m-%d')

    @staticmethod
    def print_table(table:List[List[str]]) -> None:
        longest_cols = [
            (max([len(str(row[i])) for row in table]) + 3)
            for i in range(len(table[0]))
        ]
        row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
        for row in table:
            print(row_format.format(*row))

    @staticmethod
    def parse_args(line:str) -> dict[str, str]:
        args = {}
        parts = line
        while parts != "":
            parts = parts.split(':')
            key = parts[0]
            rest = ":".join(parts[1:])
            if len(rest) == 0:
                continue
            if rest[0] == "'":
                separator = "'"
                rest = "".join(rest[1:])
            elif rest[0] == '"':
                separator = '"'
                rest = "".join(rest[1:])
            else:
                separator = " "
            quotes = rest.split(separator)
            args[key.strip()] = quotes[0].strip()
            parts = separator.join(quotes[1:]).strip()
        return args
