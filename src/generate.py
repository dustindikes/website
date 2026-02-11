#!/home/dustin/my-venv/bin/python3

import datetime
import html
import markdown
import os

#####
# TODO
# Auto copy and optimize images
# Generate RSS feed
#####

MD_SRC = '/home/dustin/Codex/Website/'
HTML_OUT = '/home/dustin/Projects/website/'

header_file = open('template/header.html')
HEADER = header_file.read()
header_file.close()

footer_file = open('template/footer.html')
FOOTER = footer_file.read()
footer_file.close()

def xmlStart(title, desc, feed):
    xmlOutput = '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1" xmlns:content="http://purl.org/rss/1.0/modules/content">\n'
    xmlOutput += '  <channel>\n'
    xmlOutput += '    <title>Dustin Dikes - ' + title + '</title>\n'
    xmlOutput += '    <link>https://dustindikes.com/' + feed + '</link>\n'
    xmlOutput += '    <description>' + desc + '</description>\n'
    xmlOutput += '    <language>en-us</language>\n'
    xmlOutput += '    <atom:link href="https://dustindikes.com/' + feed + '.xml" rel="self" type="application/rss+xml" />\n'
    return xmlOutput

def genXmlItem(line, feed):
    ln = line.strip()
    pg = ln.split(' -> ')
    tsp = pg[0].split(' | ')
    title = tsp[1]
    pubdate = tsp[0]
    d = datetime.datetime.strptime(pubdate, '%Y-%m-%d')
    src_file = MD_SRC + title + '.md'
    htmlText = genMarkdown(src_file, True)

    xmlOutput = '      <item>\n'
    xmlOutput += '        <title>' + title + '</title>\n'
    xmlOutput += '        <link>https://dustindikes.com/' + feed + '/' + pg[1] + '.html</link>\n'
    xmlOutput += '        <guid>https://dustindikes.com/' + feed + '/' + pg[1] + '.html</guid>\n'
    xmlOutput += '        <dc:creator>Dustin Dikes</dc:creator>\n'
    xmlOutput += '        <pubDate>' + d.strftime("%a, %d %b %Y %H:%M:%S") + '</pubDate>\n'
    xmlOutput += '        <description><![CDATA[' + htmlText + ']]></description>\n'
    xmlOutput += '        <content:encoded>' + html.escape(htmlText) + '</content:encoded>\n'
    xmlOutput += '      </item>\n'
    return xmlOutput

def xmlEnd():
    xmlOutput = '  </channel>\n'
    xmlOutput += '</rss>'
    return xmlOutput

def genMarkdown(src, absolutePath):
    url = ''
    if absolutePath:
        url = 'https://dustindikes.com'
    md_file = open(src)
    md = md_file.read()
    md = md.replace('[[','[]('+url+'/assets/img/').replace(']]',')')
    md_file.close()
    htmlText = markdown.markdown(md)
    return htmlText

def genPage(line, blog, weeknotes):
    ln = line.strip()
    pg = ln.split(' -> ')

    print('[+] ' + ln)

    title = pg[0]
    pubdate = ''
    if blog or weeknotes:
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

    if weeknotes:
        out_file = HTML_OUT + 'weeknotes/' + pg[1] + '.html'
    elif title == 'Week Notes':
        out_file = HTML_OUT + 'weeknotes/index.html'

    title_html = '<h1>' + title + '</h1>'

    if title == 'Resume':
        title_html = ''

    new_header = HEADER
    new_header = new_header.replace('[TITLE]',title)
    new_header = new_header.replace('[ACTIVE_ABOUT]',' class="active"' if title == 'About' else '')
    new_header = new_header.replace('[ACTIVE_BLOG]',' class="active"' if title == 'Blog' or blog else '')
    new_header = new_header.replace('[ACTIVE_WEEKNOTES]',' class="active"' if title == 'Week Notes' or weeknotes else '')
    new_header = new_header.replace('[ACTIVE_RESUME]',' class="active"' if title == 'Resume' else '')
    new_header = new_header.replace('[ACTIVE_FEEDS]',' class="active"' if title == 'Feeds' else '')

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

    if title == 'Week Notes':
        file = open('weeknotes.txt', 'r')
        lines = reversed(file.readlines())
        bloglist += '<ul id="bloglist">'
        for line in lines:
            sp = line.strip().split(' -> ')
            tsp = sp[0].split(' | ')
            bloglist += '<li>'
            bloglist += '<span>' + tsp[0] + '</span> '
            bloglist += '<a href="/weeknotes/' + sp[1] + '.html">'
            bloglist += tsp[1]
            bloglist += '</a>'
        bloglist += '</ul>'
        file.close()

    htmlText = new_header
    htmlText += '<article id="' + page_id + '">'
    htmlText += title_html

    if pubdate != '':
        htmlText += '<p id="pubdate"><em>' + pubdate + '</em></p>'

    if len(bloglist) > 0:
        htmlText += bloglist
    else:
        htmlText += genMarkdown(src_file, False)

    htmlText += '</article>'
    htmlText += FOOTER

    with open(out_file, 'w') as f:
        f.write(htmlText)


    print('    ' + src_file)
    print('    ' + out_file)
    print('    ' + title)

# PAGES
print()
print('[*] PAGES')
file = open('pages.txt', 'r')
for line in file:
    genPage(line, False, False)
file.close()


# BLOG
print()
print('[*] BLOG')
genPage('Blog -> blog', False, False)
file = open('blog.txt', 'r')
xml = xmlStart('Blog', 'Blog posts related to security, OSINT, bug bounty, CTFs, etc', 'blog')
for line in file:
    genPage(line, True, False)
    xml += genXmlItem(line, 'blog')
xml += xmlEnd()
file.close()
with open(HTML_OUT + 'blog.xml', 'w') as f:
    f.write(xml)

# WEEK NOTES 
print()
print('[*] WEEK NOTES')
genPage('Week Notes -> weeknotes', False, False)
file = open('weeknotes.txt', 'r')
xml = xmlStart('Week Notes', 'Updates of the things I have done each week', 'weeknotes')
for line in file:
    genPage(line, False, True)
    xml += genXmlItem(line, 'weeknotes')
xml += xmlEnd()
file.close()
with open(HTML_OUT + 'weeknotes.xml', 'w') as f:
    f.write(xml)
