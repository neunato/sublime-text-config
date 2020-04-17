from sublime_plugin import TextCommand


class UnfoldByLevelCommand(TextCommand):
   def run(self, _, level):
      view = self.view
      level = int(level) - 1
      regions = [r for r in view.folded_regions() if view.indentation_level(r.begin()) == level]
      view.unfold(regions)
      view.show(view.sel())


class ToggleFoldByLevelCommand(TextCommand):
   def run(self, _, level):
      view = self.view
      level = int(level) - 1
      folds_exist = any(r for r in view.folded_regions() if view.indentation_level(r.begin()) == level)
      if folds_exist:
         view.run_command("unfold_by_level", {"level": level + 1})
      else:
         view.run_command("fold_by_level", {"level": level + 1})
