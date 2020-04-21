from sublime import Region
from sublime_plugin import TextCommand


class SplitSelectionIntoLinesExtCommand(TextCommand):
   """
   Run split_selection_into_lines on multiline selection, else split into
   characters.
   """
   def run(self, edit):
      view = self.view
      selection = view.sel()
      for reg in list(selection):
         if reg.empty():
            reg = view.word(reg)
         if reg.empty():
            continue

         row_begin, _ = view.rowcol(reg.begin())
         row_end, _ = view.rowcol(reg.end())

         if row_begin == row_end:
            pos = reg.begin()
            size = reg.size()
            regs = [Region(pos+i, pos+i+1) for i in range(size)]
            selection.subtract(reg)
            selection.add_all(regs)
         else:
            view.run_command("split_selection_into_lines")
