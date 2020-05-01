from sublime import Region
from sublime_plugin import WindowCommand, TextCommand


class SetFindStringCommand(WindowCommand):
   """
   Set string as "find" input field of find panels.
   """
   def run(self, string):
      set_find_panel_input(self.window, find=string)


class SetReplaceStringCommand(WindowCommand):
   """
   Set string as "replace" input field of find panels.
   """
   def run(self, string):
      set_find_panel_input(self.window, replace=string)


def set_find_panel_input(window, find=None, replace=None):
   panel = window.active_panel()
   find_panel = panel in ("find", "replace", "find_in_files", "incremental_find")
   if not find_panel:
      window.run_command("show_panel", {"panel": "find"})

   if find is not None:
      view = window.new_file()
      view.set_scratch(True)
      window.focus_view(view)
      view.run_command("insert", {"characters": find})
      view.run_command("select_all")
      window.run_command("slurp_find_string")
      view.close()

   if replace is not None:
      view = window.new_file()
      view.set_scratch(True)
      window.focus_view(view)
      view.run_command("insert", {"characters": replace})
      view.run_command("select_all")
      window.run_command("slurp_replace_string")
      view.close()

   if not find_panel:
      window.run_command("hide_panel")
      if panel:
         window.run_command("show_panel", {"panel": panel})
