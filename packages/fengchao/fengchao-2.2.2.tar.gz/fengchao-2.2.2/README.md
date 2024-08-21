该项目集成第三方大模型，本地开源大模型，知识库建设，指令设计，api消费统计，鉴权等功能。

支持的功能接口参见下表，部分接口需要进行鉴权使用，仅API需要单独鉴权（参考<span style="color:#0000FF">【如何鉴权】</span>）。

支持通过SDK及API方式进行访问。推荐使用SDK方式进行访问，SDK已集成鉴权，解析等功能。

api_key及secret_key获取方式：<span style="color:#00BFFF">【安全中心】</span>可以进行注册、查看api_key及secret_key，不同业务请注册属于自己的api_key及secret_key

### 支持功能
| 功能         | 是否鉴权 | 是否支持协程 |
|:-----------|:----:|:------:|
| 生成token    |  否   |   否    |
| 查看模型列表     |  否   |   否    |
| 查看prompt列表 |  否   |   否    |
| 查看知识库列表    |  否   |   否    |
| 对话服务：同步对话  |  是   |   是    |
| 对话服务：异步对话  |  是   |   是    |
| 对话服务：异步结果  |  是   |   是    |
| 对话服务：流式对话  |  是   |   是    |

### 支持的模型
| 模型                          | 是否第三方 | 支持文件上传 |
|-----------------------------|:-----:|:------:|
| glm-4                       |   是   |   否    |
| gpt-3.5-turbo               |   是   |   否    |
| gpt-4                       |   是   |   否    |
| gpt-4-turbo                 |   是   |   否    |
| gpt-4o                      |   是   |   否    |
| gpt-4o-mini                 |   是   |   否    |
| Qwen1.5-0.5B-Chat           |   否   |   否    |
| Qwen1.5-1.8B-Chat           |   否   |   否    |
| ERNIE-Bot-4                 |   是   |   否    |
| ERNIE-Bot-8k                |   是   |   否    |
| ERNIE-Bot                   |   是   |   否    |
| ERNIE-Bot-turbo             |   是   |   否    |
| BLOOMZ-7B                   |   是   |   否    |
| Llama-2-7b-chat             |   是   |   否    |
| Llama-2-13b-chat            |   是   |   否    |
| Llama-2-70b-chat            |   是   |   否    |
| Mixtral-8x7B-Instruct       |   是   |   否    |
| Qianfan-Chinese-Llama-2-7B  |   是   |   否    |
| Qianfan-Chinese-Llama-2-13B |   是   |   否    |
| claude-3-opus-20240229      |   是   |   否    |
| claude-3-sonnet-20240229    |   是   |   否    |
| Doubao-pro-32k-browsing     |   是   |   否    |
| Doubao-pro-32k              |   是   |   否    |
| Doubao-pro-128k             |   是   |   否    |
| moonshot-v1-8k              |   是   |   是    |
| moonshot-v1-32k             |   是   |   是    |
| moonshot-v1-128k            |   是   |   是    |


### 支持的指令
| 指令       |
|----------|
| 多译英      |
| 多译中      |
| 韩译中      |
| 日译中      |
| 英译中      |
| 俄译中      |
| 德译中      |
| 法译中      |
| 英文词典     |
| 广告商      |
| 讲故事的人    |
| 担任编剧     |
| 小说家      |
| 词源学家     |
| 标题生成器    |
| 正则表达式生成器 |
| 语言检测器    |
| 文章摘要     |
| 问题推荐     |

### 支持的知识库
| 知识库               | 描述  |
|-------------------|-----|
| news_vector_store | 资讯库 |
