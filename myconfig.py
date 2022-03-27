import datetime
import re
import time
from urllib.parse import quote

from cqu_auth import Config


class PhoneConfig(Config):
    def __init__(self, addr: str = None, headers: dict = None, params: dict = None, data=None):
        super(PhoneConfig, self).__init__()
        self.common_header.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; NOH-AN00 Build/HUAWEINOH-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 wisedu/3.0.0 cpdaily/9.0.20 wisedu/9.0.20'
        })
        self.update(addr, headers, params, data)
        self.headers_json = {
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    @staticmethod
    def assert_resp_json_code(resp):
        assert resp.json()['code'] == '0', resp.json()


class _ConfigWEU(PhoneConfig):
    # get _WEU，跟route没什么关系
    def __init__(self):
        super(_ConfigWEU, self).__init__()
        self.url1 = 'http://i.cqu.edu.cn/qljfwapp4/sys/lwStuReportEpidemic/*default/index.do'
        self.headers1 = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'X-Requested-With': 'com.wisedu.cpdaily',
        }
        self.url2 = 'http://i.cqu.edu.cn/qljfwapp4/sys/lwpub/mobile/api/authenticated/funauth/users/roles.do'
        self.headers2 = self.headers_json
        self.url3 = 'http://i.cqu.edu.cn/qljfwapp4/sys/lwpub/mobile/api/authenticated/users/setupRole.do'
        self.headers3 = self.headers_json

    def default_method(self, session, **kwargs):
        print('获取cookie中...')
        self.update(self.url1, self.headers1)
        resp = self._get(session, **kwargs)

        APPID = re.search(r"APPID='(\d+)'", resp.text).group(1)
        APPNAME = 'lwStuReportEpidemic'
        data = 'data={"APPID":"%s","APPNAME":"%s"}' % (APPID, APPNAME)
        self.update(self.url2, self.headers2, data=data)
        resp = self._post(session, **kwargs)

        self.assert_resp_json_code(resp)
        ROLEID = resp.json()['data'][0]['id']
        data = 'data={"APPID":"%s","APPNAME":"%s","ROLEID":"%s"}' % (APPID, APPNAME, ROLEID)

        self.update(self.url3, self.headers3, data=data)

        return self._post(session, **kwargs)


class _ConfigDataTemplate(PhoneConfig):
    # get last webform data as template
    def __init__(self):
        super(_ConfigDataTemplate, self).__init__()
        url = 'http://i.cqu.edu.cn/qljfwapp4/sys/lwStuReportEpidemic/modules/healthClock/getMyDailyReportDatas.do'
        data = 'pageNumber=1&pageSize=1&*order=-CREATED_AT&'.encode()
        self.update(url, self.headers_json, data=data)

    def default_method(self, session, **kwargs):
        return self._post(session, **kwargs)

    def get_template(self, session, **kwargs):
        print('获取上次打卡记录中...')
        resp = self.default_method(session, **kwargs)
        self.assert_resp_json_code(resp)
        d = resp.json()['datas']['getMyDailyReportDatas']['rows'][0]
        new_d = dict(CHECKED='', CHECKED_DISPLAY='请选择', CZR='', CZZXM='')
        d.update(new_d)
        return d


class _ConfigServerTime(PhoneConfig):
    # get server time
    def __init__(self):
        super(_ConfigServerTime, self).__init__()
        url = 'http://i.cqu.edu.cn/qljfwapp4/sys/lwpub/api/getServerTime.do'
        headers = {
            "Accept": 'application/json, text/javascript, */*; q=0.01',
            "X-Requested-With": 'XMLHttpRequest',
            "Origin": 'http://i.cqu.edu.cn',
            "Referer": 'http://i.cqu.edu.cn/qljfwapp4/sys/lwStuReportEpidemic/*default/index.do',
        }
        self.update(url, headers)

    def default_method(self, session, **kwargs):
        v = session.cookies.pop('CASTGC')
        session.cookies.set('CASTGC', v, domain='i.cqu.edu.cn', path='/qljfwapp4/')
        session.cookies.set('AUTHTGC', v, domain='i.cqu.edu.cn', path='/qljfwapp4/')
        session.cookies.set('EMAP_LANG', 'zh', domain='i.cqu.edu.cn', path='/qljfwapp4/')
        return self._post(session, **kwargs)

    def get_servertime(self, session, **kwargs):
        resp = self.default_method(session, **kwargs)
        # self.assert_resp_json_code(resp) # 不返回code
        try:
            resp.json()['date']
        except Exception:
            print('get_servertime 错误：%s\n返回本地时间' % resp.text)
            return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        return resp.json()['date']


