# 通过jotform 同步提交数据
import sys
import requests


class JotFormAPI(object):
    def __init__(self, APIKey):
        self.__APIKey = APIKey
        self.__session = requests.Session()

    def get_forms(self):
        headers = {'APIKEY': self.__APIKey}
        ret =  self.__session.get('https://api.jotform.com/user/forms', 
            headers=headers).json()
        if ret.get('message', '') == 'success':
            return ret['content']
        else:
            return []
    
    def get_form_submissions(self, formID, offset=0,limit=10):
        # 一次拿结果有限制
        url = 'https://api.jotform.com/form/{}/submissions?apiKey={}&&offset={}&limit={}'.format(
            formID, self.__APIKey, offset, limit)
        ret = self.__session.get(url).json()
        if ret.get('message', '') == 'success':
            return ret['content']
        else:
            return []
    
    def get_form_all_submissions(self, formID):
        offset = 0
        results = []
        while True:
            x = self.get_form_submissions(formID, offset)
            if len(x) == 0:
                break
            results.extend(x)
            offset += 10
        return results
    

def main():
    jot = JotFormAPI(sys.argv[1])
    forms = jot.get_forms()
    print('total forms {}'.format(len(forms)))
    for form in forms:
        submissions = jot.get_form_all_submissions(form['id'])
        print('form {}, total submissions {}'.format(
            form['id'], 
            len(submissions)))


if __name__ == '__main__':
    main()