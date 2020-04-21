from sublime_plugin import TextCommand


class UnselectLinesCommand(TextCommand):
   """
   Remove first or last selection based on forward.
   """
   def run(self, edit, forward):
      view = self.view
      i = -1 if forward else 0
      selection = view.sel()
      if len(selection) > 1:
         selection.subtract(selection[i])
