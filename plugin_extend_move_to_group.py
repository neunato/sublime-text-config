from sublime import set_timeout
from sublime_plugin import WindowCommand, EventListener


class MoveToGroup(EventListener):
   """
   Move sheet to group and focus it, even when last in group.
   """
   def on_window_command(self, window, command, args):
      if command == "move_to_group" and args:
         return "private_move_to_group", args


class PrivateMoveToGroup(WindowCommand):
   def run(self, group):
      window = self.window
      sheet = window.active_sheet()

      g, i = window.get_sheet_index(sheet)
      n = window.sheets_in_group(g)
      n = len(n) - 1
      last_in_group = i == n

      index = window.sheets_in_group(group)
      index = len(index)
      window.set_sheet_index(sheet, group, index)

      if last_in_group:
         set_timeout(lambda: window.focus_sheet(sheet))
      else:
         window.focus_sheet(sheet)
