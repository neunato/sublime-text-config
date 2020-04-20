from sublime import Region
from sublime_plugin import TextCommand, EventListener


class TrimFileCommand(TextCommand):
   def run(self, edit, bof=True, eof=True):
      view = self.view

      if bof:
         reg = view.find("\A\s*", 0)
         view.replace(edit, reg, "")

      if eof:
         # reimplement ensure_newline_at_eof_on_save as it fires before on_pre_save
         # also taking care of bug when cursor is at eof and \n ends up selected
         reg = view.find("\s*\Z", 0)
         settings = view.settings()
         eof_newline = settings.get("_ensure_newline_at_eof_on_save")
         if eof_newline:
            view.replace(edit, reg, "\n")
            s = view.size()
            n = Region(s - 1, s)
            selection = view.sel()
            if selection.contains(n):
               selection.subtract(n)
               selection.add(Region(s))
         else:
            view.replace(edit, reg, "")


class TrimFileListener(EventListener):
   def on_pre_save(self, view):
      settings = view.settings()
      eof_newline = settings.get("ensure_newline_at_eof_on_save")
      if eof_newline is None:
         eof_newline = settings.get("_ensure_newline_at_eof_on_save")
      else:
         settings.set("ensure_newline_at_eof_on_save", None)
         settings.set("_ensure_newline_at_eof_on_save", eof_newline)

      trim = settings.get("_trim_file_on_save")
      if trim:
         view.run_command("trim_file")
