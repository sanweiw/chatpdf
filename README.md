# chatpdf
ChatPDF 旨在创建一个交互式的PDF问答平台，用户可以上传PDF文件，并通过与系统的对话来获取文件内容的深入理解。系统将自动从PDF中提取问题，用户可以选择问题进行交流，后端处理PDF内容，并通过大型语言模型（LLM）生成回答，最终将回答展示给用户。

# ChatPDF 项目需求文档 (PRD)
## 1. 项目概述
ChatPDF 旨在创建一个交互式的PDF问答平台，用户可以上传PDF文件，并通过与系统的对话来获取文件内容的深入理解。系统将自动从PDF中提取问题，用户可以选择问题进行交流，后端处理PDF内容，并通过大型语言模型（LLM）生成回答，最终将回答展示给用户。

## 2. 功能需求
### 2.1 前端
#### 2.1.1 PDF上传
用户可以通过拖拽或文件选择对话框上传PDF文件。
上传的PDF文件将被发送到后端进行处理。
#### 2.1.2 对话界面
显示历史对话信息。
支持用户输入文本查询。
从上传的PDF中随机生成三个问题供用户选择。
用户可以点击问题或输入自定义查询。
#### 2.1.3 响应展示
展示从后端接收到的回复。
支持滚动查看历史对话。
### 2.2 后端
#### 2.2.1 PDF处理
接收上传的PDF文件。
将PDF文件切割为可处理的文本块。
将文本块灌入向量数据库以便检索。
#### 2.2.2 查询处理
接收用户查询。
通过向量数据库检索相关的文本块。
使用检索到的文本块生成新的Prompt。
#### 2.2.3 与LLM交互
将生成的Prompt发送给大型语言模型（LLM）。
接收LLM生成的回复。
#### 2.2.4 回复处理
将LLM的回复格式化后发送给前端。
## 3. 技术栈
前端：Vue.js
后端：Python Flask
向量数据库：chromadb
LLM接口：OpenAI API 或其他兼容的大型语言模型API
## 4. 安全性和隐私
确保上传的PDF文件安全存储，不被未授权访问。
对话历史应仅对当前用户可见，确保隐私保护。
## 5. 性能要求
前端响应时间不超过2秒。
后端处理时间（包括与LLM的交互）不超过5秒。
## 6. 用户界面设计
界面简洁，易于导航。
对话界面应清晰展示历史对话和当前可选问题。
上传界面应直观，易于操作。
## 7. 测试计划
单元测试覆盖所有核心功能。
集成测试确保前后端交互流畅。
性能测试验证响应时间和系统负载能力。
## 8. 部署计划
使用Docker容器化部署后端服务。
前端通过CDN进行分发以提高访问速度。
使用云服务提供弹性伸缩能力。
## 9. 维护和支持
提供文档支持前端和后端的开发。
定期更新系统以修复已知问题和提升性能。
提供用户反馈渠道以持续改进产品。
## 10. 项目里程碑
需求分析和设计：完成需求文档和系统设计。（预计时间：2周）
开发实施：前端和后端的并行开发。（预计时间：8周）
测试与调优：系统测试和性能调优。（预计时间：4周）
部署上线：完成部署并上线。（预计时间：2周）
后期维护：根据用户反馈进行持续优化。（持续进行）
# 通过上述需求文档，ChatPDF项目的目标、功能、技术栈、安全隐私、性能要求、用户界面设计、测试计划、部署计划、维护支持以及项目里程碑得到了明确的规划。
