from re import sub
from sublime_plugin import TextCommand, EventListener


class JoinLines(EventListener):
   """
   Remove extra whitespace from single-line selections.
   """
   def on_text_command(self, view, command, args):
      if command == "join_lines":
         return "private_join_lines"


class PrivateJoinLines(TextCommand):
   def run(self, edit):
      view = self.view
      for reg in view.sel():
         if reg.empty():
            continue
         sel = view.substr(reg)
         if "\n" in sel:
            view.replace(edit, reg, sub("\s*\n\s*", " ", sel))
         else:
            view.replace(edit, reg, sub("\s+", " ", sel))
