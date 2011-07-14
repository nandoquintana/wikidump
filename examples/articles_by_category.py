import sys
import logging
import optparse
import csv

logger = logging.getLogger('wikidump')

sys.path.append('../src/')
from wikidump.utils import load_dumps, find_dumps
from wikidump.model import Dump

from wikidump.lang import category_identifier 

def main():
  logging.basicConfig(level=logging.DEBUG)
  if len(sys.argv) < 2:
    logger.error("Must specify language prefix")
    sys.exit(-1)

  # Dump category distribution
  parser = optparse.OptionParser()
  parser.add_option("-l", "--language", dest="lang", help="Relevant language prefix")
  parser.add_option("-o", "--output", dest="output", help="Output format: csv or yaml")
  options, args = parser.parse_args(sys.argv[1:])

  dump = load_dumps([options.lang], build_index=True)[options.lang]
  cats = dump.categories
  get_page = dump.get_page_by_index

  cat_spacename = category_identifier[options.lang]

  if options.output == 'csv':
    writer = csv.writer(sys.stdout,quoting=csv.QUOTE_ALL)
    for c in sorted(cats, key=lambda x:len(cats[x]), reverse=True):
      for a in cats[c]:
        title = get_page(a).title
        if title.find(cat_spacename) == -1:
          writer.writerow((c, title))
  
  else:
    for c in sorted(cats, key=lambda x:len(cats[x]), reverse=True):
      print "%s:" % (c)
      print "# %d articles" % (len(cats[c]))
      for a in cats[c]:
        title = get_page(a).title
        if title.find(cat_spacename) == -1:
          print "- %s" %( get_page(a).title )

main()
