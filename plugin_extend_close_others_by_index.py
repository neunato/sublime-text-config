from sublime_plugin import EventListener


class CloseTabsByIndex(EventListener):
   """
   Run on active view if called without parameters.

   Needed for binding to a key.
   """
   def on_window_command(self, window, command, args):
      if command in ("close_others_by_index", "close_to_right_by_index") and args is None:
         active = window.active_sheet()
         g, i = window.get_sheet_index(active)
         args = {"group": g, "index": i}
         return command, args
