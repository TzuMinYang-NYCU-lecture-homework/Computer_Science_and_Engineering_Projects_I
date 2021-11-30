"""
Function Module.

    _update_function
    _get_df_function_list

    create
    update
    delete
    list
    list_df
    list_na
    get
    get_all_version
    get_version
    create_sdf
    delete_sdf

    Not Support: _get_dfo_function_info
"""
import logging

from datetime import date

from flask import g, request
from sqlalchemy import func, or_

import db

from ccm.api.utils import (blueprint, invalid_input,
                           json_data, json_error, record_parser)

api = blueprint(__name__, __file__)
log = logging.getLogger("ccm.api.v0.api")


def _update_function(fn_id, code, df_id=None, fnvt_idx=None):
    """
    Update the Function code.

    If 'fnvt_idx' given, check owner is correct, then update code and date.
    Otherwise, create new function version.

    :param fn_id': <Function.fn_id>
    :param code': <FunctionVersion.code>
    :param df_id': <DeviceFeature.df_id>, optional
                   if given, add this function to SDF list,
                   else add to join function list
    :param fnvt_idx': <FunctionVersion.fnvt_idx>, optional
                      if given, update the function code by version,
                      else create new version
    :type fn_id: int
    :type code: str
    :type df_id: int
    :type fnvt_idx: int

    :return:
        {
            'fn_id': <Function.fn_id>,
            'fnvt_idx': <FunctionVersion.fnvt_idx>
        }
    """
    session = g.session

    # check function code first
    try:
        run_code = compile(code, 'run', mode='exec')
        exec(run_code, {})
    except Exception as e:
        return json_error(e)

    # Add to Function list
    if df_id:
        _create_functionSDF(fn_id, df_id)

    # check version id (fnvt_idx) is given,
    # if given, update the version,
    # otherwise create new version.
    if fnvt_idx:  # update version
        # check user is function version owner
        query_fnvt = (session.query(db.FunctionVersion)
                             .filter(db.FunctionVersion.fnvt_idx == fnvt_idx)
                             .first())
        if query_fnvt:
            # TODO: Update the NetworkApplication in execution

            # update version
            query_fnvt.code = code
            query_fnvt.date = date.today()
            session.commit()
        else:
            # given version not found or user is not owner, raise CCMError
            return json_error('Function Version not found.')
    else:  # create new version
        # check function exist
        query_fn = (session.query(db.Function)
                           .filter(db.Function.fn_id == fn_id)
                           .first())
        if not query_fn:
            return json_error('Function id not found.')

        # TODO: Update the NetworkApplication in execution

        # Save new code
        new_fnv = db.FunctionVersion(fn_id=fn_id,
                                     code=code,
                                     date=date.today(),
                                     u_id=1,
                                     completeness=True,
                                     is_switch=False,
                                     non_df_args='')
        session.add(new_fnv)
        session.commit()

        fnvt_idx = new_fnv.fnvt_idx

    return {'fn_id': fn_id, 'fnvt_idx': fnvt_idx}


def _get_df_function_list(df_id):
    session = g.session

    # query general function and user owned function
    fn_records = (session.query(db.Function)
                         .select_from(db.FunctionSDF)
                         .join(db.Function)
                         .filter(db.FunctionSDF.df_id == df_id)
                         .order_by(db.Function.fn_name)
                         .all())

    return [record_parser(f) for f in fn_records]


def _create_functionSDF(fn_id, df_id):
    session = g.session

    # check df is exist
    if df_id:
        query_df = (session.query(db.DeviceFeature)
                           .filter(db.DeviceFeature.df_id == df_id)
                           .first())

        if not query_df:
            return json_error('Device Feature not found.')

    # check record exist
    query_sdf = (session.query(db.FunctionSDF)
                        .filter(db.FunctionSDF.fn_id == fn_id,
                                db.FunctionSDF.df_id == df_id)
                        .all())

    if not query_sdf:
        # create new record
        new_fnsdf = db.FunctionSDF(fn_id=fn_id,
                                   df_id=df_id,
                                   u_id=1,
                                   display=1)
        session.add(new_fnsdf)
        session.commit()

    return {'fn_id': fn_id, 'df_id': df_id}


