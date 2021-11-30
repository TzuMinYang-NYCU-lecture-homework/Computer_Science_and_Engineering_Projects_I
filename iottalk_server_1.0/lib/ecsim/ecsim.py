#!/usr/bin/env python3
import db
import random
import json
#db.connect('ec_db')

import ec_config
db.connect(ec_config.DB_NAME)

class SimulatedIDF():
    def __init__(self, session, dm_name, df_name):
        self.type = []
        df_parameter = (
            session.query(db.DF_Parameter.param_type)
            .select_from(db.DF_Parameter)
            .join(
                (db.DM_DF, db.DM_DF.mf_id == db.DF_Parameter.mf_id),
                (db.DeviceModel, db.DM_DF.dm_id == db.DeviceModel.dm_id),
                (db.DeviceFeature, db.DM_DF.df_id == db.DeviceFeature.df_id)
            )
            .filter(db.DF_Parameter.u_id == None,
                    db.DF_Parameter.mf_id != None,
                    db.DeviceModel.dm_name == dm_name,
                    db.DeviceFeature.df_name == df_name)
            .order_by(db.DF_Parameter.param_i)
        )
        for param_type, in df_parameter:
            self.type.append(param_type)

    def gen_data(self, param_range):
        data = []
        #print(param_range)
        for range_, param_type in zip(param_range, self.type):
            if param_type == 'int':
                val = round(random.uniform(range_[0], range_[1]))
            elif param_type == 'float':
                val = random.uniform(range_[0], range_[1])
            elif param_type == 'boolean':
                val = random.choice([True, False])
            else:
                val = ''
            data.append(val)
        #print('data', data)
        return data


import csmapi
class SimulatedDevice():
    def __init__(self, session, dm_name, do_id):
        self.dm_name = dm_name
        self.do_id = do_id
        self.mac_addr = 'SimDev'+str(do_id)
        self.sidfs = {}          # sims[df_name] = SimulatedIDF()
        self.d_id = None        # represent status in Comm, fill it after created.
        self.mf_id = {}

        dm_id = (
            session.query(db.DeviceObject.dm_id)
            .filter(db.DeviceObject.do_id == do_id)
        ).first()[0]

        df_id_list = [ df_id for (df_id,) in ((
            session.query(db.DFObject.df_id)
            .filter(db.DFObject.do_id == do_id)
            ).all())
        ]
        
        device_features = (
            session.query(db.DeviceFeature.df_id,
                          db.DeviceFeature.df_name, 
                          db.DeviceFeature.df_type,
                          db.DM_DF.mf_id)
            .select_from(db.DeviceFeature)
            .join(db.DM_DF)
            .filter(db.DM_DF.dm_id == dm_id, db.DM_DF.df_id.in_(df_id_list))
        )
           
        all_features = []
        all_idf_id = []
        for df_id, df_name, df_type, mf_id in device_features:
            all_features.append(df_name)
            if df_type == 'output': continue
            sidf = SimulatedIDF(session, dm_name, df_name)
            self.sidfs[df_name] = sidf
            all_idf_id.append(df_id)
            self.mf_id[df_name] = mf_id

        profile = {
            'd_name': dm_name,
            'dm_name': dm_name,
            'u_name': None,
            'is_sim': True,
            'df_list': all_features,
        }
        csmapi.register(self.mac_addr, profile)
        print('REGISTER:', self.mac_addr)

        self.d_id = (
            session.query(db.Device.d_id)
            .filter(db.Device.mac_addr == self.mac_addr)
            .first()
        )
        if self.d_id == None: return
        self.d_id = self.d_id[0]

        simuIDF_existed =( session.query(db.SimulatedIDF).filter(db.SimulatedIDF.d_id == self.d_id) )
        if simuIDF_existed.first():
            simuIDF_existed.delete()
            session.commit()
            print ('Kill occupied SimulatedIDF d_id.')

        for idf_id in all_idf_id:
            db_sidf = db.SimulatedIDF(
                d_id = self.d_id,
                df_id = idf_id,
                execution_mode = 'Continue',
            )
            session.add(db_sidf)

        dev_obj = (
            session.query(db.DeviceObject)
            .select_from(db.DeviceObject)
            .filter(db.DeviceObject.do_id == do_id)
            .first()
        )
        if dev_obj.d_id == None:
            dev_obj.d_id = self.d_id

            # Restart db.Project.
            prj = (
                session.query(db.Project)
                .select_from(db.DeviceObject)
                .join(db.Project)
                .filter(db.DeviceObject.do_id == self.do_id)
                .first()
            )
            if not prj: prj.restart = True

            session.commit()

    def delete(self, session, KILL=0):
        bound_dev_obj = (
            session.query(db.DeviceObject)
            .select_from(db.DeviceObject)
            .filter(db.DeviceObject.d_id == self.d_id)
            .first()
        )
        if not bound_dev_obj or KILL == 1:
            try:
                csmapi.deregister(self.mac_addr)
            except:
                print('no device')

            (session.query(db.SimulatedIDF)
            .filter(db.SimulatedIDF.d_id == self.d_id)
            ).delete()
            session.commit()
            self.d_id = None

    def __del__(self):
        if self.d_id:
            self.delete(db.get_session())

    def push_data(self, session):
        mac_addr = (
            session.query(db.Device.mac_addr)
            .select_from(db.Device)
            .join(db.DeviceModel)
            .filter(db.DeviceModel.dm_name == self.dm_name,
                    db.Device.status == 'online',
                    db.Device.is_sim == False)
            .first()
        )	
        simulatedIDF_modes = (
            session.query(db.DeviceFeature.df_name,
                          db.DeviceFeature.df_id,
                          db.Device.dm_id,
                          db.SimulatedIDF.execution_mode,
                          db.SimulatedIDF.data,)
            .select_from(db.SimulatedIDF)
            .join(db.DeviceFeature)
            .join(db.Device)
            .join(db.DeviceModel)
            .filter(db.SimulatedIDF.d_id == self.d_id)
        )

        if mac_addr == None:
            min_max = None
        else:
            try:
                min_max = csmapi.pull(mac_addr[0], 'profile')['min_max']
            except:
                min_max = None
        for df_name, df_id, dm_id, execution_mode, data in simulatedIDF_modes:
                param_range = []
                params = (session.query(db.DF_Parameter.min, 
                                       db.DF_Parameter.max,)
                                .select_from(db.DM_DF)
                                .join(db.DF_Parameter)
                                .filter(db.DM_DF.df_id == df_id, 
                                        db.DM_DF.dm_id == dm_id)
                                .order_by(db.DF_Parameter.param_i)
                         )
                for i in range(params.count()):
                    min, max = params[i]
                    if min != max:
                        param_range.append((min, max))
                    elif min_max and df_name in min_max.keys() and len(min_max[df_name]) > i:                        
                        param_range.append(min_max[df_name][i])
                    else:
                        param_range.append((0, 1))

                sidf = self.sidfs[df_name]
                if execution_mode == 'Continue':
                    csmapi.push(
                        self.mac_addr, 
                        df_name, 
                        sidf.gen_data(param_range)
                    )
                elif execution_mode == 'Step':
                    csmapi.push(
                        self.mac_addr, 
                        df_name, 
                        sidf.gen_data(param_range)
                    )
                    (session.query(db.SimulatedIDF)
                    .filter(db.SimulatedIDF.d_id == self.d_id,
                            db.SimulatedIDF.df_id == df_id)
                    .first()).execution_mode = 'Stop'
                    session.commit()
                elif execution_mode == 'Input':
                    csmapi.push(
                        self.mac_addr,
                        df_name,
                        json.loads(data)['input']
                    )
                    sidf_record = (session.query(db.SimulatedIDF)
                    .filter(db.SimulatedIDF.d_id == self.d_id,
                            db.SimulatedIDF.df_id == df_id)
                    .first())
                    sidf_record.execution_mode = 'Stop'
                    sidf_record.data = None
                    session.commit()
                else: # Stop
                    continue


