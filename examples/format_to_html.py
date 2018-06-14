#!/usr/bin/env python
"""
Synopsis:
    Sample program demonstrating use of VOEvent library and Vutil.py.

    Reads a VOEvent file and produces basic HTML rendering.
    See the VOEvent specification for details 
    http://www.ivoa.net/Documents/latest/VOEvent.html
Usage:
    python format_to_html.py [options] input_event_file.xml
Options:
    -h, --help      Display this help message.
    -s, --stdout    Send output to stdout.
    -o FILENAME, --outfile=FILENAME
                    Send output to file.
    -t, --text-string
                    Capture output as a text string, then write to stdout.
    -f, --force     Force: over-write output file without asking.
Examples:
    python format_to_html.py --stdout input_event_file.xml
    python format_to_html.py --file=outfile1.html input_event_file.xml
    python format_to_html.py -s -o outfile2.html input_event_file.xml

"""
# Copyright 2010 Roy D. Williams and Dave Kuhlmann


import sys
import os
import getopt
from VOEventLib import VOEvent
from VOEventLib import Vutil

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


def display(source, o=sys.stdout):
    '''Generate HTML that provides a display of an event.
    '''
    v = Vutil.parse(source)
    print('<html>', file=o)
    print('<h2>VOEvent</h2>', file=o)
    print('IVORN <i>%s</i><br/>' % v.get_ivorn(), file=o)
    print('(role is %s)' % v.get_role(), file=o)

    print('<p>Event description: %s</p>\n' % v.get_Description(), file=o)

    r = v.get_Reference()
    if r:
        print('Reference<br/>Name=%s, Type=%s, uri=%s' \
                    % (r.get_name(), r.get_type(), r.get_uri()), file=o)
    print('<h3>Who</h3>', file=o)
    who = v.get_Who()
    a = who.get_Author()
    print('Title: %s'                        % Vutil.htmlList(a.get_title()), file=o)
    print('Name: %s'                         % Vutil.htmlList(a.get_contactName()), file=o)
    print('Email: %s'                        % Vutil.htmlList(a.get_contactEmail()), file=o)
    print('Phone: %s'                        % Vutil.htmlList(a.get_contactPhone()), file=o)
    print('Contributor: %s<br/>'             % Vutil.htmlList(a.get_contributor()), file=o)
    print('<h3>What</h3>', file=o)
    print('<h4>Params</h4>', file=o)
    print('<table border="1"><tr>', file=o)
    print('<td>Group</td>', file=o)
    print('<td>Name</td>', file=o)
    print('<td>Description</td>', file=o)
    print('<td><b>Value</b></td>', file=o)
    print('<td>ucd</td>', file=o)
    print('<td>unit</td>', file=o)
    print('<td>dataType</td>', file=o)
    print('</tr>', file=o)
    g = None
    params = v.get_What().get_Param()
    for p in params:
        print('<tr>' + Vutil.htmlParam(g, p) + '</tr>', file=o)

    groups = v.get_What().get_Group()
    for g in groups:
        for p in g.get_Param():
            print('<tr>' + Vutil.htmlParam(g, p) + '</tr>', file=o)
    print('</table>', file=o)
    print('<h4>Tables</h4>', file=o)
    tables = v.get_What().get_Table()
    for t in tables:
        print('<table border="1">', file=o)

        print('<tr><td><i>Name</i></td>', file=o)
        for f in t.get_Field():
            print('<td>' + str(f.get_name()) + '</td>', file=o)
        print('</tr>', file=o)

        print('<tr><td><i>UCD</i></td>', file=o)
        for f in t.get_Field():
            print('<td>' + str(f.get_ucd()) + '</td>', file=o)
        print('</tr>', file=o)

        print('<tr><td><i>unit</i></td>', file=o)
        for f in t.get_Field():
            print('<td>' + str(f.get_unit()) + '</td>', file=o)
        print('</tr>', file=o)
        print('<tr><td><i>dataType</i></td>', file=o)
        for f in t.get_Field():
            print('<td>' + str(f.get_dataType()) + '</td>', file=o)
        print('</tr>', file=o)
        print('<tr><td/></tr>', file=o)
        d = t.get_Data()
        if d:
            for tr in d.get_TR():
                print('<tr><td/>', file=o)
                for td in tr.get_TD():
                    print('<td>' + td + '</td>', file=o)
                print('</tr>', file=o)
        print('</table>', file=o)
    print('<h3>WhereWhen</h3>', file=o)
    wwd = Vutil.getWhereWhen(v)
    if wwd:
        print('<table border="1">', file=o)
        print('<tr><td>Observatory</td> <td>%s</td></tr>' % wwd['observatory'], file=o)
        print('<tr><td>Coord system</td><td>%s</td></tr>' % wwd['coord_system'], file=o)
        print('<tr><td>Time</td>                <td>%s</td></tr>' % wwd['time'], file=o)
        print('<tr><td>Time error</td>  <td>%s</td></tr>' % wwd['timeError'], file=o)
        print('<tr><td>RA</td>                  <td>%s</td></tr>' % wwd['longitude'], file=o)
        print('<tr><td>Dec</td>                 <td>%s</td></tr>' % wwd['latitude'], file=o)
        print('<tr><td>Pos error</td>       <td>%s</td></tr>' % wwd['positionalError'], file=o)
        print('</table>', file=o)
    print('<h3>Why</h3>', file=o)
    w = v.get_Why()
    if w:
        if w.get_Concept():
            print("Concept: %s" % Vutil.htmlList(w.get_Concept()), file=o)
        if w.get_Name():
            print("Name: %s"        % Vutil.htmlList(w.get_Name()), file=o)

        print('<h4>Inferences</h4>', file=o)
        inferences = w.get_Inference()
        for i in inferences:
            print('<table border="1">', file=o)
            print('<tr><td>probability</td><td>%s</td></tr>' % i.get_probability(), file=o)
            print('<tr><td>relation</td>     <td>%s</td></tr>' % i.get_relation(), file=o)
            print('<tr><td>Concept</td>      <td>%s</td></tr>' % Vutil.htmlList(i.get_Concept()), file=o)
            print('<tr><td>Description</td><td>%s</td></tr>' % Vutil.htmlList(i.get_Description()), file=o)
            print('<tr><td>Name</td>             <td>%s</td></tr>' % Vutil.htmlList(i.get_Name()), file=o)
            print('<tr><td>Reference</td>  <td>%s</td></tr>' % str(i.get_Reference()), file=o)
            print('</table>', file=o)
    print('<h3>Citations</h3>', file=o)
    cc = v.get_Citations()
    if cc:
        for c in cc.get_EventIVORN():
            print('<ul>', file=o)
            print('<li>%s with a %s</li>' % (c.get_valueOf_(), c.get_cite()), file=o)
            print('</ul>', file=o)
    print('</html>', file=o)


