from __future__ import absolute_import, unicode_literals

#import ADSPipeline
import adsputils

import app as app_module
#from aip.libs import solr_adapter, merger, read_records
from kombu import Queue
from adsmsg import BibRecord, DenormalizedRecord

app = app_module.AdsArxivCelery('arxiv-pipeline')
logger = app.logger

from tasks import task_output_results

class ArxivToMasterPipeline(dict):

    def serialize(self, record, **kwargs):

        if (len(record.keys()) > 0):
            rec = DenormalizedRecord(**record)
            task_output_results.delay(rec)
        else:
            print ("Null record, not sending to master pipeline")