
_sampleUrl = 'http://www.kongregate.com/games/mmx95/reach-the-core'


import time, re, os
from urllib import request
import pyperclip

def fail(string):
    print('FAIL: %s' % string)
    return None

def check_clipboard(oldPaste):
    newPaste = pyperclip.paste()
    try:
        #new/old match, do not update old
        if newPaste == oldPaste: return (None, oldPaste)
        # new is kong url, update old
        elif 'kongregate.com' in newPaste: return (newPaste, newPaste)
        # new is useless, update old
        else: return (None, newPaste)
    except: # print('FAIL:') return (None, oldPaste)
        return (fail('check_clipboad'), oldPaste)

def parse_src(pageUrl):

    if not pageUrl.startswith('http:'):
        pageUrl = 'http://www.' + pageUrl[pageUrl.index('kongregate'):]

    print('1) Collecting src: %s' % pageUrl)
    # compile patterns
    rswf  = re.compile('var swf_location = "(.*?version.*?)"')
    rname = re.compile('.*/(.*?swf)')
    rversion = re.compile('version=(\d*)')

    # download src code
    try: text = request.urlopen(pageUrl).read().decode('utf8')
    except: text = fail('parse_src, text')

    # regex url, name, version
    try: url = rswf.search(text).group(1)
    except: url = fail('parse_src, url')
    try: name = rname.search(url).group(1)
    except: name = fail('parse_src, name')
    try: version = rversion.search(url).group(1)
    except: version = fail('parse_src, version')

    return (url, name, version) if (url and name and version) else None

def dl_game(location, url, name, version):
    # setup vars
    fileName = name + ' v' + version + '.swf'
    path = os.path.join(location, fileName)
    print('2) downloading: (%s), %s' % (fileName, url))
    # download file
    try: request.urlretrieve(url, path)
    except: fail('dl_game, %s' % url)

    print('Success: (%s)' %fileName)

if __name__ == '__main__':
    pyperclip.copy('')
    oldClipboard = ''
    print('-%s-'%oldClipboard)
    while True:
        time.sleep(1)
        newClipboard, oldClipboard = check_clipboard(oldClipboard)
        if newClipboard:
            gameData = parse_src(newClipboard)
            if gameData:
                dl_game('c:/_', *gameData)



