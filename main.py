# 通过jotform 同步提交数据
import sys
import requests
import dataset
import json


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
        limit = 5
        results = []
        while True:
            x = self.get_form_submissions(formID, offset, limit)
            results.extend(x)
            offset += limit
            if len(x) != limit:
                break
        return results


class JotFormSaver(object):
    def __init__(self, db):
        self.__db = db
    def to_tablename(self, name):
        return name.strip().replace(' ', '_').replace('.', '')
        
    def submission_to_dict(self, submission):
        # 提交变字典
        """         
        answers = submission.pop('answers')
        for _, info in answers.items():
            if 'answer' in info and 'name' in info:
                if isinstance(info['answer'],str):
                    submission[self.to_tablename('a_{}'.format(info['name']))] = info['answer']
                elif isinstance(info['answer'],list):
                    submission[self.to_tablename('a_{}'.format(info['name']))] = '|'.join(info['answer'])
                elif isinstance(info['answer'],dict):
                    for k,v in info['answer'].items():
                        submission[self.to_tablename('a_{}_{}'.format(info['name'], k))] = v 
        """
        
        dic = {}
        dic['id'] = submission.pop('id')
        dic['form_id'] = submission.pop('form_id')
        dic['data'] = json.dumps(submission)
        return dic

    def saveSubmission(self, submission):
        dic = self.submission_to_dict(submission)
        self.__db['submission'].upsert(dic, ['id'])


class JotFormTxtSaver(object):
    def __init__(self):
        self.f = open('data.txt','w+')

    def saveSubmission(self, submission):
        self.f.write(json.dumps(submission))
        self.f.write('\n')


def main():
    db = dataset.connect('sqlite:///data.db')
    jot = JotFormAPI(sys.argv[1])
    saver = JotFormSaver(db)
    # saver = JotFormMongoSaver()
    # saver = JotFormTxtSaver()
    forms = jot.get_forms()
    print('total forms {}'.format(len(forms)))
    for form in forms:
        submissions = jot.get_form_all_submissions(form['id'])
        print('form {}, total submissions {}'.format(
            form['id'], 
            len(submissions)))
        for item in submissions:
            table = 'submissions_{}'.format(form['id'])
            saver.saveSubmission(item)
        


if __name__ == '__main__':
    main()