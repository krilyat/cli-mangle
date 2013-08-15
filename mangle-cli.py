import shutil
import sys
import os
import getopt
import logging as log

from mangle.book import Book
import mangle.cbz
import mangle.image

#log.basicConfig(level='DEBUG')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:t:o:e:x')
except getopt.GetoptError, err:
    print str(err)
    sys.exit(2)

directory = '.'
extension = 'zip'
book = Book()
book.device = 'Kindle 5'
book.outputFormat = 'CBZ only'
book.title = 'Unknown'
book.overwrite = False
book.imageFlags = (mangle.image.ImageFlags.Orient |
                   mangle.image.ImageFlags.Resize)


for o, a in opts:
    if o == '-d':
        directory = a
    elif o == '-t':
        book.title = a
    elif o == '-o':
        book.outputFormat = a
    elif o == '-e':
        extension = a
    elif o == '-x':
        book.overwrite = True

bookPath = os.path.join(directory, book.title)

archive = mangle.cbz.Archive(bookPath, extension)
print "Creating %s" % archive.outputPath
if not os.path.isdir(bookPath):
    os.makedirs(bookPath)

log.info('Found %d image files.' % len(args))
for index in range(0, len(args)):
    target = os.path.join(bookPath, '%05d.jpg' % index)
    log.info('Converting file : %s' % args[index])

    mangle.image.convertImage(args[index], target, str(book.device),
                              book.imageFlags)
    archive.addFile(target)
    log.info('... OK')


if 'Image' not in book.outputFormat:
    shutil.rmtree(bookPath)

archive.close()
