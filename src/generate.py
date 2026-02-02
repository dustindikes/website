#!/home/dustin/my-venv/bin/python3

import markdown
import os

#####
# TODO
# Auto copy and optimize images
# Generate RSS feed
#####

MD_SRC = '/home/dustin/Codex/Website/'
HTML_OUT = '/home/dustin/projects/website/'

header_file = open('template/header.html')
HEADER = header_file.read()
header_file.close()

footer_file = open('template/footer.html')
FOOTER = footer_file.read()
footer_file.close()

def genPage(line, blog):
    ln = line.strip()
    pg = ln.split(' -> ')

    print('[+] ' + ln)

    title = pg[0]
    pubdate = ''
    if blog:
        tsp = title.split(' | ')
        title = tsp[1]
        pubdate = tsp[0]

    page_id = title.replace(' ','_').lower()

    src_file = MD_SRC + title + '.md'
    out_file = HTML_OUT + pg[1] + '.html'

    if blog:
        out_file = HTML_OUT + 'blog/' + pg[1] + '.html'
    elif title == 'Blog':
        out_file = HTML_OUT + 'blog/index.html'

    title_html = '<h1>' + title + '</h1>'

    if title == 'Resume':
        title_html = ''

    new_header = HEADER
    new_header = new_header.replace('[TITLE]',title)
    new_header = new_header.replace('[ACTIVE_ABOUT]',' class="active"' if title == 'About' else '')
    new_header = new_header.replace('[ACTIVE_BLOG]',' class="active"' if title == 'Blog' or blog else '')
    new_header = new_header.replace('[ACTIVE_RESUME]',' class="active"' if title == 'Resume' else '')

    bloglist = ''
    if title == 'Blog':
        file = open('blog.txt', 'r')
        lines = reversed(file.readlines())
        bloglist += '<ul id="bloglist">'
        for line in lines:
            sp = line.strip().split(' -> ')
            tsp = sp[0].split(' | ')
            bloglist += '<li>'
            bloglist += '<span>' + tsp[0] + '</span> '
            bloglist += '<a href="/blog/' + sp[1] + '.html">'
            bloglist += tsp[1]
            bloglist += '</a>'
        bloglist += '</ul>'
        file.close()

    html = new_header
    html += '<article id="' + page_id + '">'
    html += title_html

    if pubdate != '':
        html += '<p id="pubdate"><em>' + pubdate + '</em></p>'

    if len(bloglist) > 0:
        html += bloglist
    else:
        md_file = open(src_file)
        md = md_file.read()

        #![[HTB-LFI-002.png]]

        md = md.replace('[[','[](/assets/img/').replace(']]',')')
        html += markdown.markdown(md)
        md_file.close()

    html += '</article>'
    html += FOOTER

    with open(out_file, 'w') as f:
        f.write(html)


    print('    ' + src_file)
    print('    ' + out_file)
    print('    ' + title)

# PAGES
print()
print('[*] PAGES')
file = open('pages.txt', 'r')
for line in file:
    genPage(line, False)
file.close()


# BLOG
print()
print('[*] BLOG')
genPage('Blog -> blog', False)
file = open('blog.txt', 'r')
for line in file:
    genPage(line, True)
file.close()
