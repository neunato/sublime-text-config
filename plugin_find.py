from sublime_plugin import TextCommand

"""
Lightweight find and replace commands that unify all the builtin find commands
while eliminating inconsistencies between them.

Find panel's whole word and case sensitive settings are always respected,
regardless of initial selection or panel having focus or not.

Known limitations:
- finding with under parameter turns in_selection off

Comparison to existing commands:
       find_next                   - {"command": "find", "args": {"forward": true}}
       find_prev                   - {"command": "find", "args": {"forward": false}}
       find_under                  - {"command": "find", "args": {"forward": true,  "expand": true, "under": true}}
       find_under_prev             - {"command": "find", "args": {"forward": false, "expand": true, "under": true}}
       find_under_expand           - {"command": "find", "args": {"forward": true,  "expand": true, "under": true, "additive": true}}
 [new] find_under_expand_prev      - {"command": "find", "args": {"forward": false, "expand": true, "under": true, "additive": true}}
       find_under_expand_skip      - {"command": "find", "args": {"forward": true,  "expand": true, "under": true, "additive": true, "skip": true}
 [new] find_under_expand_skip_prev - {"command": "find", "args": {"forward": false, "expand": true, "under": true, "additive": true, "skip": true}}
       find_all                    - {"command": "find", "args": {"all": true}}
       replace_next                - {"command": "replace", "args": {"forward": true, "replace": true}}
 [new] replace_prev                - {"command": "replace", "args": {"forward": false, "replace": true}}
       replace_all                 - {"command": "replace", "args": {"all": true}}
"""


# additive selection state
last_sels = []
last_sel = None


def expand_empty_sels(view):
   sels = view.sel()
   expanded = False
   for sel in list(sels):
      if not sel.empty():
         continue
      sel = view.word(sel)
      sel = view.split_by_newlines(sel)[0]
      if not sel.empty():
         sels.add(sel)
         expanded = True
   return expanded


def slurp_find_string(window, additive, forward):
   # find_under, find_under_expand and slurp_find_string use their own logic
   # for whole_word (empty selection turns it on) regardless of what's shown
   # in the panel. we can fix the issue by reopening the panel (and lose the
   # in_selection setting) or by toggling whole_word twice (only possible if
   # panel has focus)

   view = window.active_view()
   sels = view.sel()
   if additive and not forward and len(sels) > 1:
      regs = list(sels)
      sels.clear()
      sels.add(regs[0])
      window.run_command("slurp_find_string")
      sels.add_all(regs[1:])
   else:
      window.run_command("slurp_find_string")

   # re-open panel to re-apply the whole_word setting, but lose in_selection
   window.run_command("show_panel", {"panel": "find", "reverse": False})
   window.run_command("hide_panel")


def find(window, forward, all, additive, skip):
   view = window.active_view()
   sels = view.sel()
   last_index = -1 if forward else 0

   # find all matches
   if all:
      window.run_command("find_all")

   # find next match
   elif not additive:
      if forward:
         window.run_command("find_next")
      else:
         window.run_command("find_prev")

   # find next additive match
   else:
      # the selections from a previous find are kept to detect if we're still
      # adding to them. the last added selection is kept to know where to
      # search next (needed because of wrap around setting)
      global last_sels
      global last_sel

      # reset state when current selections don't match last run's
      regs = list(sels)
      if last_sel is None or last_sels != regs:
         last_sels = regs
         last_sel = sels[last_index]

      if skip:
         skip_sel = last_sel

      # we keep searching until we hit the first match (full circle) or selections
      # don't change (no match), while skipping everything already matched.
      # we can't jump to the first/last match because selections in between may
      # have been skipped
      start_sel = last_sel
      while True:
         sels.clear()
         sels.add(last_sel)
         if forward:
            window.run_command("find_next")
         else:
            window.run_command("find_prev")
         last_last_sel = last_sel
         last_sel = sels[0]
         if last_sel == start_sel:
            break
         if last_last_sel == last_sel:
            break
         if last_sel not in last_sels:
            break
      sels.add_all(regs)

      # remove last selection and find next
      if skip:
         # if everything is matched, skip the last added selection, and mark
         # the one before it as last
         if last_sel == start_sel:
            sels.subtract(sels[last_index])
            if len(sels):
               last_sel = sels[last_index]
         else:
            sels.subtract(skip_sel)

      # remember current selections
      last_sels = list(sels)


