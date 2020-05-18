from sublime_plugin import TextCommand


class ToggleCaseCommand(TextCommand):
   """
   Swap case of characters in selection based on first non-whitespace
   character.

   Work on word if selection is empty.
   """
   def run(self, edit):
      view = self.view
      for reg in view.sel():
         if reg.empty():
            reg = view.word(reg)
         if reg.empty():
            continue
         sel = view.substr(reg)
         char = sel.lstrip()[0]
         if char.isupper():
            view.replace(edit, reg, sel.lower())
         else:
            view.replace(edit, reg, sel.upper())