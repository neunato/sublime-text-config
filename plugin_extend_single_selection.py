from sublime_plugin import TextCommand, EventListener


class SingleSelection(EventListener):
   """
   Add reverse parameter to control whether first or last selection will remain.
   """
   def on_text_command(self, view, command, args):
      if command == "single_selection" and args and args.get("reverse"):
         return "private_last_selection"


class PrivateLastSelection(TextCommand):
   def run(self, edit):
      view = self.view
      sels = view.sel()
      last = sels[-1]
      sels.clear()
      sels.add(last)
