from sublime_plugin import ViewEventListener


class AutoClosePanel(ViewEventListener):
   """
   Close find panel once it loses focus.

   Controlled by _auto_close_find_panel setting.
   """
   @classmethod
   def is_applicable(cls, settings):
      auto_close = settings.get("_auto_close_find_panel")
      is_widget = settings.get("is_widget")
      return auto_close and not is_widget

   def on_activated(self):
      window = self.view.window()
      panel = window.active_panel()
      if panel in ("find", "replace", "find_in_files", "incremental_find"):
         window.run_command("hide_panel")
