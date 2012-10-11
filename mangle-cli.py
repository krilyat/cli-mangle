#!/usr/bin/env python2.6

import shutil
import sys
import os
import getopt

from mangle.book import Book
import mangle.cbz
import mangle.image

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:t:o:e:')
except getopt.GetoptError, err:
    print str(err)
    sys.exit(2)

directory = '.'
extension = 'cbz'
book = Book()
book.device = 'Kindle 4'
book.outputFormat = 'CBZ only'
book.title = 'Unknown'


for o, a in opts:
    if o == '-d':
        directory = a
    elif o == '-t':
        book.title = a
    elif o == '-o':
        book.outputFormat = a
    elif o == '-e':
        extension = a


bookPath = os.path.join(directory, book.title)

archive = mangle.cbz.Archive(bookPath, extension)

if not os.path.isdir(bookPath):
    os.makedirs(bookPath)

print('Found %d image files.' % len(args))
for index in range(0, len(args)):
    target = os.path.join(bookPath, '%05d.png' % index)
    print ('Converting file : %s' % args[index])

    mangle.image.convertImage(args[index], target, str(book.device),
                              book.imageFlags)
    archive.addFile(target)
    print ('... OK')


if 'Image' not in book.outputFormat:
    shutil.rmtree(bookPath)

archive.close()
