from sublime import Region
from sublime_plugin import TextCommand


class ExpandSelectionToParagraphSubCommand(TextCommand):
   """
   Subtract paragraph enclosing the mouse position from selection.
   """
   def want_event(self):
      return True

   def run(self, edit, **args):
      view = self.view
      selection = view.sel()

      pos = args["event"]
      pos = (pos["x"], pos["y"])
      pos = view.window_to_text(pos)
      pos = Region(pos)

      regs = list(selection)
      selection.clear()
      selection.add(pos)
      view.run_command("expand_selection_to_paragraph", args)
      reg = selection[0]

      selection.clear()
      selection.add_all(regs)
      selection.subtract(reg)
