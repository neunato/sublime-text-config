from sublime import Region
from sublime_plugin import TextCommand


class SplitSelectionIntoChars(TextCommand):
   """
   Split selections into characters.
   """
   def run(self, edit):
      view = self.view
      sels = view.sel()
      for reg in list(sels):
         if reg.empty():
            reg = view.word(reg)
         if reg.empty():
            continue
         pos = reg.begin()
         size = reg.size()
         regs = [Region(pos+i, pos+i+1) for i in range(size)]
         sels.subtract(reg)
         sels.add_all(regs)


class SplitSelection(TextCommand):
   """
   Run split_selection_into_lines or split_selection_into_chars if nothing changed.

   Optionally ignore empty lines.
   """
   def run(self, edit, empty=True):
      view = self.view
      sels = view.sel()
      init = list(sels)

      view.run_command("split_selection_into_lines")

      # remove empty lines
      if not empty:
         regs = list(sels)
         for sel in regs:
            line = view.line(sel)
            if line.empty():
               sels.subtract(sel)

         # all lines empty, keep last selection
         if len(sels) == 0:
            sels.add(regs[-1])

      # unaltered selections - split into chars
      if init == list(sels):
         view.run_command("split_selection_into_chars")
