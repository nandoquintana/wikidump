import sys
import logging
import optparse

logger = logging.getLogger('wikidump')

sys.path.append('../src/')
from wikidump.utils import load_dumps, find_dumps
from wikidump.model import Dump


def main():
  logging.basicConfig(level=logging.DEBUG)
  if len(sys.argv) < 2:
    logger.error("Must specify language prefix")
    sys.exit(-1)

  # Dump category distribution
  parser = optparse.OptionParser()
  parser.add_option("-l", "--language", dest="lang", help="Relevant language prefix")
  options, args = parser.parse_args(sys.argv[1:])

  dump = load_dumps([options.lang], build_index=True)[options.lang]
  cats = dump.categories
  get_page = dump.get_page_by_index

  for c in sorted(cats, key=lambda x:len(cats[x]), reverse=True):
    print "%d\t%s" % (len(cats[c]), c)
    for a in cats[c]:
      print "\t%s" %( get_page(a).title )

main()