def replace(window, forward, all):
   if all:
      window.run_command("replace_all")
   elif forward:
      window.run_command("replace_next")
   else:
      window.run_command("replace_next")
      window.run_command("find", {"forward": False})


def find_replace(window, replace_match=False, forward=True, expand=False, under=None, additive=False, skip=False, all=False, open_panel=False, panel=None, close_panel=False):
   view = window.active_view()
   sels = view.sel()
   settings = view.settings()

   last_index = -1 if forward else 0
   find_selected = settings.get("find_selected_text")
   auto_in_selection = settings.get("auto_find_in_selection")
   active_panel = window.active_panel()
   was_find_panel_open = active_panel in ("find", "replace", "find_in_files", "incremental_find")

   # if not additive, clear all but last selection
   if not replace_match and not additive and len(sels) > 1:
      sel = sels[last_index]
      sels.clear()
      sels.add(sel)

   # find_selected_text slurps the last added selection, which breaks additive
   # find in reverse direction. this is solved by always disabling the setting,
   # and using either the passed value or the setting value for under parameter
   if find_selected:
      settings.set("find_selected_text", False)

   if under is None:
      under = not was_find_panel_open and find_selected
      if auto_in_selection and not was_find_panel_open:
         sel = sels[last_index]
         row1, col = view.rowcol(sel.a)
         row2, col = view.rowcol(sel.b)
         if row1 != row2:
            under = False

   if panel not in ("find", "replace", "find_in_files", "incremental_find"):
      panel = "replace" if replace else "find"

   # don't open if closing panel
   if open_panel and close_panel:
      open_panel = False

   # don't reopen same panel to preserve in_selection
   if open_panel and panel == active_panel:
      open_panel = False

   expanded = False

   # expand empty selections
   if expand:
      expanded = expand_empty_sels(view)

   # copy current selection to panel find input
   if under:
      slurp_find_string(window, additive, forward)

   # show find panel
   if open_panel:
      window.run_command("show_panel", {"panel": panel, "reverse": False})

   # perform find or replace unless selections expanded or panel just shown
   if not expanded and not (open_panel and not was_find_panel_open):
      if replace_match:
         replace(window, forward, all)
      else:
         find(window, forward, all, additive, skip)

   # open/restore panel and settings
   if find_selected:
      settings.set("find_selected_text", True)

   if active_panel and not open_panel and under:
      window.run_command("show_panel", {"panel": active_panel, "reverse": False})
   if close_panel:
      window.run_command("hide_panel")


class Find(TextCommand):
   """
   Wrapper around find_next, find_prev and find_all commands that makes them
   always respect whole word and case sensitive settings, regardless of initial
   selection or panel having focus or not.

   It is a TextCommand because of selection modifications but always operates
   on the active view (does not work in panels) due to find_next, find_prev and
   find_all limitations.

   Parameters:
      forward - move towards end or beginning of buffer
      expand - expand empty selections before searching
      under - set current selection as find string in panel
      additive - keep existing selections when finding
      skip - remove last added selection and find next
      all - find all matches
      open_panel - show panel unless already shown
      panel - find panel open_panel will show
      close_panel - close panel after finding
   """

   def run(self, edit, **args):
      window = self.view.window()
      find_replace(window, replace_match=False, **args)


class Replace(TextCommand):
   """
   Wrapper around replace_next and replace_all commands that makes them always
   respect whole word and case sensitive settings, regardless of initial selection
   or panel having focus or not.

   It is a TextCommand because of selection modifications but always operates
   on the active view (does not work in panels) due to replace_next and
   replace_all limitations.

   Parameters:
      forward - move towards end or beginning of buffer
      expand - expand empty selections before replacing
      under - set current selection as find string in panel
      all - replace all matches
      open_panel - show panel unless already shown
      panel - find panel open_panel will show
      close_panel - close panel after replacing
   """

   def run(self, edit, **args):
      window = self.view.window()
      find_replace(window, replace_match=True, **args)
