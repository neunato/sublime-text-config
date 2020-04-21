from re import sub
from sublime_plugin import TextCommand


class JoinLinesExtCommand(TextCommand):
   """
   Run join_lines on multiline selection, else remove whitespace from
   selection.
   """
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
