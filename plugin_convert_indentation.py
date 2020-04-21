from os.path import normpath
from sublime import packages_path, load_resource, decode_value, windows
from sublime_plugin import TextCommand, EventListener


class ConvertIndentationCommand(TextCommand):
   """
   Convert indentation to reflect the user's settings.

   Run automatically based on _auto_convert_indentation setting.
   """

   def run(self, _):
      view = self.view
      if view.is_read_only():
         return
      if view.is_loading():
         return

      settings = view.settings()
      tab_size = settings.get("tab_size")
      use_spaces = settings.get("translate_tabs_to_spaces")

      # detect_indentation updates settings
      view.run_command("detect_indentation", {"show_message": False, "threshold": 1})
      file_tab_size = settings.get("tab_size")
      file_use_spaces = settings.get("translate_tabs_to_spaces")

      if file_tab_size == tab_size and file_use_spaces == use_spaces:
         return

      # spaces -> spaces
      if file_use_spaces and use_spaces:
         view.run_command("unexpand_tabs", {"set_translate_tabs": False})
         settings.set("tab_size", tab_size)
         view.run_command("expand_tabs", {"set_translate_tabs": False})

      # spaces -> tabs
      elif file_use_spaces and not use_spaces:
         view.run_command("unexpand_tabs", {"set_translate_tabs": False})

      # tabs -> spaces
      elif not file_use_spaces and use_spaces:
         view.run_command("expand_tabs", {"set_translate_tabs": False})

      # restore settings
      settings.set("tab_size", tab_size)
      settings.set("translate_tabs_to_spaces", use_spaces)


class ConvertIndentationListener(EventListener):

   # convert indentation when opening a file
   def on_load(self, view):
      settings = view.settings()
      auto_indent = settings.get("_auto_convert_indentation")
      detect_indent = settings.get("detect_indentation")
      if not auto_indent:
         return
      if detect_indent:
         return
      view.run_command("convert_indentation")


   # convert indentation when view changes its settings
   def on_post_text_command(self, view, command, args):
      if command not in ("set_setting", "toggle_setting"):
         return
      if args.get("setting") not in ("tab_size", "translate_tabs_to_spaces"):
         return
      settings = view.settings()
      auto_indent = settings.get("_auto_convert_indentation")
      if auto_indent:
         view.run_command("convert_indentation")


   # convert indentation in open files when Preferences.sublime-settings change
   def on_post_save(self, view):
      settings_path = normpath(packages_path() + "/User/Preferences.sublime-settings")
      file_name = view.file_name()
      if file_name != settings_path:
         return

      settings = load_resource("Packages/User/Preferences.sublime-settings")
      settings = decode_value(settings)
      auto_indent = settings.get("_auto_convert_indentation")
      if not auto_indent:
         return

      tab_size = settings.get("tab_size")
      use_spaces = settings.get("translate_tabs_to_spaces")

      views = [v for w in windows() for v in w.views()]
      for view in views:
         view_settings = view.settings()
         view_tab_size = view_settings.get("tab_size")
         view_use_spaces = view_settings.get("translate_tabs_to_spaces")

         if view_tab_size != tab_size or view_use_spaces != use_spaces:
            view_settings.set("tab_size", tab_size)
            view_settings.set("translate_tabs_to_spaces", use_spaces)
            view.run_command("convert_indentation")
