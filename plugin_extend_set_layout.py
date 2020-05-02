from sublime import set_timeout
from sublime_plugin import EventListener


class SetLayout(EventListener):
   """
   Move active and all tabs to the right to the newly created group, if any.
   """
   active = None

   def on_window_command(self, window, command, args):
      if command == "set_layout":
         self.active = window.active_sheet()

   def on_post_window_command(self, window, command, args):
      if command == "set_layout":
         active = self.active
         g, i = window.get_sheet_index(active)
         h = window.active_group()
         n = window.num_groups() - 1
         if g == -1:
            return
         if g >= n:
            return
         sheets = window.sheets_in_group(g)
         sheets = sheets[i:]
         for j, sheet in enumerate(sheets):
            window.set_sheet_index(sheet, h, j)
         set_timeout(lambda: window.focus_sheet(active), 1)