@api.route('/', methods=['PUT'], strict_slashes=False)
def create():
    '''
    Create new Function.

    If function name is exist, update the function code for login user.
    Note: Function name should start with alphabet.

    Request::

        {
            'fn_name': 'sleep',
            'code': 'import time; time.sleep(1)',
            'df_id': 24 // optional, if give,
                        // this function code is for the Device Feature,
                        // o.w. for the join
        }

    Response::

        {
            'state': 'ok',
            'fn_id': 666,
            'fnvt_idx': 1
        }
    '''
    err = invalid_input(
        request.json,
        {'fn_name': str, 'code': str},
        {'df_id': (int, type(None))})

    if err:
        return json_error(err), 400

    session = g.session

    fn_name = request.json.get('fn_name')
    code = request.json.get('code')
    df_id = request.json.get('df_id')

    # check function name is start with alphabet
    if not fn_name[0].isalpha():
        return json_error('Function name should start with alphabet.')

    # Check function name exist.
    query_fn = (session
                .query(db.Function)
                .filter(db.Function.fn_name == fn_name)
                .first())
    if query_fn:
        # function is exist
        return _update_function(query_fn.fn_id, code, df_id)

    # check function code first, only check compile
    try:
        run_code = compile(code, 'run', mode='exec')
        exec(run_code, {})
    except Exception as e:
        return json_error(e)

    # Save new function name.
    new_fn = db.Function(fn_name=fn_name)
    session.add(new_fn)
    session.commit()

    # Save new function code.
    return json_data(**_update_function(new_fn.fn_id, code, df_id)), 201


@api.route('/<int:fn_id>', methods=['POST'], strict_slashes=False)
def update(fn_id):
    '''
    Update the Function code.

    If 'fnvt_idx' given, check owner is correct, then update code and date.
    Otherwise, create new function version.

    Request::

        {
            'code': 'import time; time.sleep(1)',
            'df_id': 24,  // optional, if give,
                          // this function code is for the Device Feature,
                          // o.w. for the join
            'fnvt_idx': 1 // optional, if given,
                          // update the function code by version,
                          // else create new version
        }

    Response::

        {
            'state': 'ok',
            'fn_id': 666,
            'fnvt_idx': 1
        }
    '''
    err = invalid_input(
        request.json,
        {'code': str},
        {'df_id': int, 'fnvt_idx': int})

    if err:
        return json_error(err), 400

    code = request.json.get('code')
    df_id = request.json.get('df_id')
    fnvt_idx = request.json.get('fnvt_idx')

    return json_data(**_update_function(fn_id, code,
                                        df_id=df_id,
                                        fnvt_idx=fnvt_idx))


@api.route('/<int:fn_id>', methods=['DELETE'], strict_slashes=False)
def delete(fn_id):
    '''
    Delete the Function by given fn_id.

    Server will check the Function is used or not.
    If delete successful, server will return fn_id, else return NULL

    Response::

        {
            'state': 'ok',
            'fn_id': 666
        }
    '''
    session = g.session

    # check in used.
    # DF_Parameter, check feature default function.
    dfp_count, = (session.query(func.count(db.DF_Parameter.fn_id))
                         .select_from(db.DF_Parameter)
                         .filter(db.DF_Parameter.fn_id == fn_id)
                         .first())
    # DF_Module, check exist join link used.
    dfm_count, = (session.query(func.count(db.DF_Module.fn_id))
                         .filter(db.DF_Module.fn_id == fn_id)
                         .first())
    # MultipleJoin_Module, check multiple join function used.
    mjm_count, = (session.query(func.count(db.MultipleJoin_Module.fn_id))
                         .filter(db.MultipleJoin_Module.fn_id == fn_id)
                         .first())
    # FunctionSDF, check other user use for SDF
    sdf_count, = (session.query(func.count(db.FunctionSDF.fn_id))
                         .filter(db.FunctionSDF.fn_id == fn_id)
                         .first())

    if dfp_count or dfm_count or mjm_count or sdf_count:
        return json_error('This function is used, can not delete.')

    # Delete FunctionSDF
    (session.query(db.FunctionSDF)
            .filter(db.FunctionSDF.fn_id == fn_id)
            .delete())

    # Delete FunctionVersion
    (session.query(db.FunctionVersion)
            .filter(db.FunctionVersion.fn_id == fn_id)
            .delete())

    # Delete Function
    (session.query(db.Function)
            .filter(db.Function.fn_id == fn_id)
            .delete())

    session.commit()

    return json_data(fn_id=fn_id)


