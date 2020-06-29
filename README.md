# jotform及pipedirve学习

1. 使用jotform api 接口下载提交数据到数据库
2. 提交数据jotform api并把submission_id 相关信息也提交到pipedrive中


## 安装

```

python3 -m venv .venv
source .venv/bin/activ
pip install -r requirements.txt

```

## 使用

下载所有提交数据

```

python download.py apiKey

```

提交用户信息到jotform上,并传到pipedrive上

```
python submit.py apiKey form_id  lin lin@163.com 159921658712 2021-01-01 pipedrive_api_token,company_domain

```


## jotform api

GET /user/forms

```

    curl -H "APIKEY: 4424e671aec8c87a27f6b761cd3d01fa" "https://api.jotform.com/user/forms"

```

GET /form/{id}/submissions

```

 curl -X GET "https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}"

```

POST /form/{id}/submissions


```

curl -X POST -d "submission[1]=answer of Question 1" -d "submission[2_first]=First Name" -d "submission[2_last]=Last Name" "https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}"


```

## pipedrive api

新建 Person
```

https://developers.pipedrive.com/docs/api/v1/#!/Persons/post_persons


```

## TODO
+ 错误逻辑处理

## 参考

+ jotform api网站https://api.jotform.com/docs/
+ pipedirve https://pipedrive.readme.io/docs/creating-a-deal
+ pipedirve https://developers.pipedrive.com/docs/api/v1/
