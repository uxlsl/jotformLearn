import requests
import json

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


    def submit(self, form_id, data):
        """
        curl -X POST -d "submission[1]=answer of Question 1" -d "submission[2_first]=First Name" -d "submission[2_last]=Last Name" "https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}"
        data 字典 {1:1, 2:2}
        """
        submission = {}
        for k,v in data.items():
            submission['submission[{}]'.format(k)] = v
        print(form_id, data)
        r = self.__session.post('https://api.jotform.com/form/{}/submissions?apiKey={}'.format(form_id,self.__APIKey),data=submission)
        print(r.text)
        return r.json()


class PipedriveAPI(object):
    def __init__(self, api_token, company_domain):
        self.__api_token = api_token
        self.__company_domain = company_domain
        self.__session = requests.Session()

    def createDeal(self, data):
        """
            deal need title, org_id
        """
        deal = {}
        deal['title'] = json.dumps(data)
        deal['org_id'] = 'Your company domain goes here'
        url = 'https://{}.pipedrive.com/api/v1/deals?api_token={}'.format(self.__company_domain,self.__api_token)
        r = self.__session.post(url, data=deal)
        return r.json()


if __name__ == '__main__':
    pd = PipedriveAPI('0468eeb9486ccea96c0f65b6029b5bb9f9532c0d', 'foobar3')
    r = pd.createDeal({'title':'hello foobar', 'org_id': 1})
    print(r)