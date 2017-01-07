import copy
from functools import partial
import os
import json


def convert_to_markdown(infile, outfile):
    """Read in JSON, export markdown to be rendered as a website."""
    def get_adder(output, data):
        def add(i, fstring, key):
            if key in data[i] and data[i][key] is not None:
                return fstring.format(data[i][key].strip()) + '\n\n'
            return ''
        return add

    raw = ''
    with open(infile, 'r') as fin:
        raw = ''.join(fin.readlines())
    data = json.loads(raw)

    output = ''
    add_gen = get_adder(output, data)
    for i in range(len(data)):
        add = partial(add_gen, i)
        output += add('# {}', 'title')
        output += add('## {}', 'author')
        output += add('### Posted {}', 'post_date')
        output += add('![]({})', 'image_url')
        output += add('{}', 'content')
#        output += '### Comments\n\n'
#        for comment in data[i]['comments']:
#            output += '- {}\n'.format(comment)
        output += '\n'

    with open(outfile, 'w') as fout:
        fout.write(output)


def convert_to_mds(filenames):
    oldnames = copy.copy(filenames)
    newnames = [filename.split('.')[1] + '.md' for filename in filenames]
    for oldname, newname in zip(oldnames, newnames):
        print('Converting {} to Markdown'.format(oldname))
        convert_to_markdown('data/' + oldname, 'tmp/' + newname)
    return newnames


def convert_mds_to_html(filenames):
    newnames = [x.split('.')[0] + '.html' for x in filenames]
    for oldname, newname in zip(filenames, newnames):
        print('Converting {} to HTML'.format(oldname))
        os.system('pandoc tmp/{} -o tmp/{}'.format(oldname, newname))
    return newnames

def build_index(filenames):
    print('Building Index page')
    output = '# Fake News Sites\n\n'
    for filename in filenames:
        output += '- [{}]({})\n'.format(
            filename.split('.')[0],
            filename,
            )
    with open('tmp/index.md', 'w') as fout:
        fout.write(output)
    os.system('pandoc tmp/index.md -o tmp/index.html')


if __name__ == '__main__':
    filenames = [x for x in os.listdir(os.getcwd() + '/data')
                 if x.endswith('.json')]
    newnames = convert_to_mds(filenames)
    newnames = convert_mds_to_html(newnames)
    build_index(newnames)
