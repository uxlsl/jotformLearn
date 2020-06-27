"""
    提交用户信息
"""
import sys
import fire
from api import JotFormAPI,PipedriveAPI


def main(apikey,form_id,name,email,phone,Datetime,pipedrive_api_token=None,company_domain=None):
    jot = JotFormAPI(apikey)
    userinfo = {'56':name,'59':email,'190':phone, '191':Datetime}
    ret = jot.submit(form_id, userinfo)
    print('jot result', ret)
    if pipedrive_api_token is not None and company_domain is not None:
        pd = PipedriveAPI(pipedrive_api_token, company_domain)
        userinfo['submissionID'] = ret['content']['submissionID']
        r = pd.createDeal(userinfo)
        print(r)


if __name__ == "__main__":
    fire.Fire(main)
