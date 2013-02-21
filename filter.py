import sublime
import sublime_plugin
 
import os

def matches(needle, haystack, is_re):
    if is_re:
        return re.match(needle, haystack)
    else:
        return (needle in haystack)
 
def filter(eview, edit, needle, is_re = False):
    # get non-empty selections
    regions = [s for s in eview.sel() if not s.empty()]
    # if there's no non-empty selection, filter the whole document
    if len(regions) == 0:
        regions = [ sublime.Region(0, eview.size()) ]
    for region in reversed(regions):
        lines = eview.split_by_newlines(region)
        for line in reversed(lines):
            if not matches(needle, eview.substr(line), is_re):
                eview.erase(edit, eview.full_line(line))

class FilterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def done(needle):
            cname = os.path.basename(sublime.active_window().active_view().file_name())
            ffile = open(self.view.file_name())
            template = ffile.read()
            ffile.close()
 
            nwin = sublime.active_window().new_file()
            nwin.set_scratch(True)
            nwin.set_name("Filter from " + cname)
            nwin.run_command("insert_snippet", {"contents": template})
            edit = nwin.begin_edit()
            filter (nwin, edit, needle)
            nwin.end_edit(edit)
        # Get selected text
        for selection in self.view.sel():
            # if the user didn't select anything, search the currently highlighted word
            if selection.empty():
                text = self.view.word(selection)
            text = self.view.substr(selection)
 
        sublime.active_window().show_input_panel("Filter file for lines containing: ", text, done, None, None)

