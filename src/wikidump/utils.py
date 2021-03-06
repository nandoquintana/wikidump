import os
import re
import logging

from collections import defaultdict

from config import config
import model
import regexps

logger = logging.getLogger('wikidump.utils')

xml_path = config.get('paths','xml_dumps')

def find_dumps(langs=None, path=xml_path):
  """
  Find dumps existing under a given point in the filesystem.
  Takes an optional argument which specifies the language codes to look for.
  """
  def visit(arg, dirname, names):
    for name in names:
      match = regexps.dumpfile_name.match(name)
      if match:
        arg.append(os.path.join(dirname, name))

  paths = []
  os.path.walk(path, visit, paths)

  dump_paths = {}
  for p in paths:
    match = regexps.dumpfile_name.search(os.path.basename(p))
    if langs is None or match.group('prefix') in langs:
      dump_paths[match.group('prefix')] = p
  return dump_paths

def load_dumps(langs=None, dump_path=None, build_index=False):
  if dump_path is None:
    dump_path = xml_path
  dumps = {}
  paths = find_dumps(langs, dump_path)
  for lang in paths:
    if langs is not None and lang not in langs: continue
    dumps[lang] = model.Dump(paths[lang], build_index=build_index)
  return dumps

def category_map(dump):
  "Compute the category mapping of a particular dump"
  cat_count = defaultdict(list)
  for i in xrange(dump.metadata['size']):
    p = dump.get_page_by_index(i)
    for c in p.categories():
      cat_count[c].append(i)
  return cat_count
