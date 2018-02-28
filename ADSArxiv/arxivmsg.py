from __future__ import absolute_import, unicode_literals


from adsmsg import DenormalizedRecord
from ADSArxiv.tasks import task_output_results
from ADSArxiv.app import AdsArxivCelery

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
        return record

    def serialize(self, record, **kwargs):

        if (len(record.keys()) > 0):
            rec = DenormalizedRecord(**record)
            task_output_results.delay(rec)
        else:
            print ("Null record, not sending to master pipeline")
