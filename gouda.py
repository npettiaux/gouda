#!/usr/bin/env python
#
# Gouda -- a particularly easy-to-use documentation processing tool.
#
# Copyright 2011, 2012, John M. Gabriele <jmg3000@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# ======================================================================
import sys, os, os.path
import commands
import glob
import re

VERSION = '2012.05.07'

HEAD_INCL_FILENAME = '/tmp/head-incl.html'

# ======================================================================
def check_for_toc_conf():
    if not os.path.exists('toc.conf'):
        print "Didn't find a toc.conf file. Creating one ..."
        files_here = glob.glob('*.txt')
        files_here.remove('index.txt')
        if 'toc.txt' in files_here:
            files_here.remove('toc.txt')
        toc_conf_file = open('toc.conf', 'w')
        counter = 0
        for filename in files_here:
            this_file = open(filename)
            top_line = this_file.readline()
            this_file.close()
            if not top_line.startswith('% '):
                print "Error. Please make sure \"%s\" has a correct" % filename
                print "Pandoc-style title block at the top. That is, the first"
                print "line of the file should look something like: \"% My Title\""
                print "Exiting."
                toc_conf_file.close()
                os.unlink('toc.conf')
                sys.exit(1)
            this_title = re.sub(r'^%\s+', '', top_line)
            # Still has the newline, so we just write it.
            counter += 1
            toc_conf_file.write(str(counter) + ':' + filename + ':' + this_title)
        toc_conf_file.close()
    else:
        print "Found toc.conf file here. No need to generate one."

# ----------------------------------------------------------------------
def check_for_styles_css_file():
    some_default_css = '''/* Default css for Gouda doc processor. John Gabriele, */
/* with some help from <http://colorschemedesigner.com/>. */

body {
    background-color: #bbb;
    color: #2a2a2a;
}

#my-header, .nav, #footer {
    font-family: 'Pontano Sans', sans-serif;
}

#my-header {
    background-color: #cb7833;
    color: #eee;
    font-size: 2em;
    text-shadow: 1px 1px 2px #444;
    padding: 10px;
    border-top: 1px solid #bb6823;
    border-left: 1px solid #bb6823;
    border-right: 1px solid #bb6823;
}

.nav {
    font-size: small;
    background-color: #e1a877;
    padding-top: 4px;
    padding-bottom: 4px;
    padding-left: 10px;
    border-top: 1px solid #d19867;
    border-left: 1px solid #d19867;
    border-right: 1px solid #d19867;
}

#footer {
    background-color: #e1a877;
    font-size: small;
    font-style: italic;
    text-align: right;
    padding: 10px;
    border-bottom: 1px solid #d19867;
    border-left: 1px solid #d19867;
    border-right: 1px solid #d19867;
}

#main-box {
    background-color: #f8f8f8;
    font-family: 'Esteban', serif;
    padding-top: 1px;
    padding-left: 14px;
    padding-right: 14px;
    padding-bottom: 14px;
    border-left: 1px solid #aaa;
    border-right: 1px solid #aaa;
}

/* For Pandoc version < 1.9 */
.title {
    display: none;
}

#header {
    display: none;
}

caption {
    font-style: italic;
    font-size: small;
    color: #555;
}

a:link {
    color: #3A4089;
}

a:visited {
    color: #875098;
}

table {
    background-color: #eee;
    padding-left: 2px;
    border: 2px solid #d4d4d4;
    border-collapse: collapse;
}

th {
    background-color: #d4d4d4;
    padding-right: 4px;
}

tr, td, th {
    border: 2px solid #d4d4d4;
    padding-left: 4px;
    padding-left: 4px;
}

dt {
    font-weight: bold;
}

pre {
    border: 1px solid #ddd;
    background-color: #eee;
    padding-left: 6px;
    padding-right: 2px;
    padding-bottom: 5px;
    padding-top: 5px;
}

blockquote {
    color: #3a3a3a;
    background-color: #cde;
    border: 1px solid #bcd;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 16px;
    padding-right: 16px;
}

h1 {
    font-size: 1.8em;
}

h1,h2,h3,h4,h5,h6 {
    font-family: 'Pontano Sans', sans-serif;
}

h3, h5 {
    font-style: italic;
}
'''
    if not os.path.exists('styles.css'):
        print "Didn't find a styles.css file. Creating a default one ..."
        print "(Feel free to edit it later.)"
        css_file = open('styles.css', 'w')
        css_file.write(some_default_css)
        css_file.close()
    else:
        print "Found styles.css file here. No need to create a default one."


