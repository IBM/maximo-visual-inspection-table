#! /usr/bin/env python
# IBM_PROLOG_BEGIN_TAG
#
# Copyright 2020 IBM International Business Machines Corp.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#  implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  IBM_PROLOG_END_TAG
# -----------------------------------------------------------

from __future__ import print_function

import argparse
import csv
import json
import logging
import sys
from datetime import datetime

import requests
import base64
cfg = {}
csvResult = {}


# ------------------------------------
# Eases printing to STDERR
def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)


# ------------------------------------
# Checks if result from Vision API succeeded
# (Current API returns failure indication in the JSON body)
def rspOk(rsp):
  logging.debug("status_code: {}, OK={}.".format(rsp.status_code, rsp.ok))

  if rsp.ok:
    try:
      jsonBody = rsp.json()
      if ("result" in jsonBody) and (jsonBody["result"] == "fail"):
        result = False
        logging.info(json.dumps(jsonBody, indent=2))
      else:
        result = True
    except ValueError:
      result = True
      logging.info("good status_code, but no data")
  else:
    result = False

  return result


# ------------------------------------
# local post function to hide common parameters
#
def post(url, **kwargs):
  if "Auth" in cfg:
    authInfo = tuple(cfg["Auth"])
  else:
    authInfo = None
  return requests.post(url, verify=False, auth=authInfo, **kwargs)


def get(url, **kwargs):
  headers = {}
  headers['X-Auth-Token'] = u'%s' % cfg['token']

  return requests.get(url, headers=headers, verify=False, **kwargs)


# -------------------------------------
# sets up the API access
#
def setupAPIAccess(url, user, passwd):
  global cfg
  cfg["url"] = url
  # Disable warning messages about SSL certs
  requests.packages.urllib3.disable_warnings()

  if user is not None and passwd is not None:
    auth = {
      "grant_type": "password",
      "username": user,
      "password": passwd
    }
    logging.info("Setting up auth token")
    resp = requests.post(url + "/api/tokens", verify=False, json=auth)
    respdata = resp.json()
    cfg['token'] = respdata['token']


# -------------------------------------
# parse commandline options -- using argparse
#
# argparse "results" class is returned
#
def getInputs():
  parser = argparse.ArgumentParser(description="Tool to classify all images in a directory")
  parser.add_argument('--dsid', action="store", dest="dsid", required=False,
                      help="(Optional) UUID of a target dataset")
  parser.add_argument('--url', action="store", dest="url", required=True,
                      help="Vision URL eg https://ip/powerai-vision WITHOUT trailing slash or /api")
  parser.add_argument('--output', action="store", dest="output", required=True,
                      help="Output file name eg output.csv")
  parser.add_argument('--user', action="store", dest="user", required=True,
                      help="Username")
  parser.add_argument('--passwd', action="store", dest="passwd", required=True,
                      help="Password")
  parser.add_argument('--showall', action="store_true", dest="showall", required=False,
                      help="(Optional) Show all image data. By default, this tool filters training data.")
  parser.add_argument('--debug', action="store_true", dest="debug", required=False,
                      help="Set Debug logging level")


  try:
    results = parser.parse_args()

  except argparse.ArgumentTypeError as e:
    logging.error(e.args)
    parser.print_help(sys.stderr)
    results = None

  return results

def getDatasets(qparm=None):
  result = None
  url = cfg["url"] + "/api/datasets"
  logging.debug("getDatasets: URL = {}".format(url))
  rsp = get(url)

  if rspOk(rsp):
    result = rsp.json()
  return result

def getFileList(dsId, qparm=None):
  result = None

  url = cfg["url"] + "/api/datasets/" + dsId + "/files"
  if qparm:
    url += "?" + qparm
  logging.debug("getFileList: URL= {}".format(url))
  rsp = get(url)
  if rspOk(rsp):
    result = rsp.json()
  return result


def exportFile(dsId, qparm=None):
  result = None

  url = cfg["url"] + "/api/datasets/" + dsId + "/export"
  if qparm:
    url += "?" + qparm
  logging.debug("exportFile: URL= {}".format(url))
  rsp = get(url)
  if rspOk(rsp):
    f = open('exported_file.zip', 'w+')
    chunk_size = 128
    for chunk in rsp.iter_content(chunk_size=chunk_size):
        f.write(chunk)
    result = rsp.json()
  return result

def getThumbnail(path ,qparm=None):
  result = None

  url = cfg["url"] + '/' + path
  logging.debug("getThumbnail: URL= {}".format(url))
  rsp = get(url, stream=True)
  # if rspOk(rsp):
  try:
    base64_pic = base64.b64encode(rsp.content)
    logging.debug("received thumbnail")
    return base64_pic
  except:
    logging.error("error getting thumbnail")
    return ""

  # return result

