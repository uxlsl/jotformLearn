import requests


class JotFormAPI(object):
    def __init__(self, APIKey):
        self.__APIKey = APIKey
        self.__session = requests.Session()

    def get_forms(self):
        headers = {'APIKEY': self.__APIKey}
        ret =  self.__session.get('https://api.jotform.com/user/forms?limit=1000',
            headers=headers).json()
        if ret.get('message', '') == 'success':
            return ret['content']
        else:
            return []

    def get_form_submissions(self, formID, offset=0,limit=100):
        # 一次拿结果有限制
        print('get_form_submission', formID, offset, limit)
        url = 'https://api.jotform.com/form/{}/submissions?apiKey={}&&offset={}&limit={}'.format(
            formID, self.__APIKey, offset, limit)
        ret = self.__session.get(url).json()
        if ret.get('message', '') == 'success':
            print('total submission {}'.format(len(ret['content'])))
            return ret['content']
        else:
            return []

    def get_form_all_submissions(self, formID):
        offset = 0
        limit = 1000
        results = []
        while True:
            x = self.get_form_submissions(formID, offset, limit)
            results.extend(x)
            offset += limit
            if len(x) != limit:
                break
        return results