# ----------------------------------------------------------------------
def get_list_of_files_in_toc_conf():
    files_in_toc = []
    toc_conf_file = open('toc.conf')
    all_lines = toc_conf_file.readlines()
    toc_conf_file.close()
    for line in all_lines:
        if line == '\n':
            print "Error. Please remove any extra blank lines from your toc.conf file."
            print "Exiting."
            sys.exit(1)

        if ':' not in line:
            print "The following line in your toc.conf file doesn't look right:"
            print "    %s" % line
            print "Please fix (or delete toc.conf to start fresh)."
            print "Exiting."
            sys.exit(1)

        filename = line.split(':')[1]

        if filename == 'toc.txt':
            print "Please remove \"toc.txt\" from your toc.conf file."
            print "Exiting."
            sys.exit(1)

        if filename == 'index.txt':
            print "Please remove \"index.txt\" from your toc.conf file."
            print "Exiting."
            sys.exit(1)

        files_in_toc.append(filename)

    return files_in_toc

# ----------------------------------------------------------------------
def check_if_toc_conf_agrees_with_whats_here():
    files_here_now_sans_index = glob.glob('*.txt')
    files_here_now_sans_index.remove('index.txt')
    if 'toc.txt' in files_here_now_sans_index:
        files_here_now_sans_index.remove('toc.txt')

    # While we're here, may as well check this. But really, if we're
    # doing this, we should probably have something more complete. TODO
    for filename in files_here_now_sans_index:
        if ' ' in filename:
            print "Error: filename \"%s\" has one or more" % filename
            print "spaces in it. Please use underscores or dashes"
            print "instead."
            print "Exiting."
            sys.exit(1)

    files_in_toc = get_list_of_files_in_toc_conf()

    here_but_not_in_toc = set(files_here_now_sans_index).difference(set(files_in_toc))
    if here_but_not_in_toc:
        print "Error. Files found here that aren't in the toc.conf file:"
        for filename in here_but_not_in_toc:
            print "    %s" % filename
        print "The filenames listed in toc.conf should match with the \".txt\" files"
        print "here. (You can delete your toc.conf file and let this script generate"
        print "a new one for you, if you like.)"
        print "Exiting."
        sys.exit(1)

    in_toc_but_not_here = set(files_in_toc).difference(set(files_here_now_sans_index))
    if in_toc_but_not_here:
        print "Error. Files found in toc.conf file but not in this directory:"
        for filename in in_toc_but_not_here:
            print "    %s" % filename
        print "The filenames listed in toc.conf should match with the \".txt\" files"
        print "here. (You can delete your toc.conf file and let this script generate"
        print "a new one for you, if you like.)"
        print "Exiting."
        sys.exit(1)

# ----------------------------------------------------------------------
def check_toc_conf_numbers():
    """Checks that numbers in toc.conf file start at 1 and are
       sequential."""
    toc_conf_lines = open('toc.conf').readlines()
    nums = []
    for line in toc_conf_lines:
        num = line.split(':')[0]
        nums.append(num)

    nums = [int(n) for n in nums]
    if nums[0] != 1:
        print "Error: The chapter numbers in your toc.conf should"
        print "start with 1."
        print "Exiting."
        sys.exit(1)

    nice_nums = range(1, len(nums)+1)
    if nums != nice_nums:
        print "Error: Please make sure the chapter numbers in your"
        print "toc.conf file are sequential."
        print "Exiting."
        sys.exit(1)


# ----------------------------------------------------------------------
def create_toc_txt_file():
    lines_in_toc_conf = open('toc.conf').readlines()
    toc_txt_file = open('toc.txt', 'w')
    toc_txt_file.write('''% Table of Contents

''')

    for line in lines_in_toc_conf:
        chapter_number, filename, title = line.split(':', 2)
        title = title.strip()
        filename = filename[:-3] + 'html'
        toc_txt_file.write("%s. [%s](%s)\n" % (chapter_number, title, filename))

    toc_txt_file.close()


# ----------------------------------------------------------------------
def get_doc_project_name():
    doc_project_name = open('index.txt').readline().strip()
    if not doc_project_name.startswith('% '):
        print "Error. Please make sure index.txt has a correct Pandoc-"
        print "style title block at the top. That is, the first line"
        print "of the file should look something like \"% My Title\"."
        print "Exiting."
        sys.exit(1)

    doc_project_name = re.sub(r'^%\s+', '', doc_project_name)
    if doc_project_name == '':
        print "Error. Please provide a title in your index.txt file."
        print "Exiting."
        sys.exit(1)

    return doc_project_name


