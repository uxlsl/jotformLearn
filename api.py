import requests
import json


class JotFormAPI(object):
    def __init__(self, APIKey):
        self.__APIKey = APIKey
        self.__session = requests.Session()

    def get_forms(self):
        headers = {"APIKEY": self.__APIKey}
        ret = self.__session.get(
            "https://api.jotform.com/user/forms?limit=1000", headers=headers
        ).json()
        if ret.get("message", "") == "success":
            return ret["content"]
        else:
            return []

    def get_form_submissions(self, formID, offset=0, limit=100):
        # 一次拿结果有限制
        print("get_form_submission", formID, offset, limit)
        url = "https://api.jotform.com/form/{}/submissions?apiKey={}&&offset={}&limit={}".format(
            formID, self.__APIKey, offset, limit
        )
        ret = self.__session.get(url).json()
        if ret.get("message", "") == "success":
            print("total submission {}".format(len(ret["content"])))
            return ret["content"]
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
        for k, v in data.items():
            submission["submission[{}]".format(k)] = v
        print(form_id, data)
        r = self.__session.post(
            "https://api.jotform.com/form/{}/submissions?apiKey={}".format(
                form_id, self.__APIKey
            ),
            data=submission,
        )
        print(r.text)
        return r.json()


class PipedriveAPI(object):
    def __init__(self, api_token, company_domain):
        self.__api_token = api_token
        self.__company_domain = company_domain
        self.__session = requests.Session()

    def createDeal(self, deal):
        """
            deal need title, org_id
        """
        url = "https://{}.pipedrive.com/api/v1/deals?api_token={}".format(
            self.__company_domain, self.__api_token
        )
        r = self.__session.post(url, data=deal)
        return r.json()

    def searchPerson(self, term):
        """
        {'additional_data': {'pagination': {'limit': 100,
            'more_items_in_collection': False,
   'start': 0}},
        'data': {'items': [{'item': {'custom_fields': [],
     'emails': [],
     'id': 4,
     'name': 'foobar',
     'notes': [],
     'organization': None,
     'owner': {'id': 11591795},
     'phones': ['18613077154'],
     'type': 'person',
     'visible_to': 3},
    'result_score': 0.29955},
   {'item': {'custom_fields': [],
     'emails': [],
     'id': 5,
     'name': 'foobar1',
     'notes': [],
     'organization': None,
     'owner': {'id': 11591795},
     'phones': ['18613077154'],
     'type': 'person',
     'visible_to': 3},
    'result_score': 0.09985},
   {'item': {'custom_fields': [],
     'emails': ['1234138225@qq.com'],
     'id': 6,
     'name': 'foobar3',
     'notes': [],
     'organization': None,
     'owner': {'id': 11591795},
     'phones': ['18613077154'],
     'type': 'person',
     'visible_to': 3},
    'result_score': 0.09985}]},
 'success': True}

        """
        url = "https://api.pipedrive.com/v1/persons/search?term={}&start=0&api_token={}".format(
            term, self.__api_token
        )
        r = self.__session.get(url)
        return r.json()

    def addPerson(
        self,
        name,
        owner_id=None,
        org_id=None,
        email=[],
        phone=[],
        visible_to=None,
        add_time=None,
    ):
        """
        比如
        {'data': {'active_flag': True,
  'activities_count': 0,
  'add_time': '2020-06-28 06:04:13',
  'cc_email': 'foobar3@pipedrivemail.com',
  'closed_deals_count': 0,
  'company_id': 7606179,
  'done_activities_count': 0,
  'email': [{'primary': True, 'value': ''}],
  'email_messages_count': 0,
  'files_count': 0,
  'first_char': 'l',
  'first_name': 'lsl',
  'followers_count': 0,
  'id': 8,
  'label': None,
  'last_activity_date': None,
  'last_activity_id': None,
  'last_incoming_mail_time': None,
  'last_name': None,
  'last_outgoing_mail_time': None,
  'lost_deals_count': 0,
  'name': 'lsl',
  'next_activity_date': None,
  'next_activity_id': None,
  'next_activity_time': None,
  'notes_count': 0,
  'open_deals_count': 0,
  'org_id': None,
  'org_name': None,
  'owner_id': {'active_flag': True,
   'email': 'lin.sl.0001@gmail.com',
   'has_pic': 0,
   'id': 11591795,
   'name': '松林',
   'pic_hash': None,
   'value': 11591795},
  'owner_name': '松林',
  'participant_closed_deals_count': 0,
  'participant_open_deals_count': 0,
  'phone': [{'primary': True, 'value': ''}],
  'picture_id': None,
  'related_closed_deals_count': 0,
  'related_lost_deals_count': 0,
  'related_open_deals_count': 0,
  'related_won_deals_count': 0,
  'undone_activities_count': 0,
  'update_time': '2020-06-28 06:04:13',
  'visible_to': '3',
  'won_deals_count': 0},
 'related_objects': {'user': {'11591795': {'active_flag': True,
    'email': 'lin.sl.0001@gmail.com',
    'has_pic': 0,
    'id': 11591795,
    'name': '松林',
    'pic_hash': None}}},
 'success': True}
        """
        print("add Persion")
        url = "https://{}.pipedrive.com/api/v1/persons?api_token={}".format(
            self.__company_domain, self.__api_token
        )
        data = {"name": name, "email": email, "phone": phone}
        if owner_id is not None:
            data["owner_id"] = owner_id
        if org_id is not None:
            data["org_id"] = org_id
        if visible_to is not None:
            data["visible_to"] = visible_to
        if add_time is not None:
            data["add_time"] = add_time
        r = self.__session.post(url, data=data)
        return r.json()

    def GetAllDealFields(self):
        """
        {"success":True, "data":[]}
        """
        url = 'https://api.pipedrive.com/v1/dealFields?start=0&api_token={}'.format(self.__api_token)
        r = self.__session.get(url)
        return r.json()

    def AddDealFields(self, name, field_type="varchar"):
        print('AddDealField')
        url = 'https://api.pipedrive.com/v1/dealFields?api_token={}'.format(self.__api_token)
        r = self.__session.post(url, data={'name':name,'field_type': field_type})
        return r.json()


if __name__ == "__main__":
    pd = PipedriveAPI("0468eeb9486ccea96c0f65b6029b5bb9f9532c0d", "foobar3")
    r = pd.createDeal({"title": "hello foobar", "org_id": 1})
    print(r)
