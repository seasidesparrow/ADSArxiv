from __future__ import absolute_import, unicode_literals

#import ADSPipeline
import adsputils

import adi.app as app_module
#from aip.libs import solr_adapter, merger, read_records
from kombu import Queue
from adsmsg import BibRecord, DenormalizedRecord

app = app_module.AdsArxivCelery('arxiv_pipeline')
logger = app.logger

from adi.tasks import task_output_results

class ArxivToMasterPipeline(dict):


    def translate(self, record, **kwargs):
# need stuff to convert a pyingest.arxiv record to denorm.proto
# This should be a general procedure for anything that comes out of
# adsabs-pyingest
        x = 0
        if (x > 0):
            print "lol."
        return x


    def serialize(self, record, **kwargs):

        if (len(record.keys()) > 0):
            rec = DenormalizedRecord(**record)
            task_output_results.delay(rec)
        else:
            print ("Null record, not sending to master pipeline")
