

### FIXME: Merge feature config of imported configs don't work yet ... :/
### Need to fix this in flm.main.run().  Probably all $import's should be
### processed first, before merging anything.

flm_default_import_config = {
    'flm': {
        'features': {
            'flm_citations': {},
            # {
            #     'sources': [
            #         {
            #             '$defaults': True,
            #         },
            #     ],
            # },
        },
    },
}


from .feature import FeatureClass
