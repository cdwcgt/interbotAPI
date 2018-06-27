# -*- coding: utf-8 -*-
import re
import json
import logging
import requests
from commLib import interMysql

class msgHandler():

    def __init__(self, context):
        self.context = context
        self.localhost = '127.0.0.1'

    def auto(self):
        msg = self.context['message']
        msg = msg.replace('！', '!')
        if '!' in msg:
            return self.autoApi(msg)
        else:
            return self.autoReply(msg)

    def autoApi(self, msg):
        """api检测，自动调用"""
        cmd = self.extractCmd(msg)
        res = self.getCmdRef(cmd)
        if not res:
            return ''

        if 'http' not in res['location']:
            apiUrl = 'http://{host}/{location}{api}'.format(
                    host = self.localhost,
                    location = res['location'],
                    api = res['url']
                )
        else:
            apiUrl = '{location}{api}'.format(
                    location = res['location'],
                    api = res['url']
                )

        iargs = self.extractArgs(msg, cmd)
        res = requests.post(apiUrl, data={"iargs": json.dumps(iargs)})
        if res.status_code == 200 and res.text:
            return res.text
        logging.info('调用[%s]异常' % apiUrl)
        return ''
        
    def extractArgs(self, msg, cmd):
        """参数提取"""
        args = []
        effmsg = msg[msg.find(cmd):]
        l = effmsg.split(' ')
        if len(l) > 1:
            args = l[1:]
        return args

    def autoReply(self, msg):
        """自动回复，非特殊指令性"""
        retmsg = ''
        fmsg = self.filterCN(msg)
        fmsg = fmsg.replace(' ', '')
        if len(msg) == len(fmsg):
            res = self.getCmdRef(fmsg)
            if res:
                retmsg = res['reply']
        return retmsg

    def extractCmd(self, msg):
        """命令提取"""
        retcmd = None
        p = re.compile('!\w+')
        cmds = p.findall(msg)
        if cmds:
            retcmd = cmds[0]
        logging.info('提取的cmd[%s]', retcmd)
        return retcmd

    def filterCN(self, content):
        """过滤中文"""
        pat = re.compile('[\u4e00-\u9fa5]')
        ret = pat.sub('', content)
        return ret

    def getCmdRef(self, cmd):
        """映射"""
        db = interMysql.Connect('osu2')
        sql = '''
            SELECT cmd, url, location, reply
            FROM cmdRef WHERE cmd = %s
        '''
        res = db.query(sql, [cmd])
        if not res:
            return ''
        return res[0]