class _ConfigWID(PhoneConfig):
    # get post params: today's WID
    def __init__(self):
        super(_ConfigWID, self).__init__()
        url = 'http://i.cqu.edu.cn/qljfwapp4/sys/lwStuReportEpidemic/modules/healthClock/getMyTodayReportWid.do'
        data = 'pageNumber=1'.encode()
        self.update(url, self.headers_json, data=data)

    def default_method(self, session, **kwargs):
        return self._post(session, **kwargs)

    def getWID(self, session, **kwargs):
        resp = self.default_method(session, **kwargs)
        self.assert_resp_json_code(resp)
        items = resp.json()['datas']['getMyTodayReportWid']['rows'][0]
        WID = items['WID']
        return WID


class ConfigReport(PhoneConfig):
    def __init__(self):
        super(ConfigReport, self).__init__()
        url = 'http://i.cqu.edu.cn/qljfwapp4/sys/lwStuReportEpidemic/modules/healthClock/T_HEALTH_DAILY_INFO_SAVE.do'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://i.cqu.edu.cn',
            'Referer': 'http://i.cqu.edu.cn/qljfwapp4/sys/lwStuReportEpidemic/*default/index.do',
        }

        self.update(url, headers)
        self.confWEU = _ConfigWEU()
        self.confWID = _ConfigWID()
        self.confServerTime = _ConfigServerTime()
        self.confDataTemplate = _ConfigDataTemplate()

    def default_method(self, session, **kwargs):
        self.confWEU.default_method(session, **kwargs)
        self.data = self.get_data(session, **kwargs)
        print('提交打卡数据中...')
        resp = self._post(session, **kwargs)
        self.assert_resp_json_code(resp)
        return resp

    def get_data(self, session, **kwargs):
        # 其他参数从以前提交的记录里获取
        data = self.confDataTemplate.get_template(session, **kwargs)
        print('构造本次打卡数据中...')
        # with open('data.txt', 'r') as f:
        #     line = f.read()
        # data = {}
        # for s in line.split('&'):
        #     if s:
        #         k, v = s.split('=')
        #         data[k] = unquote(v)

        curr_date = time.strftime("%Y-%m-%d", time.localtime())
        curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        server_time = self.confServerTime.get_servertime(session, **kwargs)
        server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(server_time, "%Y/%m/%d %H:%M:%S"))

        prev_date = datetime.date.today() - datetime.timedelta(days=1)
        prev_time = datetime.time(23, 57, 15)
        prev_datetime = datetime.datetime.combine(prev_date, prev_time)
        prev_datetime = prev_datetime.strftime("%Y-%m-%d %H:%M:%S")

        FILL_TIME = curr_time
        NEED_CHECKIN_DATE = curr_date
        CREATED_AT = server_time
        CZRQ = prev_datetime
        # 需要动态获取WID，否则会替换掉之前的记录
        # 3-26: DB0B051C7FE511BEE05366D614AC032D
        # 3-27: DB164395E8DC0D50E05366D614ACFFC0
        WID = self.confWID.getWID(session, **kwargs)

        data['FILL_TIME'] = FILL_TIME
        data['NEED_CHECKIN_DATE'] = NEED_CHECKIN_DATE
        data['CREATED_AT'] = CREATED_AT
        data['CZRQ'] = CZRQ
        data['WID'] = WID
        data = '&'.join(['='.join([k, quote(v) if v else '']) for k, v in data.items()]) + '&'
        data_bytes = data.encode()
        return data_bytes
