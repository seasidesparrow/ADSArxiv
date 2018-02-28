# ADSArxiv

A worker that generates metadata records from ArXiv.org in .json format
suitable for conversion to PROTOBUF, and forwards them to RabbitMQ (to
the queue "direct_ingest_pipeline/output-results").

ADSArxiv is intended to be plugged into eb-deploy's direct_ingest_pipeline.
My hope(?) is that there can be multiple workers for publication-specific
jobs (e.g. APS, Zenodo) that can *all* be plugged in to direct_ingest_pipeline,
and eliminate the need for separate eb-deploy pipelines for each publication
(i.e. don't do arxiv_pipeline, aps_pipeline, zenodo_pipeline, etc).
