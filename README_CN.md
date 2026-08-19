<p align="center"><img src= "https://github.com/1Panel-dev/maxkb/assets/52996290/c0694996-0eed-40d8-b369-322bf2a380bf" alt="MaxKB" width="300" /></p>
<h3 align="center">A powerful and easy-to-use enterprise-level agent platform</h3>
<p align="center">
    <a href="https://trendshift.io/repositories/9113" target="_blank"><img src="https://trendshift.io/api/badge/repositories/9113" alt="1Panel-dev%2FMaxKB | Trendshift" style="width: 250px; height: auto;" /></a>
</p>
<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English_README-blue" alt="English README"></a>
  <a href="https://www.gnu.org/licenses/gpl-3.0.html#license-text"><img src="https://img.shields.io/github/license/1Panel-dev/maxkb?color=%231890FF" alt="License: GPL v3"></a>
  <a href="https://github.com/1Panel-dev/maxkb/releases/latest"><img src="https://img.shields.io/github/v/release/1Panel-dev/maxkb" alt="Latest release"></a>
  <a href="https://github.com/1Panel-dev/maxkb"><img src="https://img.shields.io/github/stars/1Panel-dev/maxkb?style=flat-square" alt="Stars"></a>
  <a href="https://hub.docker.com/r/1panel/maxkb"><img src="https://img.shields.io/docker/pulls/1panel/maxkb?label=downloads" alt="Download"></a>
  <a href="https://gitee.com/fit2cloud-feizhiyun/MaxKB"><img src="https://gitee.com/fit2cloud-feizhiyun/MaxKB/badge/star.svg?theme=gvp" alt="Gitee Stars"></a>
  <a href="https://gitcode.com/feizhiyun/MaxKB"><img src="https://gitcode.com/feizhiyun/MaxKB/star/badge.svg" alt="GitCode Stars"></a>
</p>
<hr/>

MaxKB = Max Knowledge Brain，is a powerful and easy-to-use enterprise-level agent platform, dedicated to solving problems in enterprises AI The implementation faces problems such as high technical threshold, high deployment cost, and long iteration cycle, helping enterprises to gain the upper hand in the artificial intelligence era. Adhering to the design concept of "use out of the box, grow with it"，MaxKB Support enterprises to quickly access mainstream large models, efficiently build exclusive knowledge bases, and provide a progressive upgrade path from basic question answering (RAG), complex process automation (workflow) to agents (Agent), fully empowering multiple application scenarios such as intelligent customer service and intelligent office assistants.。

- **RAG Search enhanced generation**: Efficiently build local AI Knowledge base, supports direct upload of documents / Automatically crawl online documents, support automatic text splitting and vectorization, effectively reduce the illusion of large models and improve the Q&A effect；
- **Flexible orchestration**: built-in powerful workflow engine, function library and MCP Tool calling ability and support for orchestration AI Work process to meet the needs of complex business scenarios；
- **Seamless embedding**: supports zero coding and rapid embedding into third-party business systems, allowing existing systems to quickly have intelligent question and answer capabilities and improve user satisfaction.；
- **Model neutral**: Supports docking with various large models, including local private large models（DeepSeek R1 / Qwen 3 etc.), domestic public large models (Tongyi Qianwen / Tencent Hunyuan / Byte bean bag / Baidu Qianfan / Wisdom spectrum AI / Kimi / MiniMax , etc.) and foreign public large models（OpenAI / Claude / Gemini etc.）。

MaxKB Three-minute video introduction：https://www.bilibili.com/video/BV18JypYeEkj/

## Quick start

```
# Linux machine
docker run -d --name=maxkb --restart=always -p 8080:8080 -v ~/.maxkb:/opt/maxkb registry.fit2cloud.com/maxkb/maxkb

# Windows machine
docker run -d --name=maxkb --restart=always -p 8080:8080 -v C:/maxkb:/opt/maxkb registry.fit2cloud.com/maxkb/maxkb

# username: admin
# Password: MaxKB@123..
```

- You can also synchronize the website knowledge base through [1Panel app store](https://apps.fit2cloud.com/1panel) Rapid deployment MaxKB；
- If it is an intranet environment, it is recommended to use [Offline installation package](https://community.fit2cloud.com/#/products/maxkb/downloads) Perform installation and deployment；
- MaxKB For comparison of different product versions, see：[MaxKB Product version comparison](https://maxkb.cn/price)；
- If you need to introduce it to the team MaxKB，can use this [official PPT Materials](https://fit2cloud.com/maxkb/download/introduce-maxkb_2026.pdf)。

If you have more questions, you can check the user manual, or communicate with us through the forum。

- [Case display](USE-CASES.md)
- [User manual](https://maxkb.cn/docs/)
- [Forum help](https://bbs.fit2cloud.com/c/mk/11)
- Technical exchange group

<image height="150px" width="150px" src="https://github.com/1Panel-dev/MaxKB/assets/52996290/a083d214-02be-4178-a1db-4f428124153a"/>

## UI exhibit

<table style="border-collapse: collapse; border: 1px solid black;">
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src= "https://github.com/user-attachments/assets/eb285512-a66a-4752-8941-c65ed1592238" alt="MaxKB Demo1"   /></td>
    <td style="padding: 5px;background-color:#fff;"><img src= "https://github.com/user-attachments/assets/f732f1f5-472c-4fd2-93c1-a277eda83d04" alt="MaxKB Demo2"   /></td>
  </tr>
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src= "https://github.com/user-attachments/assets/c927474a-9a23-4830-822f-5db26025c9b2" alt="MaxKB Demo3"   /></td>
    <td style="padding: 5px;background-color:#fff;"><img src= "https://github.com/user-attachments/assets/e6268996-a46d-4e58-9f30-31139df78ad2" alt="MaxKB Demo4"   /></td>
  </tr>
</table>

## Technology stack

- Front end：[Vue.js](https://cn.vuejs.org/)
- Backend：[Python / Django](https://www.djangoproject.com/)
- LangChain：[LangChain](https://www.langchain.com/)
- Vector database：[PostgreSQL / pgvector](https://www.postgresql.org/)

## Other star projects of Feizhiyun

- [Cordys CRM](https://github.com/1Panel-dev/CordysCRM) - A new generation of open source AI CRM system
- [1Panel](https://github.com/1panel-dev/1panel/) - Modern, open source Linux Server operation and maintenance management panel
- [JumpServer](https://github.com/jumpserver/jumpserver/) - Popular open source bastion machine
- [DataEase](https://github.com/dataease/dataease/) - Open source data visualization analysis tool available to everyone
- [MeterSphere](https://github.com/metersphere/metersphere/) - A new generation of open source continuous testing tools
- [Halo](https://github.com/halo-dev/halo/) - Powerful and easy-to-use open source website building tool

## License

Copyright (c) 2014-2026 Feizhiyun FIT2CLOUD, All rights reserved.

Licensed under The GNU General Public License version 3 (GPLv3)  (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<https://www.gnu.org/licenses/gpl-3.0.html>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
