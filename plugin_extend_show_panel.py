from sublime_plugin import EventListener


class ShowPanel(EventListener):
   """
   Close active panel regardless of focus when toggle is true.
   """
   def on_window_command(self, window, command, args):
      if command == "show_panel" and args:
         toggle = args.get("toggle")
         panel = args.get("panel")
         active = window.active_panel()
         if toggle and active and panel == active:
            return "hide_panel"
