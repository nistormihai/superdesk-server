from superdesk.models import BaseModel
from bson.objectid import ObjectId
from flask import current_app as app


desks_schema = {
    'name': {
        'type': 'string',
        'unique': True,
        'required': True,
    },
    'description': {
        'type': 'string'
    },
    'members': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'user': BaseModel.rel('users', True)
            }
        }
    },
    'incoming_stage': BaseModel.rel('stages', True)
}


def init_app(app):
    DesksModel(app=app)
    UserDesksModel(app=app)


class DesksModel(BaseModel):
    endpoint_name = 'desks'
    schema = desks_schema
    datasource = {'default_sort': [('created', -1)]}

    def create(self, docs, **kwargs):
        for doc in docs:
            if not doc.get('incoming_stage', None):
                stage = {'name': 'Incoming'}
                app.data.insert('stages', [stage])
                doc['incoming_stage'] = stage.get('_id')
            super().create(docs, **kwargs)
            app.data.update('stages', doc['incoming_stage'], {'desk': doc['_id']})
        return [doc['_id'] for doc in docs]


class UserDesksModel(BaseModel):
    endpoint_name = 'user_desks'
    url = 'users/<regex("[a-f0-9]{24}"):user_id>/desks'
    schema = desks_schema
    datasource = {'source': 'desks'}
    resource_methods = ['GET']

    def get(self, req, lookup):
        if lookup.get('user_id'):
            lookup["members.user"] = ObjectId(lookup['user_id'])
            del lookup['user_id']
        return super().get(req, lookup)
