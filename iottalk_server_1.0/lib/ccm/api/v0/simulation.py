"""
Simulation Moduel.

    get
    update
"""
import logging

import db

from flask import g, request

from ccm.api.utils import blueprint, json_data, json_error

api = blueprint(__name__, __file__)
log = logging.getLogger("ccm.api.v0.api")


@api.route('/<int:p_id>', methods=['GET'], strict_slashes=False)
def get(p_id):
    """
    Get simulation status about Project by p_id.

    Response:

        {
            'state': 'ok',
            'data': 'on' / 'off'
        }

    Response if not project not found, HTTP 404 is returned:

        {
            'state': 'error',
            'reason': 'project not found',
        }
    """
    session = g.session
    project_record = (session.query(db.Project)
                             .filter(db.Project.p_id == p_id)
                             .first())
    if not project_record:
        return json_error('Project not found.')

    return json_data(data=project_record.sim)


@api.route('/<int:p_id>', methods=['POST'], strict_slashes=False)
def update(p_id):
    """
    Update simulation status of a project.

    Request:

        {
            'sim': 'on' | 'off',
        }

    Response:

        {
            'state': 'ok',
            'p_id': 42,
            'sim': 'on',
        }
    """
    session = g.session

    sim = request.json.get('sim')

    # check exist
    project_record = (session.query(db.Project)
                             .filter(db.Project.p_id == p_id)
                             .first())

    if not project_record:
        return json_error('Project not found.')

    # check status is valid and set ControlChannel
    if str(project_record.sim) == str(sim):
        return json_data(p_id=p_id, sim=sim)

    project_record.sim = sim
    session.commit()

    return json_data(p_id=p_id, sim=sim)
