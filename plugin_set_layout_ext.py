from sublime_plugin import WindowCommand


class SetLayoutExtCommand(WindowCommand):
   """
   Run set_layout and move the selected tab and all to the right to the newly
   created group, if any.
   """
   def run(self, **args):
      window = self.window
      active = window.active_sheet()
      g, i = window.get_sheet_index(active)

      n = window.num_groups()
      window.run_command("set_layout", args)
      m = window.num_groups()
      if m <= n:
         return

      sheets = window.sheets_in_group(g)
      sheets = sheets[i:]
      h = window.active_group()
      for j, s in enumerate(sheets):
         window.set_sheet_index(s, h, j)
      window.focus_sheet(active)
