from sublime_plugin import WindowCommand


class SlurpFindStringExtCommand(WindowCommand):
   """
   Run slurp_find_string on first or last selection based on forward.
   """
   def run(self, forward=True):
      slurp_find_panel_strings(self.window, forward, "slurp_find_string")


class SlurpReplaceStringExtCommand(WindowCommand):
   """
   Run slurp_find_string on first or last selection based on forward.
   """
   def run(self, forward=True):
      slurp_find_panel_strings(self.window, forward, "slurp_replace_string")


def slurp_find_panel_strings(window, forward, slurp_command):
   if forward:
      window.run_command(slurp_command)
   else:
      view = window.active_view()
      sels = view.sel()
      regs = list(sels)
      sels.clear()
      sels.add(regs[0])
      window.run_command(slurp_command)
      sels.add_all(regs[1:])
