from sublime_plugin import WindowCommand


class NextViewInGroupCommand(WindowCommand):
   def run(self):
      switch_view_in_group(self.window, forward=True)


class PrevViewInGroupCommand(WindowCommand):
   def run(self):
      switch_view_in_group(self.window, forward=False)


def switch_view_in_group(window, forward=True):
   group = window.active_group()
   sheets = window.sheets_in_group(group)
   active = window.active_sheet()
   n = len(sheets)
   o = 1 if forward else -1
   i = (sheets.index(active) + o + n) % n
   window.focus_sheet(sheets[i])
