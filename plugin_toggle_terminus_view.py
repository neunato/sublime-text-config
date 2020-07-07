from sublime import active_window
from sublime_plugin import WindowCommand, EventListener


views = []


def plugin_loaded():
   global views
   window = active_window()
   views = window.views()
   views = reversed(views)
   views = list(views)


def is_terminus_view(view):
   settings = view.settings()
   is_terminus = settings.get("terminus_view")
   return is_terminus


class Listener(EventListener):
   def on_activated(self, view):
      settings = view.settings()
      is_widget = settings.get("is_widget")
      if is_widget:
         return

      if view in views:
         views.remove(view)
      views.append(view)

   def on_close(self, view):
      if view in views:
         views.remove(view)


class ToggleTerminusView(WindowCommand):
   """
   Focus last used non-terminus view if terminus is active, else focus last
   used terminus view or create a new one.
   """
   def run(self, **args):
      window = self.window
      active = window.active_view()

      # terminus tab active -> focus last active non-terminus tab
      if is_terminus_view(active):
         for view in reversed(views):
            if not is_terminus_view(view):
               window.focus_view(view)
               return

      # normal tab active -> focus last active terminus tab, or create a new one
      else:
         for view in reversed(views):
            if is_terminus_view(view):
               window.focus_view(view)
               return
         window.run_command("terminus_open", args)
