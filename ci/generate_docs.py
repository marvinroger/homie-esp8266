#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib
import urllib2
import tempfile
import zipfile
import glob
import subprocess
import getopt
import sys
import shutil

FIRST_RELEASE_ID=3084382

output_dir = getopt.getopt(sys.argv[1:], 'o:')[0][0][1]
github_releases = json.load(urllib2.urlopen('https://api.github.com/repos/marvinroger/homie-esp8266/releases'))

for release in github_releases:
  if (release['id'] < FIRST_RELEASE_ID): continue

  tag_name = release['tag_name']
  version = tag_name[1:]
  zip_url = 'https://github.com/marvinroger/homie-esp8266/archive/' + tag_name + '.zip'
  zip_path = tempfile.mkstemp()[1]
  urllib.urlretrieve(zip_url, zip_path)

  zip_file = zipfile.ZipFile(zip_path, 'r')
  unzip_path = tempfile.mkdtemp()
  zip_file.extractall(unzip_path)
  src_path = glob.glob(unzip_path + '/*')[0]

  subprocess.call(['docker', 'run', '--rm', '-it', '-p', '8000:8000', '-v', src_path + ':/docs', 'squidfunk/mkdocs-material', 'build'])
  shutil.copytree(src_path + '/site', output_dir + '/' + version)
