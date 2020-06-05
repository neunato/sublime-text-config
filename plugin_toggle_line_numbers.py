from sublime import load_settings, save_settings
from sublime_plugin import WindowCommand


class ToggleLineNumbers(WindowCommand):
   """
   Toggle line_numbers setting at window level based on active view.
   """
   def run(self):
      window = self.window
      views = window.views()
      view = window.active_view()

      settings = view.settings()
      line_numbers = not settings.get("line_numbers")

      settings = load_settings("Preferences.sublime-settings")
      settings.set("line_numbers", line_numbers)
      save_settings("Preferences.sublime-settings")

      for view in views:
         settings = view.settings()
         settings.set("line_numbers", line_numbers)
