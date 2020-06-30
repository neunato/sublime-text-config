from sublime import DRAW_NO_FILL
from sublime_plugin import EventListener


class HighlightFindSelection(EventListener):
   """
   Highlight find selection while panel is open.

   Controlled by _highlight_find_selection setting.
   """
   def on_window_command(self, window, command, args):
      if command == "show_panel":
         view = window.active_view()

         # another panel shown, clear highlight
         panel = args.get("panel")
         if panel not in ("find", "replace", "find_in_files", "incremental_find"):
            view.erase_regions("_find_selection")
            return

         # find panel shown, highlight selection
         settings = view.settings()
         highlight = settings.get("_highlight_find_selection")
         if highlight:
            sels = view.sel()
            view.add_regions("_find_selection", sels, scope="comment", flags=DRAW_NO_FILL)
            return

      # panel closed, clear highlight
      if command == "hide_panel":
         view = window.active_view()
         view.erase_regions("_find_selection")


   def on_activated(self, view):
      # view focused, clear highlight
      view.erase_regions("_find_selection")

      # view focused and find panel shown, highlight selection
      window = view.window()
      if not window:
         return

      panel = window.active_panel()
      if panel in ("find", "replace", "find_in_files", "incremental_find"):
         sels = view.sel()
         view.add_regions("_find_selection", sels, scope="comment", flags=DRAW_NO_FILL)
