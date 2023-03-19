import urllib3, re, json, sys
if len(sys.argv) != 2:
    print >> sys.stderr, ' '.join([
        'Usage:', sys.argv[0], 'google-form-url > submit.js'])
    sys.exit(1)

def idfromurl(url):
    m = re.match('https?://docs.google.com/forms/d/(.{16}[^/]*)/', url)
    return m and m.group(1)

# Scrape the Google Form.
html = urllib2.urlopen(sys.argv[1]).read()

# If it is a form authoring URL, then it contains a form submission url.
match = re.search(r'<meta itemprop="url" content="([^"]*)"', html)
if match and idfromurl(match.group(1)) != idfromurl(sys.argv[1]):
    # So fetch that page instead.
    html = urllib2.urlopen(match.group(1)).read()

# Extract this special variable value.
match = re.search(
    r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);\s*</script>', html, re.DOTALL)

compressed = match.group(1)

# Fix up JSON-like by replacing ,, with , null,
jstext = re.sub(r'(?<=[,[])\s*,', 'null,', compressed)

# Decode JSON.
js = json.loads(jstext)

# Sometimes the imporant data is the whole array; other times it is
# wrapped as an array inside the first element.
if isinstance(js[0] ,list):
    js = js[0]

# Camel casing, for code generation.
def camel(n):
    names = re.sub(r'\W', ' ', n).split(' ')
    cameled = [names[0].lower()] + [n.title() for n in names[1:]]
    return ''.join(cameled)

# Extract form information from the JSON.
# Tested on 3/29/2016; revised on 1/27/2017 for updated format.
formid = js[14] or js[0]
formname = js[3] or js[1][0]
fname = camel('send ' + formname)
data = js[1][1]
args = [camel(d[1]) for d in data]
nums = [d[4][0][0] for d in data]
