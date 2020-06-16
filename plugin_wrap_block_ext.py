from sublime import Region, OP_EQUAL, OP_NOT_EQUAL
from sublime_plugin import TextCommand, EventListener


def is_ws(str):
   for c in str:
      if c != " " and c != "\t":
         return False
   return True


def indented_block(view, r):
   if not r.empty():
      return False

   if r.a == view.size():
      return False

   line = view.line(r)
   indent1 = view.indentation_level(line.b)
   indent2 = view.indentation_level(line.b + 1)
   return indent1 == indent2 - 1


class WrapBlockExtListener(EventListener):
   def on_query_context(self, view, key, operator, operand, match_all):
      if key != "indented_block":
         return None

      if operator != OP_EQUAL and operator != OP_NOT_EQUAL:
         return False

      is_all = True
      is_any = False

      for r in view.sel():
         if operator == OP_EQUAL:
            b = (operand == indented_block(view, r))
         else:
            b = (operand != indented_block(view, r))

         if b:
            is_any = True
         else:
            is_all = False

      if match_all:
         return is_all
      else:
         return is_any


class WrapBlockExt(TextCommand):
   def run(self, edit, begin, end):
      view = self.view
      settings = view.settings()

      # messes up selection offsets
      trim_auto_ws = settings.get("trim_automatic_white_space")
      if trim_auto_ws:
         settings.set("trim_automatic_white_space", False)

      sels = view.sel()
      cursors = []
      offset = 0

      for sel in list(sels):
         if not sel.empty():
            continue

         size = view.size()
         start = sel.a + offset
         cursors.append(Region(start + 1))

         # detect block location and indentation level
         block_indent = float("inf")
         line = view.line(start + 1)
         while not is_ws(view.substr(line)):
            indent = view.indentation_level(line.a)
            if indent < block_indent:
               block_indent = indent
            if line.b == size:
               view.insert(edit, size, "\n")
            line = view.line(line.b + 1)

         # no block follows, simply output begin and end characters
         if block_indent == float("inf"):
            view.insert(edit, start, begin + end)
            offset += len(begin) + len(end)
            continue

         # select block and adjust indentation
         block = Region(start + 1, line.a - 1)
         sels.clear()
         sels.add(block)

         indent = view.indentation_level(start)
         diff = block_indent - indent - 1
         if diff > 0:
            for i in range(diff):
               view.run_command("unindent")
         else:
            for i in range(-diff):
               view.run_command("indent")

         # wrap block with begin and end characters
         view.run_command("move", {"by": "lines", "forward": True})
         line = view.line(sels[0].a)

         view.replace(edit, line, "\t"*indent + end)
         view.insert(edit, start, begin)

         # adjust selection offset
         offset += view.size() - size

      # restore cursors
      sels.clear()
      sels.add_all(cursors)

      # restore settings
      if trim_auto_ws:
         settings.set("trim_automatic_white_space", True)