def format_to_stdout(infilename):
    '''Write HTML to standard output.
    '''
    display(infilename)


def format_to_file(infilename, outfilename, force):
    '''Write HTML to a file.
    
    Check for existence of the file.  If it exists,
    write only if force is True.
    '''
    if os.path.exists(outfilename) and not force:
        sys.stderr.write(
            '\nFile %s exists.  Use -f/--force to over-write.\n\n' % (
            outfilename, ))
        sys.exit(1)
    outfile = open(outfilename, 'w')
    display(infilename, outfile)
    outfile.close()


def format_to_string(infilename):
    '''Format as HTML and capture in a string.  Return the string.
    '''
    outfile = StringIO()
    display(infilename, outfile)
    content = outfile.getvalue()
    return content


def usage():
    sys.stderr.write(__doc__)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, 'hso:tf', ['help',
            'stdout', 'outfile=', 'text', 'force' ])
    except:
        usage()
    outfilename = None
    stdout = False
    force = False
    text = False
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-o', '--outfile'):
            outfilename = val
        elif opt in ('-s', '--stdout'):
            stdout = True
        elif opt in ('-t', '--text'):
            text = True
        elif opt in ('-f', '--force'):
            force = True
    if len(args) != 1:
        usage()
    infilename = args[0]
    if stdout:
        format_to_stdout(infilename)
    if outfilename is not None:
        format_to_file(infilename, outfilename, force)
    if text:
        content = format_to_string(infilename)
        print(content)
    if not stdout and outfilename is None and not text:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


