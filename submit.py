"""
    提交用户信息
"""
import sys
from datetime import datetime
import fire
from pprint import pprint
from api import JotFormAPI, PipedriveAPI


def findOrAddPerson(pd, name, email, phone):
    ret = pd.searchPerson(name)
    for item in ret["data"]["items"] if ret["success"] else []:
        persion = item["item"]
        if (
            name == persion["name"]
            and email in persion["emails"]
            and phone in persion["phones"]
        ):
            print("find persion")
            pprint(persion)
            return persion
    else:
        ret = pd.addPerson(name, email=[email], phone=[phone])
        if ret["success"]:
            return ret["data"]
        else:
            print("add perion fail")
            # TODO
            return


def findOrAddDealField(pd, name):
    ret = pd.GetAllDealFields()
    for i in ret['data'] if ret['success'] else []:
        if i['name'] == 'submissionID':
            return i['key']
    else:
        ret = pd.AddDealFields(name)
        if ret['success']:
            return ret['data']['key']
        else:
            # TODO
            pass
        

def main(
    apikey,
    form_id,
    name,
    email,
    phone,
    Datetime,
    pipedrive_api_token=None,
    company_domain=None,
):
    jot = JotFormAPI(apikey)
    # TODO
    phone = str(phone)
    userinfo = {"56": name, "59": email, "190": phone, "191": Datetime}
    ret = jot.submit(form_id, userinfo)
    print("jot result")
    pprint(ret)
    submissionID = ret['content']['submissionID']
    if pipedrive_api_token is not None and company_domain is not None:
        pd = PipedriveAPI(pipedrive_api_token, company_domain)
        person = findOrAddPerson(pd,name,email,phone)
        person_id = person['id']
        print("persion_id", person_id)
        deal = {
            "title": "{} name->{},phone->{}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, phone
            ),
            "person_id": person_id,
        }
        # userinfo['submissionID'] = ret['content']['submissionID']
        key = findOrAddDealField(pd, 'submissionID')
        deal[key] = submissionID
        r = pd.createDeal(deal)
        pprint(r)


if __name__ == "__main__":
    fire.Fire(main)