# ----------------------------------------------------------------------
def is_this_file_more_recent_than_these(this_file, these_files):
    it_is_more_recent = False
    this_file_mtime = os.path.getmtime(this_file)
    these_files_mtimes = [os.path.getmtime(fn) for fn in these_files]
    for other_mtime in these_files_mtimes:
        if this_file_mtime > other_mtime:
            it_is_more_recent = True
    return it_is_more_recent


# ----------------------------------------------------------------------
def create_html_head_inclusion():
    html_to_include = '''<link href='http://fonts.googleapis.com/css?family=Pontano+Sans' rel='stylesheet' type='text/css'>
<link href='http://fonts.googleapis.com/css?family=Esteban' rel='stylesheet' type='text/css'>
'''
    head_incl_file = open(HEAD_INCL_FILENAME, 'w')
    head_incl_file.write(html_to_include)
    head_incl_file.close()


# ----------------------------------------------------------------------
def process_files():
    doc_project_name = get_doc_project_name()

    pandoc_idx_toc_command = "pandoc -s       --css=styles.css -S -H %s -B %s -A %s -o %s %s"
    pandoc_command         = "pandoc -s --toc --css=styles.css -S -H %s -B %s -A %s -o %s %s"

    # Recall, these are ordered, so we can always refer
    # back to see what comes before and after a given line.
    toc_conf_lines = open('toc.conf').readlines()

    # Will need these data structures for setting up crosslinks between docs.
    chap_num_for_txtfilename = {}  # keys are txt filenames
    title_for_txtfilename = {}     # keys are txt filenames

    for toc_conf_line in toc_conf_lines:
        chap_num, filename, title = toc_conf_line.split(':', 2)

        chap_num = int(chap_num)

        chap_num_for_txtfilename[filename] = chap_num
        title_for_txtfilename[filename] = title

    # chap_num_for_txtfilename, inverted
    txtfilename_for_chap_num = dict(zip( chap_num_for_txtfilename.values(),
                                         chap_num_for_txtfilename.keys()    ))

    header_html_tmpl = '''
<div class="nav">
{{navigation links}}
</div>
<div id="my-header">{{doc project name}}</div>
<div id="main-box">
{{this page}}
'''
    footer_html_tmpl = '''
</div>
<div class="nav">
{{navigation links}}
</div>
<div id="footer">
<a href="{{this page as text}}">Pandoc-Markdown source for this page</a><br/>
(Docs processed by <a href="http://www.unexpected-vortices.com/sw/gouda/docs/">Gouda</a>.)
</div>
'''
    txt_filenames = chap_num_for_txtfilename.keys()
    txt_filenames.extend(['index.txt', 'toc.txt'])
    
    toc_conf_was_touched = False

    existing_html_files = [tfn[:-3] + 'html' for tfn in txt_filenames]
    existing_html_files = [hf for hf in existing_html_files if os.path.exists(hf)]
    if is_this_file_more_recent_than_these('toc.conf', existing_html_files):
        print "The toc.conf file may have been modified, so all html"
        print "files will be regenerated."
        toc_conf_was_touched = True

    any_files_processed_yet = False
    for txt_filename in txt_filenames:
        nav_html = ''
        if txt_filename == 'index.txt':
            nav_html += '''Main | <a href="toc.html">Table of Contents</a>'''
        elif txt_filename == 'toc.txt':
            nav_html += '''<a href="index.html">Main</a> | Table of Contents'''
        else:
            if chap_num_for_txtfilename[txt_filename] == 1:
                nav_html += '''
                <a href="index.html">Main</a> | <a href="toc.html">Table of Contents</a> |
                <a href="%s"><b>Next:</b> 2. %s</a>
                ''' % (txtfilename_for_chap_num[2][:-3] + 'html',
                       title_for_txtfilename[ txtfilename_for_chap_num[2] ])
            elif chap_num_for_txtfilename[txt_filename] == max(chap_num_for_txtfilename.values()):
                prev_chap_num = chap_num_for_txtfilename[txt_filename] - 1
                prev_title = title_for_txtfilename[ txtfilename_for_chap_num[prev_chap_num] ]
                nav_html += '''
                <a href="index.html">Main</a> | <a href="toc.html">Table of Contents</a> |
                <a href="%s"><b>Prev:</b> %s. %s</a>
                ''' % (txtfilename_for_chap_num[prev_chap_num][:-3] + 'html',
                       prev_chap_num,
                       prev_title)
            else:
                prev_chap_num = chap_num_for_txtfilename[txt_filename] - 1
                prev_title = title_for_txtfilename[ txtfilename_for_chap_num[prev_chap_num] ]
                next_chap_num = chap_num_for_txtfilename[txt_filename] + 1
                next_title = title_for_txtfilename[ txtfilename_for_chap_num[next_chap_num] ]

                prev_html_filename = txtfilename_for_chap_num[prev_chap_num][:-3] + 'html'
                next_html_filename = txtfilename_for_chap_num[next_chap_num][:-3] + 'html'

                nav_html += '''
                <a href="index.html">Main</a> | <a href="toc.html">Table of Contents</a> |
                <a href="%s"><b>Prev:</b> %s. %s</a> |
                <a href="%s"><b>Next:</b> %s. %s</a>
                ''' % (prev_html_filename, prev_chap_num, prev_title,
                       next_html_filename, next_chap_num, next_title)

        # Put that nav html into our header & footer templates.
        header_html = header_html_tmpl.replace('{{navigation links}}', nav_html)
        header_html = header_html.replace('{{doc project name}}', doc_project_name)
        if txt_filename == 'index.txt':
            header_html = header_html.replace('{{this page}}', '')
        elif txt_filename == 'toc.txt':
            header_html = header_html.replace('{{this page}}', '<h1>Table of Contents</h1>')
        else:
            header_html = header_html.replace(
                '{{this page}}',
                '<h1>Chapter '
                + str(chap_num_for_txtfilename[txt_filename])
                + ': '
                + title_for_txtfilename[txt_filename]
                + '</h1>')

        footer_html = footer_html_tmpl.replace('{{navigation links}}', nav_html)
        footer_html = footer_html.replace('{{this page as text}}', txt_filename)

        header_file = open('/tmp/header.html', 'w')
        header_file.write(header_html)
        header_file.close()
        footer_file = open('/tmp/footer.html', 'w')
        footer_file.write(footer_html)
        footer_file.close()

        html_filename = txt_filename[:-3] + 'html'

        if txt_filename == 'index.txt' or txt_filename == 'toc.txt':
            cmd = pandoc_idx_toc_command % (HEAD_INCL_FILENAME,
                                            '/tmp/header.html',
                                            '/tmp/footer.html',
                                            html_filename,
                                            txt_filename)
        else:
            cmd = pandoc_command % (HEAD_INCL_FILENAME,
                                    '/tmp/header.html',
                                    '/tmp/footer.html',
                                    html_filename,
                                    txt_filename)

        if toc_conf_was_touched \
                or not os.path.exists(html_filename) \
                or os.path.getmtime(txt_filename) > os.path.getmtime(html_filename):
            any_files_processed_yet = True
            print "* Processing %s --> %s ..." % (txt_filename, html_filename)
            os.system(cmd)

    if not any_files_processed_yet:
        print "No text files needed processing."


# ======================================================================
# ======================================================================
# Main

if len(sys.argv) != 1:
    print "This tool doesn't take any arguments. Just run"
    print "it in your docs directory and it generates html"
    print "files in there from the \".txt\" files present."
    print "Exiting."
    sys.exit(1)

if not len(glob.glob('*.txt')):
    print "Error. Could not find any \"*.txt\" files here."
    print "Exiting."
    sys.exit(1)

if not os.path.exists('index.txt'):
    print "Error. Could not find an \"index.txt\" file here. Gouda"
    print "won't work without one. Please create one and try again."
    print "Exiting."
    sys.exit(1)

if len(glob.glob('*.txt')) < 3:
    print "Error: Gouda needs at least 2 doc files in addition to the"
    print "index.txt file. Please create another text file here."
    print "Exiting."
    sys.exit(1)

check_for_toc_conf()
check_for_styles_css_file()
check_if_toc_conf_agrees_with_whats_here()
check_toc_conf_numbers()
print "toc.conf file looks good."

if not os.path.exists('toc.txt') \
        or os.path.getmtime('toc.conf') > os.path.getmtime('toc.txt'):
    print "* Generating toc.txt file ..."
    create_toc_txt_file()

create_html_head_inclusion()
process_files()
print "Done."
