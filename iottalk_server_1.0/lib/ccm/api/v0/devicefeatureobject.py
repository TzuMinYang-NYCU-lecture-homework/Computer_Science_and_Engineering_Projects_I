"""
DeviceFeature Module.

    _get_mf_parameter
    _update_mf_parameter
    _create_dfo
    _delete_dfo

    #create
    #delete
    get
    update
"""
import logging

import db

from flask import g, request
from sqlalchemy import and_

from ccm.api.utils import (blueprint, invalid_input,
                           json_data, json_error, record_parser)
from .function import _get_df_function_list
from .networkapplication import adjust_na

api = blueprint(__name__, __file__)
log = logging.getLogger("ccm.api.v0.api")


def _get_mf_parameter(mf_id):
    session = g.session

    # query DF_Parameter
    dfp_records = (session.query(db.DF_Parameter)
                          .filter(db.DF_Parameter.mf_id == mf_id)
                          .all())

    return [record_parser(dfp) for dfp in dfp_records]


def _update_mf_parameter(mf_id, df_parameter):
    session = g.session

    # update device feature parameter
    for idx, dfp in enumerate(df_parameter):
        # try update first
        update_dfp = (session.query(db.DF_Parameter)
                             .filter(db.DF_Parameter.mf_id == mf_id,
                                     db.DF_Parameter.param_i == idx)
                             .update(dfp))

        session.commit()

        # if return value is 0 means update 0 rows, so create new one
        if update_dfp == 0:
            new_dfp = db.DF_Parameter(
                mf_id=mf_id,
                param_type=dfp.get('param_type', 'int'),
                param_i=idx,
                idf_type=dfp.get('idf_type', 'sample'),
                fn_id=dfp.get('fn_id', None),
                min=dfp.get('min', 0),
                max=dfp.get('max', 0),
                unit_id=dfp.get('unit_id', 1),  # 1 for None
                normalization=dfp.get('normalization', 0),
            )
            session.add(new_dfp)
            session.commit()

    # delete other parameter,
    # which param_i larger then number of given parameters
    (session.query(db.DF_Parameter)
            .filter(db.DF_Parameter.mf_id == mf_id,
                    db.DF_Parameter.param_i >= len(df_parameter))
            .delete())

    session.commit()

    return mf_id


def _create_dfo(do_id, df_id, alias_name):
    session = g.session

    # create DFObject
    new_dfo = db.DFObject(
        do_id=do_id,
        df_id=df_id,
        alias_name=alias_name,
    )
    session.add(new_dfo)
    session.commit()

    return new_dfo.dfo_id


def _delete_dfo(dfo):
    session = g.session

    # get all NetworkApplication which connected
    na_records = (session.query(db.NetworkApplication)
                         .select_from(db.NetworkApplication)
                         .join(db.DF_Module)
                         .join(db.DFObject)
                         .filter(db.DFObject.dfo_id == dfo.dfo_id)
                         .group_by(db.NetworkApplication.na_id)
                         .all())

    # delete DF_Module
    (session.query(db.DF_Module)
            .filter(db.DF_Module.dfo_id == dfo.dfo_id)
            .delete())
    session.commit()

    # delete MultipleJoin_Module
    (session.query(db.MultipleJoin_Module)
            .filter(db.MultipleJoin_Module.dfo_id == dfo.dfo_id)
            .delete())
    session.commit()

    # delete DFObject
    session.delete(dfo)
    session.commit()

    # check na still has at least one input and output
    for na in na_records:
        adjust_na(na.na_id)


# @api.route('/', methods=['PUT'], strict_slashes=False)
def create(pid, do_id):
    '''
    Reserved, not public API.

    Request::

        {
            "df_id": 24,
            "alias_name": "good_feature"
        }

    Response::

        {
            'state': 'ok',
            'dfo_id': 42,
        }
    '''
    err = invalid_input(request.json, {'df_id': int,
                                       'alias_name': str})
    if err:
        return json_error(err), 400

    return json_data(dfo_id=_create_dfo(do_id, **request.json)), 201


# @api.route('/<ind:id_>', methods=['DELETE'], strict_slashes=False)
def delete(pid, do_id, id_):
    '''
    Reserved, not public API.

    Response::

        {
            'state': 'ok',
            'do_id': 42,
            'dfo_id': 24
        }
    '''
    session = g.session

    # Get DFObject
    dfo_record = (session.query(db.DFObject)
                         .filter(db.DFObject.dfo_id == id_)
                         .first())

    # Delete all relationship records of dfo
    _delete_dfo(dfo_record)

    return json_data(do_id=do_id, dfo_id=id_)


@api.route('/<int:id_>', methods=['GET'], strict_slashes=False)
def get(pid, do_id, id_):
    '''
    Response::

        {
            'state': 'ok',
            'data': {
                'dfo_id': 42,
                'df_id': 24,
                'df_type': 'input',
                'alias_name': 'good_feature',
                'dm_name': 'good_model',
                'df_mapping_func': [ ...],
                'df_parameter': [ ...]
            },
        }
    '''
    session = g.session

    # get basic info
    dfo_record = (session.query(db.DFObject.dfo_id,
                                db.DFObject.alias_name,
                                db.DFObject.df_id,
                                db.DeviceModel.dm_name,
                                db.DeviceFeature.df_type,
                                db.DM_DF.mf_id)
                         .select_from(db.DFObject)
                         .join(db.DeviceObject)
                         .join(db.DeviceModel)
                         .join(db.DeviceFeature)
                         .join(db.DM_DF,
                               and_(db.DM_DF.df_id == db.DFObject.df_id,
                                    db.DM_DF.dm_id == db.DeviceModel.dm_id))
                         .filter(db.DFObject.dfo_id == id_)
                         .first())

    result = record_parser(dfo_record)
    result['df_mapping_func'] = _get_df_function_list(dfo_record.df_id)
    result['df_parameter'] = _get_mf_parameter(dfo_record.mf_id)

    return json_data(data=result)


@api.route('/<int:id_>', methods=['GET'], strict_slashes=False)
def update(pid, do_id, id_):
    '''
    Request::

        {
            'alias_name': 'Finn',
            'df_parameter': [ { ... }, ... ]
        }

    Response::

        {
            'state': 'ok',
            'dfo_id': 24
        }
    '''
    err = invalid_input(request.json, {},
                        optional={'df_parameter': list,
                                  'alias_name': str})
    if err:
        return json_error(err), 400

    session = g.session

    # Check DM_DF exist
    mf_record = (session.query(db.DM_DF)
                        .select_from(db.DFObject)
                        .join(db.DeviceObject)
                        .outerjoin(db.DM_DF,
                                   and_(db.DM_DF.df_id == db.DFObject.df_id,
                                        db.DM_DF.dm_id == db.DeviceObject.dm_id))
                        .filter(db.DFObject.dfo_id == id_)
                        .first())

    if not mf_record:
        return json_error('Device Feature for the Device Model not find.'), 400

    # Update DF_Parameter
    if 'df_parameter' in request.json:
        _update_mf_parameter(mf_record.mf_id, request.json.get('df_parameter'))

    # Update alias_name
    if 'alias_name' in request.json:
        (session.query(db.DFObject)
                .filter(db.DFObject.dfo_id == id_)
                .update({'alias_name': request.json.get('alias_name')}))
        session.commit()

    return json_data(dfo_id=id_)
