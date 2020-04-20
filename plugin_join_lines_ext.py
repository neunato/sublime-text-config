import re
from sublime_plugin import TextCommand


class JoinLinesExtCommand(TextCommand):
   def run(self, edit):
      view = self.view
      for reg in view.sel():
         if reg.empty():
            continue
         sel = view.substr(reg)
         if "\n" in sel:
            view.replace(edit, reg, re.sub("\s*\n\s*", " ", sel))
         else:
            view.replace(edit, reg, re.sub("\s+", " ", sel))
