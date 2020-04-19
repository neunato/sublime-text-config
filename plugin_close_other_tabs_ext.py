from sublime_plugin import WindowCommand


class CloseOthersByIndexExt(WindowCommand):
   def run(self, **args):
      window = self.window
      active = window.active_sheet()
      g, i = window.get_sheet_index(active)
      if "group" not in args:
         args["group"] = g
      if "index" not in args:
         args["index"] = i
      window.run_command("close_others_by_index", args)


class CloseToRightByIndexExt(WindowCommand):
   def run(self, **args):
      window = self.window
      active = window.active_sheet()
      g, i = window.get_sheet_index(active)
      if "group" not in args:
         args["group"] = g
      if "index" not in args:
         args["index"] = i
      window.run_command("close_to_right_by_index", args)