import time
import copy
def main():
    sim_devs = {}    # dm_sims[do_id] = dm_sim

    # check server first.
    while True:
        try:
            csmapi.tree()
        except:
            #print('reconnecting to server...')
            time.sleep(1)
        else:
            break
    # if there are any simulator in Comm / db.SimulatedIDF, clear them.
    for mac_addr in csmapi.tree():
        if mac_addr.startswith('SimDev'):
            csmapi.deregister(mac_addr)

    session = db.get_session()
    session.query(db.SimulatedIDF).delete()

    # if there are any simulator mounted on DeviceObject, clear them, too.
    # When the simulator is restarted (by reboot or some unexpected errors),
    # the old d_id still mount on DeviceObject.
    query_p_dm_with_simulator = (
        session.query(db.DeviceObject)
        .select_from(db.DeviceObject)
        .join(db.Device)
        .filter(db.Device.is_sim == True)
    )
    for p_dm in query_p_dm_with_simulator:
        p_dm.d_id = None

    session.commit()
    
    previous_do_id_with_simu_on = []
    # main loop
    while True:
        do_id_with_simu_on = []            
        device_objs_with_simu_on = []

        device_objs_with_simu_on = (
            session.query(
                db.DeviceObject.do_id,
                db.DeviceModel.dm_name,
                db.DeviceObject.d_id)
            .select_from(db.DeviceObject)
            .join(db.Project)
            .join(db.DeviceModel)
            .filter(db.Project.sim == 'on')
        )

        for do_id, dm_name, d_id in device_objs_with_simu_on:
            do_id_with_simu_on.append(do_id)
            if not d_id:                
                sim_dev = SimulatedDevice(session, dm_name, do_id)
                sim_devs[do_id] = sim_dev

        for _id in previous_do_id_with_simu_on:
            if _id not in do_id_with_simu_on:
                target = sim_devs.get(_id)
                if target:
                    target.delete(session,KILL=1)
                    if not target.d_id: sim_devs.pop(_id, None)

        previous_do_id_with_simu_on = do_id_with_simu_on.copy()   

        for do_id, sim_dev in list(sim_devs.items()):
            sim_dev.delete(session)
            if not sim_dev.d_id:
                sim_devs.pop(do_id, None)
            else:
                if do_id in do_id_with_simu_on: sim_dev.push_data(session)

        print('# of sim_dev: ', len(sim_devs))
        time.sleep(1)

if __name__ == '__main__':
    main()