# -------------------------------------
# Generate CSV from dictionary
#
def generateCSV(filename, rows, showall=False):

  numrows = 0
  # Generate minimal info CSV
  with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['Thumbnail', 'DataSetID', 'DataSetName', 'Class', 'Score', 'Owner', 'URL', 'Type', 'FormattedDate', 'RawDate', 'TriggerDate', 'TriggerReference', 'TriggerString', 'Project', 'Result',
               'Location', 'Station', 'Type']
    headers.extend(['Metadata%d' % i for i in range(25)])
    writer.writerow(headers)
    # writer.writeheader()
    logging.debug("Parsing data for dataset %s" % rows[0]['datasetid'])
    for row in rows:
      if "___" in row['original_file_name']:
        visinspectdata = row['original_file_name'].split('___')
        print(visinspectdata)
        if len(visinspectdata) > 10:
            classes = visinspectdata[10]
            scores = visinspectdata[11]
            top_class = classes.split('__')[0]
            top_score = scores.split('__')[0]
        else:
            top_class = ""
            top_score = ""
        thumbnail = getThumbnail(row['thumbnail_path'])
        # prepend our URL to deep-link to Vision
        visinspectdata[0:0] = [row['thumbnail'],  row['datasetid'], row['datasetname'], top_class, top_score, row['owner'], row['url']]
        # reformat time to something excel can parse
        try:
          dt = datetime.strptime(visinspectdata[9], "%Y%m%d%H%M%S")
          # insert the formatted date in BEFORE the old date
          visinspectdata[8:8] = [dt.strftime("%Y-%m-%d %H:%M:%S")]
        except ValueError:
          visinspectdata[8:8] = [""]

        if (not showall) and (visinspectdata[7] == "TRAINING"):
          #skip this row since we're filtering out training data
          continue
        # remove the .jpeg appended by Inspector on the very end...
        if '.jpeg' in visinspectdata:
          visinspectdata.remove('.jpeg')
        writer.writerow(visinspectdata)
        numrows += 1
      elif showall:
        # handle cases where we found a user-uploaded image, but only if we're dumping all of the user's data
        writer.writerow([row['url'], 'LABELED'])
        numrows += 1
  return numrows


def dumpinspectordata(dsid=None, user="admin", passwd="passw0rd", url="http://ip/powerai-vision", output="out.csv", showall=False):
  # set up the auth token
  setupAPIAccess(url, user, passwd)
  logging.info("Retrieving global dataset list...")
  datasets = getDatasets()
  if dsid:
    # filter us down to just the dataset we care about
    datasets = [dataset for dataset in datasets if dataset['_id'] == dsid]
  logging.info("Successfully retrieved %d datasets" % len(datasets))
  # holding spot accumulator for all files system-wide
  files = []

  #iterate across all datasets, one-by-one
  for dataset in datasets:
    #get files for this specific dataset
    dsfiles = getFileList(dataset['_id'])
    logging.info("Fetched %7d items in Dataset %s = %s" % (len(dsfiles), dataset['_id'], dataset['name']))
    # create a unique URL and some other book keeping items for this file
    if 'thumbnail_path' in dataset.keys():
        thumbnail = getThumbnail(dataset['thumbnail_path'])
    else:
        thumbnail = ""

    for file in dsfiles:
      file['datasetid'] = dataset['_id']
      file['datasetname'] = dataset['name']
      file['owner'] = dataset['owner']
      file['url'] = url + "/" + "#/datasets/" + dataset['_id'] + "/label?imageId=" + file['_id']
      file['thumbnail'] = str(thumbnail, "utf-8")
      # TODO, values ending up in wrong column
      file['thumbnail_path'] = dataset['thumbnail_path']
    # append this into the master list for csv processing...
    files.extend(dsfiles)

  # output our CSV for additional parsing
  csvname = output
  rowswritten = generateCSV(csvname, files, showall)
  logging.info("Wrote %d rows to %s. We filtered out %d items." % (rowswritten, csvname, len(files) - rowswritten))

if __name__ == '__main__':
  args = getInputs()
  loglevel = logging.DEBUG if args.debug else logging.INFO
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                      datefmt='%H:%M:%S',
                      level=loglevel)

  if args is not None:
    dumpinspectordata(dsid=args.dsid, user=args.user, passwd=args.passwd, url=args.url, output=args.output, showall=args.showall)
  else:
    exit(1)