@api.route('/', methods=['GET'], strict_slashes=False)
def list_():
    '''
    Get all Functions.

    List all function name in Function which user can use.

    Response::

        {
            'state': 'ok',
            'fn_list': [
                {
                    'fn_id': 666,
                    'fn_name': 'sleep'
                },
                ...
            ]
        }
    '''
    session = g.session

    # query general function and user owned function
    query_fn = (session.query(db.Function)
                       .select_from(db.Function)
                       .join(db.FunctionVersion)
                       .order_by(db.Function.fn_name)
                       .all())

    return json_data(fn_list=[record_parser(f) for f in query_fn])


@api.route('/devicefeature/<int:df_id>', methods=['GET'], strict_slashes=False)
def list_df_functions(df_id):
    '''
    Get all Functions for Device Feature could use.

    The list of function only contain which store in FunctionSDF with
    login user and device feature.

    Response::

        {
            'state': 'ok',
            'fn_list': [
                {
                    'fn_id': 666,
                    'fn_name': 'sleep'
                },
                ...
            ]
        }
    '''
    return json_data(fn_list=_get_df_function_list(df_id))


@api.route('/networkapplication', methods=['GET'], strict_slashes=False)
def list_na_functions():
    '''
    Get all Functions for Network Application could use.

    The list of function only contain which store in FunctionSDF with
    login user and NetworkApplication (df_id == None).

    Response::

        {
            'state': 'ok',
            'fn_list': [
                {
                    'fn_id': 666,
                    'fn_name': 'sleep'
                },
                ...
            ]
        }
    '''
    session = g.session

    # query general function and user owned function
    query_fn = (session.query(db.Function)
                       .select_from(db.FunctionSDF)
                       .join(db.Function)
                       .filter(db.FunctionSDF.df_id.is_(None))
                       .order_by(db.Function.fn_name)
                       .all())

    return json_data(fn_list=[record_parser(f) for f in query_fn])


@api.route('/<int:fn_id>', methods=['GET'], strict_slashes=False)
def get(fn_id):
    '''
    Get the latest Function's infomation by given fn_id.

    Response::

        {
            'state': 'ok',
            'data': {
                'fnvt_id': 21,
                'fn_id': 666,
                'date': '2020/01/01',
                'code': 'import time; time.sleep(1)',
            }
        }
    '''
    session = g.session

    # query_fn = [<fn_name>, <fnvt_idx>, <code>, <date>]
    if not fn_id or int(fn_id) <= 0:
        # query no function
        query_fn = [None, None, None, None]
    else:
        # query by function id (fn_id)
        query_fn = (session.query(db.Function.fn_name,
                                  db.FunctionVersion.fnvt_idx,
                                  db.FunctionVersion.code,
                                  db.FunctionVersion.date)
                           .select_from(db.FunctionVersion)
                           .join(db.Function)
                           .filter(db.FunctionVersion.fn_id == fn_id)
                           .order_by(db.FunctionVersion.fnvt_idx.desc())
                           .first())

        if not query_fn:
            return json_error('Function version not found by fn_id.')

    result = {
        'name': query_fn[0],
        'fnvt_idx': query_fn[1],
        'code': query_fn[2],
        'date': str(query_fn[3])
    }
    return json_data(data=result)


@api.route('/<int:fn_id>/a', methods=['GET'], strict_slashes=False)
def get_all_versions(fn_id):
    '''
    Get the Function's version list by given fn_id.

    Return general function version and user's function version.

    Response::

        {
            'state': 'ok',
            'fnvt_list': [
                {
                    'fnvt_id': 21,
                    'fn_id': 666,
                    'u_id': 1,
                    'date': '2020/01/01',
                    'code': 'import time; time.sleep(1)',
                    'completeness': 1,  // legacy
                    'is_switch': 0,     // legacy
                    'non_df_args': ''   // legacy
                },
                ...
            ]
        }
    '''
    session = g.session

    query_fnvt = (session.query(db.FunctionVersion)
                         .filter(db.FunctionVersion.fn_id == fn_id)
                         .all())

    return json_data(fnvt_list=[record_parser(fnvt) for fnvt in query_fnvt])


