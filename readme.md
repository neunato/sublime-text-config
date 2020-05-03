### Installation

1. Install [Package Control](https://packagecontrol.io/installation)
2. Run `git clone https://github.com/independentgeorge/sublime-text-config {DATA DIRECTORY}/Packages/User`
3. Open Sublime Text
4. Run `git reset --hard`


### Additions

Setting | Description
------- | -----------
<a name="_auto_convert_indentation"></a>[**`_auto_convert_indentation`**][_auto_convert_indentation] | Reflect user's indentation settings in open files automatically. See [`convert_indentation`](#convert_indentation)
<a name="_trim_file_on_save"></a>[**`_trim_file_on_save`**][_trim_file_on_save] | Remove leading and trailing whitespace from a file when saving it. See [`trim_file`](#trim_file)


Command | Args | Description
------- | ---- | -----------
<a name="convert_indentation"></a>[**`convert_indentation`**][convert_indentation] |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Convert indentation to reflect the user's settings. See [`_auto_convert_indentation`](#_auto_convert_indentation)
<a name="trim_file"></a>[**`trim_file`**][trim_file] | | Remove leading and trailing whitespace from a file. See [`_trim_file_on_save`](#_trim_file_on_save)
<a name="toggle_fold_by_level"></a>[**`toggle_fold_by_level`**][toggle_fold_by_level] | `level` : `int` | Fold/unfold regions of given indentation level. If folded regions exist they are unfolded, else code is folded.
<a name="unfold_by_level"></a>[**`unfold_by_level`**][unfold_by_level] | `level` : `int` | Unfold regions of given indentation level.
<a name="toggle_case"></a>[**`toggle_case`**][toggle_case] | | Swap case of characters in selection based on first non-whitespace character. Work on word if selection is empty.
<a name="next_view_in_group"></a>[**`next_view_in_group`**][next_view_in_group] | | Select the next neighbouring file within group.
<a name="prev_view_in_group"></a>[**`prev_view_in_group`**][prev_view_in_group] | | Select the previous neighbouring file within group.
<a name="unselect_lines"></a>[**`unselect_lines`**][unselect_lines] | `forward` : `bool` | Remove first or last selection based on `forward`.
<a name="expand_selection_to_paragraph_sub"></a>[**`expand_selection_to_paragraph_sub`**][expand_selection_to_paragraph_sub] | | Subtract paragraph enclosing the mouse position from selection.
<a name="set_find_string"></a>[**`set_find_string`**][set_find_string] | `string` : `str` | Set `string` as "find" input field of find panels.
<a name="set_replace_string"></a>[**`set_replace_string`**][set_replace_string] | `string` : `str` | Set `string` as "replace" input field of find panels.
<a name="toggle_regex_ext"></a>[**`toggle_regex_ext`**][toggle_regex_ext] | | Run `toggle_regex` regardless of find panels being open, and make it trigger command listeners.
<a name="toggle_case_sensitive_ext"></a>[**`toggle_case_sensitive_ext`**][toggle_case_sensitive_ext] | | Run `toggle_case_sensitive` regardless of find panels being open, and make it trigger command listeners.
<a name="toggle_whole_word_ext"></a>[**`toggle_whole_word_ext`**][toggle_whole_word_ext] | | Run `toggle_whole_word` regardless of find panels being open, and make it trigger command listeners.


### Modifications

Command | Args | Description
------- | ---- | -----------
<a name="extend_show_panel"></a>[**`show_panel`**][extend_show_panel] | `panel` : `str` <br> `reverse` : `bool` <br> `toggle` : `bool` | Close active panel regardless of focus when `toggle` is on.
<a name="extend_single_selection"></a>[**`single_selection`**][extend_single_selection] | `reverse` : `bool` | Add `reverse` parameter to control whether first or last selection will remain.
<a name="join_lines"></a>[**`join_lines`**][join_lines] |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Remove extra whitespace from single-line selections.
<a name="split_selection_into_lines"></a>[**`split_selection_into_lines`**][split_selection_into_lines] | | Split single-line selections into characters.
<a name="set_layout"></a>[**`set_layout`**][set_layout] | `rows` : `[int]` <br> `cols` : `[int]` <br> `cells` : `[[int]]` | Move active and all tabs to the right to the newly created group, if any.
<a name="close_others_by_index"></a>[**`close_others_by_index`**][close_others_by_index] | `group` : `int` <br> `index` : `int` | Run on active view if called without parameters. Needed for binding to a key.
<a name="close_to_right_by_index"></a>[**`close_to_right_by_index`**][close_to_right_by_index] | `group` : `int` <br> `index` : `int` | Run on active view if called without parameters. Needed for binding to a key.


[convert_indentation]: ./plugin_convert_indentation.py "View source"
[_auto_convert_indentation]: ./plugin_convert_indentation.py "View source"
[trim_file]: ./plugin_trim_file.py "View source"
[_trim_file_on_save]: ./plugin_trim_file.py "View source"
[toggle_fold_by_level]: ./plugin_toggle_fold_by_level.py "View source"
[unfold_by_level]: ./plugin_toggle_fold_by_level.py "View source"
[toggle_case]: ./plugin_toggle_case.py "View source"
[next_view_in_group]: ./plugin_switch_view_in_group.py "View source"
[prev_view_in_group]: ./plugin_switch_view_in_group.py "View source"
[unselect_lines]: ./plugin_unselect_lines.py "View source"
[expand_selection_to_paragraph_sub]: ./plugin_expand_selection_to_paragraph_sub.py "View source"
[set_find_string]: ./plugin_set_find_string.py "View source"
[set_replace_string]: ./plugin_set_find_string.py "View source"
[extend_show_panel]: ./plugin_extend_show_panel.py "View source"
[extend_single_selection]: ./plugin_extend_single_selection.py "View source"
[toggle_regex_ext]: ./plugin_extend_toggle_find_setting.py "View source"
[toggle_case_sensitive_ext]: ./plugin_extend_toggle_find_setting.py "View source"
[toggle_whole_word_ext]: ./plugin_extend_toggle_find_setting.py "View source"
[join_lines]: ./plugin_extend_join_lines.py "View source"
[split_selection_into_lines]: ./plugin_extend_split_selection_into_lines.py "View source"
[set_layout]: ./plugin_extend_set_layout.py "View source"
[close_others_by_index]: ./plugin_extend_close_others_by_index.py "View source"
[close_to_right_by_index]: ./plugin_extend_close_others_by_index.py "View source"
