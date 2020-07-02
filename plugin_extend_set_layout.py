from sublime import set_timeout
from sublime_plugin import WindowCommand, EventListener


class SetLayout(EventListener):
   """
   Move active and all tabs to the right to the newly created group, if any.
   """
   def on_window_command(self, window, command, args):
      if command == "set_layout" and args and args.get("transfer"):
         del args["transfer"]
         return "private_set_layout", args


class PrivateSetLayout(WindowCommand):
   def run(self, **args):
      window = self.window

      sheet = window.active_sheet()
      g, i = window.get_sheet_index(sheet)

      window.run_command("set_layout", args)

      h = window.num_groups() - 1

      if g == -1:
         return
      if g >= h:
         return

      o = window.sheets_in_group(h)
      o = len(o)

      sheets = window.sheets_in_group(g)
      sheets = sheets[i:]
      for j, s in enumerate(sheets):
         window.set_sheet_index(s, h, j + o)

      sheets = window.sheets_in_group(g)
      last_in_group = not sheets

      if last_in_group:
         set_timeout(lambda: window.focus_sheet(sheet))
      else:
         window.focus_sheet(sheet)
