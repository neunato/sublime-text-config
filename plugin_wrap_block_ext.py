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
   return indent1 < indent2


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
   """
   Wrap and reindent the block of code that follows with begin and end
   characters, stopping at the first newline.
   """
   def run(self, edit, begin, end):
      if len(begin) != 1:
         raise Exception("'begin' must be a single character")
      if len(end) != 1:
         raise Exception("'end' must be a single character")

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
         block_a = sel.a + offset
         block_b = block_a
         cursors.append(Region(block_a + 1))

         block_indent = view.indentation_level(block_a + 1)

         # detect block location and indentation level
         line = view.line(block_a + 1)
         while True:
            string = view.substr(line)

            # break on empty line
            if is_ws(string):
               break

            # break on indentation smaller than first line
            indent = view.indentation_level(line.a)
            if indent < block_indent:
               if not (indent + 1 == block_indent and string.strip() == end):
                  view.insert(edit, line.a, "\n")
               break

            # break on end of file
            if line.b == size:
               view.insert(edit, size, "\n")
               break

            # break if closing bracket found in block and is last char in line
            i = 0
            end_count = 0
            for char in string:
               if char == begin:
                  end_count -= 1
               elif char == end:
                  end_count += 1
               if end_count > 0:
                  break
               i += 1

            end_line = string[i:].strip()
            if end_count > 0 and len(end_line) == 1:
               if end_line[0] != end:
                  end_line = "\t" * (block_indent - 1)
               else:
                  end_line = "\n" + "\t" * (block_indent - 1)
               view.insert(edit, line.a + i, end_line)
               end = ""
               break

            # move to the next line
            block_b = line.b
            line = view.line(line.b + 1)

         # no block follows, simply output begin and end characters
         if block_a == block_b:
            view.insert(edit, block_a, begin + end)
            offset += len(begin) + len(end)
            continue

         # select block and adjust indentation
         block = Region(block_a + 1, block_b)
         sels.clear()
         sels.add(block)

         cursor_indent = view.indentation_level(block_a)
         diff = block_indent - cursor_indent - 1
         if diff > 0:
            for i in range(diff):
               view.run_command("unindent")
         else:
            for i in range(-diff):
               view.run_command("indent")

         # wrap block with begin and end characters, keeping in mind that
         # reindenting messed up the block region
         view.run_command("move", {"by": "characters", "forward": True, "extend": True})
         last_line = view.line(sels[0].b)
         next_line = view.line(sels[0].b + 1)

         use_spaces = settings.get("translate_tabs_to_spaces")
         if use_spaces:
            tab_size = settings.get("tab_size")
            end_line = tab_size * " " * cursor_indent + end
         else:
            end_line = "\t" * cursor_indent + end

         if view.substr(next_line) != end_line:
            view.replace(edit, last_line, "\t"*cursor_indent + end)
         view.insert(edit, block_a, begin)

         # adjust selection offset
         offset += view.size() - size

      # restore cursors
      sels.clear()
      sels.add_all(cursors)

      # restore settings
      if trim_auto_ws:
         settings.set("trim_automatic_white_space", True)
