import os
import sys
import requests
import json


#config, username, password, session auth, req, session
class Eve:
    def __init__(self, serveripaddr, configdata):
    #------------------authenticating user to evengserver---------------------
        self.loginurl = "https://{}/api/auth/login".format(serveripaddr)
        self.loginheader = {
            'Host': serveripaddr,
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.loginpayload = configdata['creds']
        
    #------------------revoking authentication of user to evengserver---------------------
        self.logouturl = "https://{}/api/auth/logout".format(serveripaddr)

    #------------------Get User info from evengserver---------------------
        self.getuserinfourl = "https://{}/api/auth".format(serveripaddr)
        self.userinfoheader = {
            'Host': serveripaddr,
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9', 
        }

    #------------------Check Session active using poll api---------------------
        self.pollurl = "https://{}/api/poll".format(serveripaddr)
        self.pollheader = {
            'Host': serveripaddr,
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9', 
        }

    #----------------------------Get System Status-------------------------
        self.systemstatusurl = "https://{}/api/status".format(serveripaddr)

    #---------------------------List all node templates----------------------------
        self.listnodetempurl = "https://{}/api/list/templates/".format(serveripaddr)

    #---------------------------List all images for a single node template--------------------------
        self.imgfromnodetemplateurl = "https://{}/api/list/templates/{}".format(serveripaddr, "{}")

    #----------------------List all contents within a folder----------------------------
        self.listallcontenturl = "https://{}/api/folders/{}".format(serveripaddr, "{}")

    #----------------------List all users (only for admin users else it will list the current user logged in)----------------------------
        self.listalluserurl = "https://{}/api/users/".format(serveripaddr)

    #----------------------get lab information----------------------------
        self.getlabinfourl = "https://{}/api/labs/{}".format(serveripaddr, "{}")

    #----------------------get info of existing networks in a specific lab / create lab network----------------------------
        self.getlabnetworkinfourl = "https://{}/api/labs/{}/networks".format(serveripaddr, "{}")
        self.createnetworkpayload = {"count":1,"name":"","type":"","left":702,"top":409,"visibility":1,"postfix":0}

    #----------------------get info of all/single existing nodes in a specific lab (specified node id in code)----------------------------
        self.getnodeinfourl = "https://{}/api/labs/{}/nodes".format(serveripaddr, "{}")

    #----------------------start or stop a specific node----------------------------
        self.nodeactionurl = "https://{}/api/labs/{}/nodes/{}/".format(serveripaddr, "{}", "{}")

    #-------------------------create new lab---------------------------------------------------
        self.createlaburl = "https://{}/api/labs".format(serveripaddr)
        self.createlabpayload = configdata['create_new_lab']

    #---------------------------create new windows node -----------------------------
        self.createnodeurl = "https://{}/api/labs/{}/nodes".format(serveripaddr, "{}")
        self.createnodepayload =   {"template": "", "type": "", "count": "1", "image": "", "name": "",
                                    "icon": "", "uuid": "", "cpulimit": "undefined", "cpu": "", "ram": "", "ethernet": "", "firstmac": "",
                                    "qemu_version": "", "qemu_arch": "", "qemu_nic": "",
                                    "qemu_options": "",
                                    "ro_qemu_options": "",
                                    "config": "0", "sat": "0", "delay": "0", "console": "", "rdp_user": "", "rdp_password": "", "left": "468", "top": "422", "postfix": 0
                                    }
        
        
    #-------------------------get lab topology--------------------------------------------------------#
        self.getlabtopologyurl = "https://{}/api/labs/{}/topology".format(serveripaddr, "{}")
        
    #-------------------------update lab quality link-----------------------------------------------------
        self.updatelinkquality = "https://{}/api/labs/{}/quality".format(serveripaddr,"{}")

    #-------------------------Get/Update Interface-----------------------------------------------------
        self.interfaceurl = "https://{}/api/labs/{}/nodes/{}/interfaces".format(serveripaddr, "{}", "{}")
        
    #-------------------------Update network -------------------------------------------------------------
        self.updatenetworkurl = "https://{}/api/labs/{}/networks{}".format(serveripaddr, "{}", "{}")

    
    #-------------------------Default config payload ------------------------------------------------------
        self.defaultconfig = {
        "source_label": "",
        "source_delay": "0",
        "source_jitter": "0",
        "source_loss": "0",
        "source_bandwidth": "0",
        "destination_label": "",
        "destination_delay": "0",
        "destination_jitter": "0",
        "destination_loss": "0",
        "destination_bandwidth": "0",
        "source": "",
        "destination": "",
        "source_interfaceId": "",
        "destination_interfaceId": "",
        "save": "1"
    }