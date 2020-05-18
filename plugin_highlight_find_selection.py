from sublime import DRAW_NO_FILL
from sublime_plugin import EventListener


class HighlightFindSelection(EventListener):
   """
   Highlight find selection while panel is open.

   Controlled by _highlight_find_selection setting.
   """
   def on_window_command(self, window, command, args):
      if command != "show_panel":
         return

      panel = args.get("panel")
      if panel not in ("find", "replace", "find_in_files", "incremental_find"):
         return

      view = window.active_view()
      settings = view.settings()
      highlight = settings.get("_highlight_find_selection")
      if not highlight:
         return

      sels = view.sel()
      view = window.active_view()
      view.add_regions("_find_selection", sels, scope="comment", flags=DRAW_NO_FILL)

   def on_post_window_command(self, window, command, args):
      if command != "hide_panel":
         return
      view = window.active_view()
      view.erase_regions("_find_selection")
