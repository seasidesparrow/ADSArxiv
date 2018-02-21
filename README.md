# ADSArxiv

A worker that generates metadata records from ArXiv.org in .json format
suitable for conversion to PROTOBUF, and forwards them to RabbitMQ (to
the queue "arxiv_pipeline/output-results")

ADSArxiv is intended to be plugged into a generic ADSdirectingest pipeline,
which could include other pub-specific utilities (e.g. APS, Zenodo).
