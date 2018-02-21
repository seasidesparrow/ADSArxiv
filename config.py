#!/usr/bin/env python

LOGGING_LEVEL = 'DEBUG'

## ================ ArXiv data location ================ #
## ##################################################### #
# Where the worker is going to look for incoming ArXiv
# submissions: ARCHIVE_ABS_DIR

INCOMING_ABS_DIR = '/proj/ads/abstracts/sources/ArXiv'

UPDATE_AGENT_DIR = INCOMING_ABS_DIR + '/UpdateAgent'

ARCHIVE_ABS_DIR = INCOMING_ABS_DIR + '/oai/arXiv.org'


## ================= celery/rabbitmq rules============== #
## ##################################################### #
#

CELERY_INCLUDE = ['ADSArxiv.tasks']
ACKS_LATE=True
PREFETCH_MULTIPLIER=1
CELERYD_TASK_SOFT_TIME_LIMIT = 300
CELERY_BROKER = 'pyamqp://'

CELERY_DEFAULT_EXCHANGE = 'arxiv_pipeline'
CELERY_DEFAULT_EXCHANGE_TYPE = "topic"


# Should this be going to port:6672 ?
#OUTPUT_CELERY_BROKER = 'pyamqp://guest:guest@localhost:6672/master_pipeline'
OUTPUT_CELERY_BROKER = 'pyamqp://guest:guest@localhost:5682/master_pipeline'

OUTPUT_TASKNAME = 'adsmp.tasks.task_update_record'
