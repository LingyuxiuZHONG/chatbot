# 路由
用于定义URL与视图函数之间的映射关系
## 视图函数
- 是处理Web应用程序请求的Python函数，接收HTTP请求并返回HTTP响应，Flask负责将响应发送给客户端。
- 参数可以包含HTTP请求的信息，例如`请求方法`、`URL参数`、`表单数据`等。
- 通过返回一个响应对象（例如字符串、HTML模板渲染结果等）来告诉Flask要发送给客户端的内容。
### __init__.py
定义公共接口（模块中对外可见的类和函数
### home_comtroller.py
- URL:'/','/home' HTML:'home/index.html'
- URL:'/contact' HTML:'home/contact.html'
- URL:'/about' HTML:'home/about.html'
### nlu_controller.py
- URL:'/nlu' HTML:'nlu/index.html'
- URL:'/api/nlu' Method:'GET' 根据查询内容渲染列表
- URL:'/api/nlu/file' Method:'GET' 加载所选item
- URL:'/api/nlu/file' Method:'POST' 保存修改后的已存在的item
- URL:'/api/nlu/file' Method:'PUT' 保存新创建的item
- URL:'/api/nlu/file' Method:'DELETE' 删除所选item
### stories_controller.py
- URL:'/stories' HTML:'stories/index.html'
- URL:'/api/stories' Method:'GET'
- URL:'/api/stories/file' Method:'GET' 加载所选story
- URL:'/api/stories/file' Method:'POST' 保存修改后的已存在的story
- URL:'/api/stories/file' Method:'PUT' 保存新创建的story
- URL:'/api/stories/file' Method:'DELETE' 删除所选story
- URL:'/api/stories/intentWithUtter' Method:'PUT'
- URL:'/api/stories/intentWithAction' Method:'PUT'
### domain_controller.py
- URL:'/domain' HTML:'domain/index.html'
- URL:'/api/domain' Method:'GET' 加载domain.yml
- URL:'/api/domain' Method:'POST''PUT' 修改domain.yml
- URL:'/api/domain/intent' Method:'PUT' 加intent
### chat_controller.py
- URL:'/chat' HTML:'chat/index.html'
- URL:'/api/train'
### logs_controller.py
- URL:'/logs/all' HTML:'logs/all.html'
- URL:'/logs/rasa' HTML:'logs/rasa.html'
- URL:'/logs/conversation' HTML:'logs/conversations.html'
- URL:'/api/logs/all' Method:'GET'
- URL:'/api/logs/rasa' Method:'GET'
- URL:'/api/logs/conversations' Method:'GET' 
### rasa_controller.py
- URL:'/conversations/<sender_id>/respond' Method:'GET'
- URL:'/actions' Method:'POST''GET'
