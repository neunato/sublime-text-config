import sublime
from sublime_plugin import TextCommand, EventListener


class TrimFileCommand(TextCommand):
   def run(self, edit, bof=True, eof=True):
      view = self.view

      if bof:
         reg = view.find("\A\s*", 0)
         view.replace(edit, reg, "")

      if eof:
         # reimplement ensure_newline_at_eof_on_save as it fires before on_pre_save
         reg = view.find("\s*\Z", 0)
         settings = view.settings()
         eof_newline = settings.get("ensure_newline_at_eof_on_save")
         if eof_newline:
            view.replace(edit, reg, "\n")
         else:
            view.replace(edit, reg, "")


class TrimFileListener(EventListener):
   def on_pre_save(self, view):
      settings = view.settings()
      trim = settings.get("_trim_file_on_save")
      if trim:
         view.run_command("trim_file")
