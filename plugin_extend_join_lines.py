from re import sub, match
from sublime_plugin import TextCommand


class JoinWhitespace(TextCommand):
   """
   Join multi-line selections into a single line; join consecutive whitespace
   of single-line selections, or remove all whitespace if none are consecutive.
   """
   def run(self, edit):
      view = self.view
      for sel in view.sel():
         if sel.empty():
            continue
         s = view.substr(sel)

         # remove newlines and surrounding whitespace
         if "\n" in s:
            r = sub("\s*\n\s*", " ", s)

         # replace/remove whitespace from single line
         else:
            r = sub("\s+", " ", s)
            if r == s:
               r = sub("\s", "", s)

         view.replace(edit, sel, r)