@api.route('/version/<int:fnvt_idx>', methods=['GET'], strict_slashes=False)
def get_version(fnvt_idx):
    '''
    Get the Function's infomation by given fnvt_idx.

    Response::

        {
            'state': 'ok',
            'data': {
                'fnvt_idx': 21,
                'fn_id': 666,
                'date': '2020/01/01',
                'code': 'import time; time.sleep(1)',
            }
        }
    '''
    session = g.session

    # query_fn = [<fn_name>, <fnvt_idx>, <code>, <date>]
    if not fnvt_idx:
        # query no function
        query_fn = [None, None, None, None]
    else:
        # query by function version id (fnvt_idx)
        query_fn = (session.query(db.Function.fn_name,
                                  db.FunctionVersion.fnvt_idx,
                                  db.FunctionVersion.code,
                                  db.FunctionVersion.date)
                           .select_from(db.FunctionVersion)
                           .join(db.Function)
                           .filter(db.FunctionVersion.fnvt_idx == fnvt_idx)
                           .order_by(db.FunctionVersion.fnvt_idx.desc())
                           .first())

        if not query_fn:
            return json_error('Function version not found by fnvt_idx.')

    result = {
        'name': query_fn[0],
        'fnvt_idx': query_fn[1],
        'code': query_fn[2],
        'date': str(query_fn[3])
    }

    return json_data(data=result)


@api.route('/<int:fn_id>/SDF/(?<int:df_id>)',
           methods=['PUT'], strict_slashes=False)
def create_sdf(fn_id, df_id=None):
    '''
    Add the Function to the usage list for
    Device Feature or Network Application.

    This addition will store in the FunctionSDF,
    and specified the login user.
    This API NOT support add the function to the usage list for general.

    Response::

        {
            'state': 'ok',
            'data': {
                'df_id': 21,
                'fn_id': 666
            }
        }
    '''
    return json_data(data=_create_functionSDF(fn_id, df_id))


@api.route('/<int:fn_id>/SDF/(?<int:df_id>)',
           methods=['DELETE'], strict_slashes=False)
def delete_sdf(fn_id, df_id=None):
    '''
    Remove the Function to the usage list for DF or NA.

    This will remove the specified setting which store in the FunctionSDF,
    and specified the login user.
    This API NOT support remove the function to the usage list for general.

    Response::

        {
            'state': 'ok',
            'data': {
                'df_id': 21,
                'fn_id': 666
            }
        }
    '''
    session = g.session

    # check in used
    # DF_Parameter, check feature default function.
    dfp_count, = (session.query(func.count(db.DF_Parameter.fn_id))
                         .select_from(db.DF_Parameter)
                         .join(db.DM_DF,
                               db.DM_DF.mf_id == db.DF_Parameter.mf_id)
                         .filter(db.DF_Parameter.fn_id == fn_id,
                                 or_(db.DM_DF.df_id == df_id,
                                     db.DF_Parameter.df_id == df_id))
                         .first())
    # DF_Module, check exist join link used.
    dfm_count, = (session.query(func.count(db.DF_Module.fn_id))
                         .select_from(db.DF_Module)
                         .join(db.DFObject)
                         .filter(db.DF_Module.fn_id == fn_id,
                                 db.DFObject.df_id == df_id)
                         .first())
    # MultipleJoin_Module, check multiple join function used.
    mjm_count, = (session.query(func.count(db.MultipleJoin_Module.fn_id))
                         .select_from(db.MultipleJoin_Module)
                         .join(db.DFObject)
                         .filter(db.MultipleJoin_Module.fn_id == fn_id,
                                 db.DFObject.df_id == df_id)
                         .first())

    if dfp_count or dfm_count or mjm_count:
        return json_error('This function is used, can not delete.')

    # move out function (delete FunctionSDF)
    (session.query(db.FunctionSDF)
            .filter(db.FunctionSDF.df_id == df_id,
                    db.FunctionSDF.fn_id == fn_id)
            .delete())
    session.commit()

    return json_data(data={'fn_id': fn_id, 'df_id': df_id})
