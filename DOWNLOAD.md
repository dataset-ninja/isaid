Dataset **iSAID** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/A/u/hW/JrUp42uwxDibAP6Lvmt9sGR2LTKI3vCtdtL8OpAVPsPdNyyRLQ2zcroGkFdaPbZlPiLcGbpt3U4sd0q6lrLjV60APl4nGNRwZ0LuoVd3I4K9O1bGiN6YNIrZ49OZ.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='iSAID', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://captain-whu.github.io/iSAID/dataset.html).