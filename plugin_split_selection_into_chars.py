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
