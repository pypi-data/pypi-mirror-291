# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_addfriend']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1', 'nonebot2>=2.0.0-beta.1']

setup_kwargs = {
    'name': 'nonebot-plugin-addfriend',
    'version': '2.5.6',
    'description': '一个基于NoneBot2的插件，用于处理被请求加QQ好友和QQ群的请求.A plugin based on nonebot2, which is used to process requests to add QQ friends and QQ requests.',
    'long_description': '# nonebot_plugin_addFriend\n## 一个基于NoneBot2的插件，用于处理被请求加QQ好友和QQ群的请求\n\n\nA plug-in based on nonebot2, which is used to process the request to add QQ friends and QQ groups\n\n## 如果版本更新请按模板手动配置config.json文件中的新增项和键名更改项，如果不介意原来配置初始化，可以删掉重新生成。修改config.json 时，如果使用vscode的话推荐使用prettier插件格式化，自带的也行\n\n下载方法(做得粗糙，可能有bug，不过应该也没bug了):\n\n    pip install nonebot_plugin_addFriend\n\n单个机器人代码下载方法(旧版，大概没bug)：\n\n    pip install nonebot_plugin_addFriend==2.4.7\n\n\n\n多个机器人配置原理：\n\n初始配置文件为{}，每多一个机器人触发插件，便会以其id即QQ号为索引在配置中生成该机器人的配置\n\n\n\n总的来说有如下几种主动命令：\n\n/重载配置\n\n/更改自动同意,/更改最大加数量,/更改查看加返回数量,/更改加时间,/更改加时间单位(群聊、好友)\n\n/同意加,/拒绝加,/查看加(群聊、好友)\n\n/清理请求表\n\n/重置请求次数(群聊、好友)\n\n/添加请求接收者,/删除请求接收者\n\n\n\n解释如下：\n\n1.该插件运行后会检查配置文件是否存在，并生成默认配置，也可手动复制内容创建文件，创建路径为插件目录，文件名为config.json,其中.json为后缀名，表征文件类型，请不要创建为config.json.json文件，\n\n2.可自行设置是否同意自动加好友，命令为/更改自动同意群聊 1、/更改自动同意好友 0、/更改自动同意 1 1   1是同意,0是不同意\n\n同时，也可以重置当时间段好友请求的数量 /重置请求次数(群聊、好友) 数量（不写默认重置日被请求次数为零，后缀数字则会重置为该数值，(群聊、好友)是指命令为/重置请求次数群聊和/重置请求次数好友以此区分重置类型。下面类似者，不再赘述），\n\n3.该插件会检查添加好友、群的请求，同意自动添加则自动，好友上限默认为2小时5个，群聊8小时2个，群聊加的频繁易风控，具体频率可以自己控制，等下次收到请求时会检查时间，如果是下一个时间段会重置被请求加好友、群次数，并向插件指定qq号发送提示，\n\n4.不同意则保存记录等待命令/同意加(好友、群聊) qq号或群号，/拒绝加(好友、群聊) qq号或群号，/查看加(好友、群聊)  查看数量（可不填，默认为配置中的最大值），也可以写一个算法依时清理没有自动添加的好友群聊，\n\n5./添加请求接收者 /删除请求接收者 此二者用来添加好友请求处理人，默认配置为前2个超管。\n\n6./更改最大加数量(好友、群聊) 数量（正整数） \n\n/更改加时间(好友、群聊) 时间（正整数） \n\n/更改加时间单位(好友、群聊) 时/分/天 (刷新时间间隔单位)  \n\n7./重载配置 重新载入配置文件数据 用于手动修改文件后的重载问题 \n\n8./更改查看加返回数量 数量 （非负整数，<120） \n\n9.黑名单群聊与警告群聊、黑名单群名与警告群名，一个直接拒绝、一个不自动同意，含黑名单、警告词或群号时生效，可以同时转发拉人头兼职群群聊发起者给配置过的好友，一般是该群管理员（自己配置qq号，因为只发给好友，临时会话太危险），暂无机器人接口、请于本插件目录下config.json文件中手动配置\n\n10.验证消息，需要验证消息在添加者验证消息中方验证通过，默认空，表示皆通过。手动配置\n\n11./清理请求表 清理请求表中已添加过的好友信息\n\n12./加好友帮助 返回各命令，忘了命令是哪个就康康。\n\n\n预期更新，1.优化返回结果，2.改善验证，便于用户自行编写验证方法，3.增加闲余时间自处理多余请求算法\n\n配置项模板结构\n\n{\n\n  "agreeAutoApprove": { "friend": 1, "group": 0 },\n\n  "recipientList": [],\n\n  "forwardSet":0,\n\n  "numControl": {"useAlgorithm":0, "maxNum": 5, "time": 2, "unit": "h" ,"friend":{"maxNum": 5, "time": 2, "unit": "h" },"group":{"maxNum": 2, "time": 8, "unit": "h" }},\n\n  "maxViewNum": 20,\n\n  "blackDict":{"friend":{"text":[],"id":[]},"group":{"text":[],"id":[]},"forward":{}},\n\n  "warnDict":{"friend":{"text":[],"id":[]},"group":{"text":[],"id":[]},"forward":{}},\n\n  "allowAddFriednText":[],\n\n  "botName": "我",\n\n  "friend_msg": {\n\n\u200b    "notice_msg": "请求添加好友,验证消息为",\n\n\u200b    "welcome_msg": "我未知的的朋友啊，很高兴你添加我为qq好友哦！\\n同时，如果有疑问，可以发送/help哦"\n\n  },\n\n  "group_msg": {\n\n\u200b    "notice_msg": "发送群邀请,验证消息为",\n\n\u200b    "welcome_msg": "我亲爱的的朋友啊，很高兴你邀请我哦！"\n\n  },\n\n  "statusDict":{\n\n\u200b    "blackDict":{"friend":{"status":"拉黑QQ,已拒绝,仅作提示"},"group":{"status":"拉黑群聊,已拒绝,仅作提示"}},\n\n\u200b    "warnDict":{"friend":{"status":"警告QQ,手动同意,是否同意"},"group":{"status":"警告群聊,手动同意,是否同意"}}\n\n  }\n\n}',
    'author': 'ziru-w',
    'author_email': '77319678+ziru-w@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
