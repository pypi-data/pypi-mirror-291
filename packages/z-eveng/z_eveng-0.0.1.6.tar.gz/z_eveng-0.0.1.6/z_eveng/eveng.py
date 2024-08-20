import os
import sys
import requests
import json
import time
import logging
requests.packages.urllib3.disable_warnings() 
from .eveng_res import *

import copy
__author__ = {"Prajwal Jha" : "pkumarjha@zscaler.com"}

class Eveng:
    def __init__(self, config, configdir=None, logger = None, session:requests.Session=None):
        """
        config: used to pass config filename/data.
        configdir: used to pass custom configdir if lookup needs to be done in a custom directory.
        """
        self.logger = logger if logger != None else self.Initialize_Logger("eveng.log", Log_Level="INFO")
        if isinstance(session, requests.Session):
            self.__session = session
        else:
            self.__session = requests.Session()
            self.__session.verify = False
            self.__session.headers.update({'Connection': 'keep-Alive'})
        self.config=None
        if type(config) is dict:
            self.config = config 
        else:
            self.logger.info("Fetching Eveng's config.json file")
            if configdir is None: raise Exception("status:False\nmessage:Config directory path cannot be None")
            self.config = self.__class__.get_config(ConfigDir=configdir,ConfigFile=config)
        # self.get_config(Config)
        if self.config == None:self.logger.error("Failed to load Configuration file"); raise Exception("Failed to load Configuration file")
        self.resource = Eve(serveripaddr=self.config['server_ip'], configdata= self.config)
        status, message, self.current_lab_topology = self.get_lab_topology_info()
        if not status: raise Exception(f"status:{status}\nmessage:{message}\nresponse:{self.current_lab_topology}")
        status, message,self.current_lab_nodes_info = self.get_node_info()
        if not status: raise Exception(f"status:{status}\nmessage:{message}\nresponse:{self.current_lab_topology}")

    def Initialize_Logger(self,
                          Log_File_Name,  # (str)     Name of the Log file to be created
                          Log_Level,  # (str)     Level of logging (INFO/DEBUG/WARNING/CRICITCAL etc)
                          console_handle_needed=True  # (bool)    print_ on command line if True only
                          ):
        """
        Target: Create Logger object.
        Work Flow
        ----------
            1. Create a logger object.
            2. Create a console handler if required
                - console handler is used to print_ required info on command line window.
            3. Create a file handler -> mandatory
                - Make sure 'Logs' folder exists, as this file handler will be created in this folder only.
                - file handler is used to send all information to a log file in specified folder.
            4. Set the debug level (INFO/DEBUG/WARNING/CRITICAL etc). Default: INFO
            5. Specify how the logging must happen (with/without datetime/loglevel/username)
            6. Add all created handlers to the logger instance created in step 1.
            7. return the logger instance.
        """
        # 1, 2 & 3
        self.Logs_Directory = os.path.join(os.getcwd(), "Logs")
        logger = logging.getLogger(Log_File_Name)
        if console_handle_needed: console_handler = logging.StreamHandler()
        if not os.path.exists(self.Logs_Directory): os.mkdir(self.Logs_Directory)
        file_handler = logging.FileHandler(os.path.join(self.Logs_Directory, Log_File_Name))

        # 4
        if Log_Level:
            logger.setLevel(eval("logging.{}".format(Log_Level)))
            if console_handle_needed: console_handler.setLevel(eval("logging.{}".format(Log_Level)))
            file_handler.setLevel(eval("logging.{}".format(Log_Level)))

        # 5
        if console_handle_needed: console_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s'))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s'))

        # 6
        if console_handle_needed: logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        # 7
        return logger
    @classmethod
    def get_config(cls,ConfigDir, ConfigFile):
        if os.path.exists(os.path.join(ConfigDir, ConfigFile)):
            with open(os.path.join(ConfigDir, ConfigFile)) as config_file:
                return json.load(config_file)

        for f in os.listdir(ConfigDir):
            path = os.path.join(ConfigDir, f)
            if os.path.isdir(path):
                return cls.get_config(ConfigDir=path, ConfigFile=ConfigFile)
            
        return None
   
    def convert_resp_to_json(self, response):
        info = json.loads(response.text)
        if info.get("status") == None:
            info['status'] = "Invalid Status"
        if info.get("code") == None:
            return [False,"Response does not have status code",Exception("Response is invalid or corrupted as it does not have Status Code")]
        if info.get("message") == None:
            return [False, "Response does not contain any message",  Exception("Response does not contain any messages")]
        return [True, info.get('message'), info]
    
    def REQ(self, reqtype, url, data = None, params = None, headers=None, throw_excep=False, retry=False):
        assert reqtype in ["get", "post", "delete", "put"]
        response= None
        try:
            if reqtype == "get":
                response = self.__session.get(url=url, headers=headers, json=data, params=params)
            if reqtype == "post":
                response = self.__session.post(url=url, headers=headers, json=data, params=params)
            if reqtype == "delete":
                response = self.__session.delete(url, headers=headers, json=data, params=params)
            if reqtype == "put":
                response = self.__session.put(url, headers=headers, json=data, params=params)

            status, message, info = self.convert_resp_to_json(response)

            if not status: #return [status, f"Response seems to be in html format which is not useful. Ignoring this response.\n {response.text}", info]
                self.logger.debug("Response seems to be in html format which is not useful. Ignoring this response.")
                self.logger.debug(response.text)

            if str(response.status_code) >= str(200) and str(response.status_code)<=str(300):
                self.logger.debug(f'{info["status"]} - {info["message"]}')
            else:
                self.logger.debug(f"{response}\n{response.text}")
                raise Exception([False, message, Exception(f'{info["code"]} - {info["status"]} - {info["message"]}')])
            if "logout" in url:return [True, "Logged out successfully", f"Successfully Logged out from Eve-ng - {self.config['server_ip']}"]
            return [True, message, info]
        except Exception as E:
            #self.logger.error(E)
            if retry: 
                if type(E.args[0]) is not list: return [False, "Something went wrong", E]
                return E.args[0]
            self.logger.warning(f"Encountered Error: {E}\nWaiting 20 seconds..."); time.sleep(20)
            response = self.__session.get(url = self.resource.pollurl, headers=self.resource.pollheader)
            if str(response.status_code)!= str(200):
                self.__session.close()
                self.__session = requests.Session()
                self.__session.headers.update({'Connection': 'keep-Alive'})
                self.__session.verify = False
                if "logout" in url:
                    return [True, "Session has already expired", f"Successfully Logged out from Eve-ng - {self.config['server_ip']}"]
                self.logger.warning("Creating session to Eveng server : '{}'".format(self.config['server_ip']))
                self.__login()
            response= self.REQ(reqtype=reqtype,url=url,data=data,params=params,headers=headers,retry=True)
            if throw_excep: raise Exception(response)
            return response

    @classmethod
    def createSession(cls, config, configdir=None):
        if configdir is None and type(config) is not dict: raise Exception("status:False\nmessage:Config directory path cannot be None")
        if type(config) is not dict:
            config = cls.get_config(ConfigDir=configdir, ConfigFile=config)
        if config is None: 
            raise Exception("Failed to load the configuration")
        evengresource = Eve(serveripaddr=config['server_ip'], configdata= config)
        session= requests.Session()
        session.headers.update({'Connection': 'keep-Alive'})
        session.verify=False
        response = session.post(url=evengresource.loginurl, headers=evengresource.loginheader, json=evengresource.loginpayload)
        if str(response.status_code) !=str(200):
            return [False, f"Unable to login specified user {config['creds']['username']} into eveng server {config['server_ip']}", None]
        return [True, "User '{}' logged into the eveng-server".format(config['creds']['username']), session]
    def __login(self):
        response = self.__session.post(url=self.resource.loginurl, headers=self.resource.loginheader, json =self.resource.loginpayload)
        if str(response.status_code) !=str(200):
            self.logger.error(f"Unable to login specified user {self.config['creds']['username']} into eveng server {self.config['server_ip']}")
            status, message, info = self.convert_resp_to_json(response)
            raise Exception(f'{info["code"]} - {info["status"]} - {info["message"]}')
        self.logger.info("User '{}' logged into the eveng-server".format(self.config['creds']['username']))

    def logout(self):
        self.REQ(reqtype="get", url= self.resource.logouturl)

    def get_user_info(self):
        status, message, response = self.REQ(reqtype="get", url= self.resource.getuserinfourl)
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
    def get_system_status(self):
        status, message, response = self.REQ(reqtype="get", url = self.resource.systemstatusurl)
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return[status, message, response['data']]
        # print(f"status code : {response.status_code}")
        # print(response.text)

    def list_node_templates(self):
        status, message, response = self.REQ(reqtype="get", url = self.resource.listnodetempurl)
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return[status, message, response['data']]

    def list_images_from_nodetemplate(self, templatename):
        status, message, response = self.REQ(reqtype="get", url = self.resource.imgfromnodetemplateurl.format(templatename))
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return [status, message, response['data']]
    def list_content_inside_folders(self, folderpath):
        status, message, response = self.REQ(reqtype="get", url = self.resource.listallcontenturl.format(folderpath))
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return [status, message,response['data']]
    
    def list_user(self, username=None):
        #if logged in as admin then it will list all the users, else the current user logged in if no username is specified.
        url = self.resource.listalluserurl
        if not username == None:
            url = ''.join([self.resource.listalluserurl, username])
        status, message, response = self.REQ(reqtype="get", url = url)
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return [status, message,response['data']]
        # print(f"status code : {response.status_code}")
        # print(response.text)

    def get_lab_info(self, labpath=None):
        if labpath == None:
            labpath = self.config['path']
        status, message, response = self.REQ(reqtype="get", url = self.resource.getlabinfourl.format(labpath))
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return [status, message, response['data']]
    
    def get_labnetwork_info(self, labpath=None, networkid=None):
        if labpath == None:
            labpath = self.config['path']
        url = self.resource.getlabnetworkinfourl.format(labpath)
        if not networkid == None:
            url = ''.join([url, '/', networkid])
        status, message, response = self.REQ(reqtype="get", url = url)
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return [status, message, response['data']]
        # print(f"status code : {response.status_code}")
        # print(response.text)

    def get_node_info(self, labpath=None, nodeid=None):
        if labpath == None:
            labpath = self.config['path']
        url = self.resource.getnodeinfourl.format(labpath)
        if not nodeid==None:
            url = ''.join([url, '/', nodeid])
        status, message, response = self.REQ(reqtype="get", url = url)
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return [status, message, response['data']]
    
    def node_action(self,action, labpath=None, nodeid=None):
        urls =[]
        if labpath == None:
            labpath = self.config['path']
        if nodeid ==None:
            status, message,nodes = self.get_node_info(labpath=labpath) 
            if not status: self.logger.error(message); self.logger.error(nodes); return [status, message, nodes]
            for node in nodes.keys():
                urls.append(self.resource.nodeactionurl.format(labpath, node))
        else:
            urls.append(self.resource.nodeactionurl.format(labpath, nodeid))
        for url in urls:
            if action == "start":
                url = ''.join([url, 'start'])
            if action == "stop":
                url = ''.join([url, 'stop/stopmode=3'])
            status, message, response = self.REQ(reqtype="get", url = url)
            if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]

        return [True, f"Succesfully applied action: '{action}' to nodes - {nodeid if nodeid else 'all nodes'}",response]
            #self.logger.debug(f"{status}, {message}, {response}")
        #print(f"status code : {response.status_code}")
        # print(response)

    def get_lab_topology_info(self,labpath=None):
        if labpath == None:
            labpath = self.config['path']
        status, message, response = self.REQ(reqtype="get", url = self.resource.getlabtopologyurl.format(labpath))
        #self.logger.info(f'{response["status"]} - {response["message"]}')
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return [status, message, response["data"]]
    
    def update_lab_quality(self,config,labpath=None):
        # url = self.resource.updatelinkquality.format(labpath)   
        if labpath == None:
            labpath = self.config['path']     
        status, message, response=self.REQ(reqtype="put",url= self.resource.updatelinkquality.format(labpath),data=config)
        if not status: self.logger.error(message); self.logger.error(response)
        return [status, message, response]
        
    def create_new_lab(self, labname=None, labpath=None):
        if not labpath == None:
            self.resource.createlabpayload['path'] = labpath
        if not labname == None:
            self.resource.createlabpayload['name'] = labname
        
        status, message, response = self.REQ(reqtype="post", url= self.resource.createlaburl, data = self.resource.createlabpayload)
        
        if not status:
            self.resource.createlabpayload =copy.deepcopy(self.config['create_new_lab'])
            self.logger.error(message); self.logger.error(response)
            return [status, message, response]
            #raise Exception(E)
        self.resource.createlabpayload = copy.deepcopy(self.config['create_new_lab'])
        self.logger.info(f"{response['status']} - {self.resource.createlabpayload['name']} {response['message']}")
        return [status, message, response]
    def delete_lab(self,labpath = None):
        if labpath == None:
            labpath = self.config['path']
        status, message, response = self.REQ(reqtype="delete", url= self.resource.getlabinfourl.format(labpath))
        if not status: self.logger.error(message); self.logger.error(response)
        return [status, message, response]
        
    def create_new_node(self, labpath=None,configs = None):
        """configs must be a list"""
        #print(tempnode)
        responsedata = []
        if labpath == None:
            labpath = self.config['path']
        if configs == None:
            configs = self.config['create_new_node']
        status, message, allNodeList= self.get_node_info(labpath)
        if not status: return [status, message, allNodeList]
        for config in configs:
            tempnode = copy.deepcopy(self.resource.createnodepayload)
            status, message, apiData = self.list_images_from_nodetemplate(config["template"])
            if not status: return [status, message,apiData]
            for key in config.keys():
                if key == "type" and config[key] == "qemu":
                    # self.tempnode[key] = config[key]
                    tempnode["qemu_options"] = apiData["qemu"]['options']
                    tempnode["ro_qemu_options"] = apiData["qemu"]['options']
                if config[key] == "":
                    if not apiData["options"].get(key) == None:
                        config[key]= apiData["options"][key]["value"]
                tempnode[key] = config[key]
            exist = False
            if len(allNodeList) > 0:
                for value in allNodeList.values():
                    if tempnode["name"] == value['name']:
                        self.logger.warning(f"Node {tempnode['name']} already exist in the lab")
                        responsedata.append(value['id'])
                        exist = True
            if exist: continue
            status, message, response = self.REQ(reqtype="post", url = self.resource.createnodeurl.format(labpath), data=tempnode)
            if not status:return [status, message, response]
            responsedata.append(response)
            self.logger.info(f"Node {tempnode['name']} created successfully")
        return [True, "Created new nodes", responsedata]
            #return responsedata

    def create_new_network(self, labpath=None, configs=None):
        if labpath== None:
            labpath= self.config['path']
        status, message, allNetworkList = self.get_labnetwork_info(labpath)
        if not status:return [status, message, allNetworkList]
        if configs == None:
            configs = self.config['create_network']
            for config in configs:
                tempnode = copy.deepcopy(self.resource.createnetworkpayload)
                for key in config.keys():
                    tempnode[key] = config[key]
                exist = False
                if len(allNetworkList) > 0:
                    for value in allNetworkList.values():
                        if tempnode['name'] == value['name']:
                            self.logger.warning(f"Network {tempnode['name']} already exist in the lab")
                            exist = True
                if exist: continue
                status, message, response = self.REQ(reqtype="post", url=self.resource.getlabnetworkinfourl.format(labpath), data = tempnode)
                if not status:return [status, message, response]
                self.logger.info(f"Network {tempnode['name']} created successfully")
            return [True, "All Network Nodes created successfully", None]
        else:
            status, message, response = self.REQ(reqtype="post", url=self.resource.getlabnetworkinfourl.format(labpath), data = configs)
            if not status: return [status, message, response]
            self.logger.info("Network defined in custom config created successfully")
            return [status, message, response['data']]
    
    def get_interface_info(self, labpath, nodeid):
        if labpath == None:
            labpath = self.config['path']
        status, message, response = self.REQ(reqtype="get", url = self.resource.interfaceurl.format(labpath, nodeid))
        if not status: self.logger.error(message); self.logger.error(response); return [status, message, response]
        return [status, message, response['data']]

    def link_nodes(self, labpath=None, configs=None):
        """firstnodename = name of the first node\n
            secondnodename = name of the second node or the network name.\n
            if secondnodename is not a node and not a network then by default this script will create a network with secondnodename and link with firstnode
            for configs structure refer to link_network key from config.json in Config directory
        """
        if labpath == None:
            labpath = self.config['path']
        if configs==None:
            configs = self.config['link_nodes']
        
        status, message, allNodeList= self.get_node_info(labpath)
        if not status: return [status, message, allNodeList]
        status, message, allNetworkList = self.get_labnetwork_info(labpath)
        if not status:return [status, message, allNetworkList]
        # print(allNodeList)
        # print("\n")
        # print(allNetworkList)
        
        for config in configs:
            resNode = [False, False]
            resNetwork = False
            for value in allNodeList.values():
                if config['firstnodename'] == value['name']:
                    resNode[0] = value
                if config['secondnodename'] == value['name']:
                    resNode[1] = value
            if not resNode[0] and not resNode[1]: return [False, "Cannot Link two networks, one must be a node", Exception("Cannot link two networks, one must be node")]
            if not resNode[0]: return [False, f"{config['firstnodename']} is not a node", Exception(f"{config['firstnodename']} is not a node")]
            if not resNode[1]:
                for value in allNetworkList.values():
                    if config['secondnodename'] == value['name']:
                        resNetwork= value
                if not resNetwork:return [False, f"{config['secondnodename']} is neither a network or a node", Exception(f"{config['secondnodename']} is neither a network nor a node")]
            status, message,firstinterfaceslst = self.get_interface_info(labpath, nodeid= str(resNode[0]['id']))
            if not status: return [status, message, firstinterfaceslst]
            firstinterfaceslst = firstinterfaceslst['ethernet']
            firstNodeInterfacetoConnect=None; secondNodeInterfacetoConnect = None
            networkid = set()
            for indx in range(len(firstinterfaceslst)):
                if firstinterfaceslst[indx]['network_id'] == 0 and firstNodeInterfacetoConnect == None:
                    firstNodeInterfacetoConnect = str(indx)
                if firstinterfaceslst[indx]['network_id'] != 0:
                    networkid.add(firstinterfaceslst[indx]['network_id'])

            if resNode[0] and resNode[1]:
                status, message, secondinterfaceslst = self.get_interface_info(labpath, nodeid= str(resNode[1]['id']))
                if not status:return [status, message, secondinterfaceslst]
                secondinterfaceslst = secondinterfaceslst['ethernet']
                isConnected=False
                for indx in range(len(secondinterfaceslst)):
                    if secondinterfaceslst[indx]['network_id'] == 0 and secondNodeInterfacetoConnect == None:
                        secondNodeInterfacetoConnect = str(indx)
                    if secondinterfaceslst[indx]['network_id'] in networkid:
                        self.logger.warning(f"Node {config['firstnodename']} and Node {config['secondnodename']} are already linked")
                        isConnected = True
                if isConnected:
                    continue
                assert len(firstNodeInterfacetoConnect) > 0 or len(secondNodeInterfacetoConnect) > 0
                networkpayload = self.resource.createnetworkpayload
                for key in config['network_config'].keys():
                    networkpayload[key] = config['network_config'][key]
                status, message, networkid = self.create_new_network(labpath=labpath, configs=networkpayload)
                if not status: return [status, message, networkid]
                try:
                    self.REQ(reqtype="put", url = self.resource.interfaceurl.format(labpath, resNode[0]['id']), data= {firstNodeInterfacetoConnect: networkid['id']})
                    self.REQ(reqtype="put", url = self.resource.interfaceurl.format(labpath, resNode[1]['id']), data= {secondNodeInterfacetoConnect: networkid['id']})
                    self.REQ(reqtype="put", url=self.resource.getlabnetworkinfourl.format(labpath)+"/"+str(networkid['id']), data = {"visibility":0})
                    self.logger.info(f"Successfully created link between Node {config['firstnodename']} <-----> Node {config['secondnodename']}")
                except Exception as E: status, message, resp = E.args[0]; self.logger.error(message); self.logger.error(resp); return E.args[0]
            else:
                if resNetwork['id'] in networkid: self.logger.warning(f"Node {config['firstnodename']} and Network {config['secondnodename']} are already linked"); continue
                resp = self.REQ(reqtype="put", url = self.resource.interfaceurl.format(labpath, resNode[0]['id']), data= {firstNodeInterfacetoConnect: resNetwork['id']})
                self.logger.info(f"Successfully created link between Node {config['firstnodename']} <-----> Network {config['secondnodename']}")
        return [True, "Successfully linked all Nodes", None]
    def default_config(self, settle_down_time=None):
        self.logger.info(f"Applying default config to lab {self.config['path']}")
        for payload in self.current_lab_topology:
            if "network" not in payload['destination']:
                payload['destination'] = payload['destination'].split("node")[-1]

            if "network" not in payload['source']:
                payload['source'] = payload['source'].split("node")[-1]
            default_config_payload = copy.deepcopy(self.resource.defaultconfig)
            default_config_payload['source_label']= payload['source_label']
            default_config_payload['destination_label']= payload['destination_label']
            default_config_payload['source']=payload['source']
            default_config_payload['destination']= payload['destination']
            default_config_payload['source_interfaceId'] = payload['source_interfaceId']
            default_config_payload["destination_interfaceId"] = payload["destination_interfaceId"]
            status, message, response = self.update_lab_quality(config=default_config_payload)
            if not status: return [status, message, response]
            self.logger.info(f"{message}")
        if settle_down_time:
            self.settle_down(settle_down_time)
        return [True, "Successfully applied default config", None]
    
    def settle_down(self, settle_down_time):
        self.logger.info("Waiting for settle down period to be over...")
        stime = int(time.time())
        while(int(time.time())- stime <= settle_down_time*60):
            time.sleep(1)

    def apply_manual_config(self, config, settle_down_time=None):
        self.logger.info(f"Applying manual config to lab {self.config['path']}")
        if config.get('nodes') is None:
            self.logger.error("Manual config does not have any nodes configurations")
            return [False, "config args does not have valid configuration", None]
        for payload in self.current_lab_topology:
            for nodes in config.get('nodes'):
                nodes_linkconfig = None
                if payload['source_node_name'] == nodes['name']:
                    nodes_linkconfig = nodes.get('linkconfig')
                if nodes_linkconfig:
                    for linkconfig in nodes_linkconfig:
                        if payload['source_label'] == linkconfig['source_label']:
                            if "network" not in payload['destination']:
                                payload['destination'] = payload['destination'].split("node")[-1]

                            if "network" not in payload['source']:
                                payload['source'] = payload['source'].split("node")[-1]
                            
                            manual_payload = copy.deepcopy(self.resource.defaultconfig)
                            for keys, values in manual_payload.items():
                                if payload.get(keys) is not None:
                                    manual_payload[keys]= payload[keys]

                            for keys, values in linkconfig.items():
                                manual_payload[keys] = values
                            status, message, response = self.update_lab_quality(config=manual_payload)
                            if not status: return [status, message, response]
                            self.logger.info(f"{message}")
        if settle_down_time:
            self.settle_down(settle_down_time)
        return [True, "Successfully applied manual config", None]

