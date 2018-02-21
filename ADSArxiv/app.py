from __future__ import absolute_import, unicode_literals
from adsputils import ADSCelery
from kombu import Queue
from adsmsg import BibRecord, DenormalizedRecord
from ADSArxiv.tasks import task_output_results

class AdsArxivCelery(ADSCelery):
    pass

class ArxivToMasterPipeline(dict):


    def translate(self, record, **kwargs):
        if record['title']:
            record['title'] = [record['title']]
        if record['authors']:
            record['author'] = [record['authors']]
            del record['authors']
        if record['keywords']:
            record['keyword'] = [record['keywords']]
            del record['keywords']
        if record['properties']:
            del record['properties']

    def serialize(self, record, **kwargs):

        if (len(record.keys()) > 0):
            rec = DenormalizedRecord(**record)
            task_output_results.delay(rec)
        else:
            print ("Null record, not sending to master pipeline")

app = AdsArxivCelery('arxiv_pipeline')
logger = app.logger


