MONGO_URI = 'mongodb://localhost:27017/delivery_system'

DOMAIN = {
    'orders': {
        'schema': {
            'status': {
                'type': 'string',
                'allowed': ['unassigned', 'assigned','delivered'],
                'required': True,
            },
            'driver_id': {
                'type': 'objectid',
                'nullable': True,
            },
            'start_location': {
                'type': 'point',
                'required': True,
            },
            'end_location': {
                'type': 'point',
                'required': True,
            },
        },
    },
    'drivers': {
        'schema': {
            # 'name': {
            #     'type': 'string',
            #     'required': True,
            # },
            'status': {
                'type': 'string',
                'allowed': ['busy', 'free'],
                'required': True,
            },
            'current_location': {
                'type': 'point',
                'required': True,
            },
        },
    },
}
