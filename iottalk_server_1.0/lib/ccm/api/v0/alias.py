"""
Alias Module.

    get
    set
"""
import logging

import db

from flask import g, request

from ccm.api.utils import blueprint, json_data, json_error

api = blueprint(__name__, __file__)
log = logging.getLogger("ccm.api.v0.api")


@api.route('/<string:mac_addr>/<string:df_name>',
           methods=['GET'], strict_slashes=False)
def get(mac_addr, df_name):
    """
    Get DeviceFeatureObject's alias_name.

    :param mac_addr: <Device.mac_addr>
    :param df_name: <DeviceFeature.df_name>
    :type mac_addr: str
    :type df_name: str

    :return:
        {
            'state': 'ok',
            'alias_name': <DFObject.alias_name>
        }
    """
    session = g.session
    dfo_record = (session.query(db.DFObject)
                         .select_from(db.Device)
                         .filter(db.Device.mac_addr == mac_addr)
                         .join(db.DeviceObject)
                         .join(db.DFObject)
                         .join(db.DeviceFeature)
                         .filter(db.DeviceFeature.df_name == df_name)
                         .first())

    if not dfo_record:
        return json_error('Cannot find Device or DeviceFeatureObject')

    return json_data(alias_name=dfo_record.alias_name)


@api.route('/<string:mac_addr>/<string:df_name>',
           methods=['POST'], strict_slashes=False)
def set(mac_addr, df_name):
    """
    Set DeviceFeatureObject's alias_name.

    :param mac_addr: <Device.mac_addr>
    :param df_name: <DeviceFeature.df_name>
    :param alias_name: <DFObject.alias_name>
    :type mac_addr: str
    :type df_name: str
    :type alias_name: str

    :return:
        {
            'state': 'ok',
            'alias_name': <DFObject.alias_name>
        }
    """
    session = g.session
    alias_name = request.json.get('alias_name')

    # check exist
    dfo_record = (session.query(db.DFObject)
                         .select_from(db.Device)
                         .filter(db.Device.mac_addr == mac_addr)
                         .join(db.DeviceObject)
                         .join(db.DFObject)
                         .join(db.DeviceFeature)
                         .filter(db.DeviceFeature.df_name == df_name)
                         .first())

    if not dfo_record:
        return json_error('Cannot find Device or DeviceFeatureObject')

    # udpate
    (session.query(db.DFObject)
            .filter(db.DFObject.dfo_id == dfo_record.dfo_id)
            .update({'alias_name': alias_name}))
    session.commit()

    return json_data(alias_name=dfo_record.alias_name)
