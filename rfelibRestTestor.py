# encoding=utf-8
import json
import re
from unittest import TestCase
from unittest.util import safe_repr
import requests
from jsonpath_rw import parse


class rfelibRestTestor(TestCase):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'

    def __init__(self):
        self.s = requests.session()

    def assertDictContainsSubset(self, expected, actual, asserttype=1, msg=None):
        """
        Checks whether actual is a superset of expected\n
        :param expected: expect obj;\n
        :param actual: actual obj;\n
        :param asserttype: int 1\2 精确匹配：1 模糊匹配：2\n
        :param msg: Error massage\n
        :return:
        """
        missing = []
        mismatched = []
        for key, value in expected.iteritems():
            if key not in actual:
                missing.append(key)
            elif value != actual[key]:
                if type(value) != type(actual[key]):
                    mismatched.append(
                        '%s, expected: %s, actual: %s' % (safe_repr(key), safe_repr(value), safe_repr(actual[key])))
                else:
                    if isinstance(value, dict):
                        self.assertDictContainsSubset(value, actual[key], int(asserttype))
                        continue
                    if asserttype == 1:
                        # 做正则表达式的判断
                        if isinstance(value, str):
                            if '!@' in value:
                                r = value[2:]
                                if re.match(r, actual[key]) is not None:
                                    continue
                            # 根据不同值类型打印信息
                            mismatched.append('key[%s] value assert fail' % (safe_repr(key)))
        if not (missing or mismatched):
            return
        standardMsg = ''
        if missing:
            standardMsg = 'Missing:%s' % ';'.join(safe_repr(m) for m in missing)
        if mismatched:
            if standardMsg:
                standardMsg += ';'
            standardMsg += 'Mismatched values: %s' % ';'.join(mismatched)
        self.fail(self._formatMessage(msg, standardMsg))

    def reqByParams(self, method, url, params=None, headers=None, cookies=None):
        """
        通过 Params 的方式发起请求\n
        :param method: post\get\...\n
        :param url: str\n
        :param params: dictionary\n
        :param headers: dictionary\n
        :param cookies: RequestsCookieJar\n
        :return: response_obj
        """
        res = self.s.request(method.upper(), url, params=params, headers=headers, cookies=cookies)
        return res

    def reqByForm(self, method, url, form=None, headers=None, cookies=None):
        """
        通过 Form 的方式发起请求\n
        :param method: post\get\...\n
        :param url: str\n
        :param form: dictionary\n
        :param headers: dictionary\n
        :param cookies: response_obj
        :return: response_obj
        """
        res = self.s.request(method.upper(), url, form=form, headers=headers, cookies=cookies)
        return res

    def reqByJson(self, method, url, json=None, headers=None, cookies=None):
        """
        通过 Json 的方式发起请求\n
        :param method: post\get\...\n
        :param url: str\n
        :param form: dictionary\n
        :param headers: dictionary\n
        :param cookies: response_obj
        :return: response_obj
        """
        res = self.s.request(method.upper(), url, json=json, headers=headers, cookies=cookies)
        return res

    def getValueFromJson(self, str_json, jsonpath):
        """
        获取json中某个key对应的value\n
        :param str_json: str json\n
        :param jsonpath: str jsonpath\n
        :return: obj 通过jsonpath在json中得到的value 可能是 int str obj ...\n
        """
        jsonxpr = parse(jsonpath)
        return jsonxpr.find(json.loads(str_json))[0].value
