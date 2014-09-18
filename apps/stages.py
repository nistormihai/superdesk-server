import logging


from superdesk.models import BaseModel


logger = logging.getLogger(__name__)


class StagesModel(BaseModel):
    endpoint_name = 'stages'
    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'minlength': 1
        },
        'description': {
            'type': 'string',
            'minlength': 1
        },
        'desk': BaseModel.rel('desks', required=True, embeddable=True),
        'outgoing': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'stage': BaseModel.rel(endpoint_name, True)
                }
            }
        }
    }
