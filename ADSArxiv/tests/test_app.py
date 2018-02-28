import unittest
import sys, os
import glob
import json
from mock import patch
from pyingest.parsers import arxiv
from ADSArxiv import arxivmsg
from ADSArxiv import tasks
from ADSArxiv import app as app_module

ONEREC_STD = {'bibcode': u'2011arXiv1111.0262T', u'keyword': [u'Astrophysics - Solar and Stellar Astrophysics'], 'pubdate': u'2011-11-01', 'title': [u"Modern observations of Hubble's first-discovered Cepheid in M31"], 'abstract': u"We present a modern ephemeris and modern light curve of the first-discovered\nCepheid variable in M31, Edwin Hubble's M31-V1. Observers of the American\nAssociation of Variable Star Observers undertook these observations during the\nlatter half of 2010. The observations were in support of an outreach program by\nthe Space Telescope Science Institute's Hubble Heritage project, but the\nresulting data are the first concentrated observations of M31-V1 made in modern\ntimes. AAVSO observers obtained 214 V-band, Rc-band, and unfiltered\nobservations from which a current ephemeris was derived. The ephemeris derived\nfrom these observations is JD(Max) = 2455430.5(+/-0.5) + 31.4 (+/-0.1) E. The\nperiod derived from the 2010 data are in agreement with the historic values of\nthe period, but the single season of data precludes a more precise\ndetermination of the period or measurement of the period change using these\ndata alone. However, using an ephemeris based upon the period derived by Baade\nand Swope we are able to fit all of the observed data acceptably well.\nContinued observations in the modern era will be very valuable in linking these\nmodern data with data from the 1920s-30s and 1950s, and will enable us to\nmeasure period change in this historic Cepheid. In particular, we strongly\nencourage intensive observations of this star around predicted times of maximum\nto constrain the date of maximum to better than 0.5 days.", u'author': [u'Templeton, M.; Henden, A.; Goff, W.; Smith, S.; Sabo, R.; Walker, G.; Buchheim, R.; Belcheva, G.; Crawford, T.; Cook, M.; Dvorak, S.; Harris, B.']}

ONEREC_FILE = 'test_data/1111/0262'


class TestADSArxiv(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.proj_home = os.path.join(os.path.dirname(__file__), '../..')
        self._app = tasks.app
        self.app = app_module.AdsArxivCelery('test',local_config={
            'SQLALCHEMY_URL': 'sqlite:///',
            'SQLALCHEMY_ECHO': False
            })
        tasks.app = self.app # monkey-patch the app object


    def test_record_translation(self):
        test_record = ONEREC_STD
        test_file = ONEREC_FILE

        with open(test_file,'rU') as fp:
            parser = arxiv.ArxivParser()
            indat = parser.parse(fp)
            outobj = arxivmsg.ArxivToMasterPipeline()
            outdat = outobj.translate(indat)
            self.assertEqual(outdat, test_record)
        

    def test_bad_file_record_translation(self):
        test_record = ONEREC_STD
        test_file = 'foo' # does not exist

        with self.assertRaises(IOError):
            with open(test_file,'rU') as fp:
                parser = arxiv.ArxivParser()
                indat = parser.parse(fp)
                outobj = arxivmsg.ArxivToMasterPipeline()
                outdat = outobj.translate(indat)
                self.assertEqual(outdat, test_record)


    def test_record_serialization(self):
        test_record = ONEREC_STD
        test_file = ONEREC_FILE

        with patch('ADSArxiv.tasks.task_output_results.delay', return_value = None) as next_app:
            with open(test_file,'rU') as fp:
                parser = arxiv.ArxivParser()
                indat = parser.parse(fp)
                outobj = arxivmsg.ArxivToMasterPipeline()
                outdat = outobj.translate(indat)
                output = outobj.serialize(outdat)
                self.assertTrue(next_app.called)

            indat = {}
            outobj = arxivmsg.ArxivToMasterPipeline()
            output = outobj.serialize(indat)
            self.assertTrue(next_app.called)
            self.assertTrue(next_app.call_count, 2)
