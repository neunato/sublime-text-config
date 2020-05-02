from sublime_plugin import WindowCommand


class ToggleRegexExt(WindowCommand):
   """
   Run toggle_regex regardless of find panels being open, and make it trigger command listeners.
   """
   def run(self):
      toggle_find_panel_setting(self.window, "toggle_regex")


class ToggleCaseSensitiveExt(WindowCommand):
   """
   Run toggle_case_sensitive regardless of find panels being open, and make it trigger command listeners.
   """
   def run(self):
      toggle_find_panel_setting(self.window, "toggle_case_sensitive")


class ToggleWholeWordExt(WindowCommand):
   """
   Run toggle_whole_word regardless of find panels being open, and make it trigger command listeners.
   """
   def run(self):
      toggle_find_panel_setting(self.window, "toggle_whole_word")


def toggle_find_panel_setting(window, command):
   panel = window.active_panel()
   if panel in ("find", "replace", "find_in_files", "incremental_find"):
      window.run_command(command)
   else:
      window.run_command("show_panel", {"panel": "find"})
      window.run_command(command)
      window.run_command("hide_panel")
      if panel:
         window.run_command("show_panel", {"panel": panel})
