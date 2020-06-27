"""
    提交用户信息
"""
import sys
from api import JotFormAPI


def main():
    """
        假设正确输入
        apikey,form_id,name,email,phone,Datetime
    """
    jot = JotFormAPI(sys.argv[1])
    form_id, name,email,phone,Datetime = sys.argv[2:]
    ret = jot.submit(form_id,{'56':name,'59':email,'190':phone, '191':Datetime})
    print(ret)


if __name__ == "__main__":
    main()
