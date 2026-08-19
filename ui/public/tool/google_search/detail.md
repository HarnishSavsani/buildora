## Overview

Google The search tool is a real-time API，Search engine results can be extracted, providing information from Google of structured data. It supports various search types including Web、Images, News and Maps。

## Configuration

1. create Google Custom Search Engine
In[Programmable Search Engine](https://programmablesearchengine.google.com/)Medium Add to Search Engine
![google Creation engine](/admin/tool/img/google_AddSearchEngine.jpg)
2. Get cx parameters
Enter the added engine details and obtain the search engine ID in the [Basic] menu, that iscx。
![google cx ](/admin/tool/img/google_cx.jpg)
3. get API Key
Open https://developers.google.com/custom-search/v1/overview?hl=zh-cn getAPI Key。
![google API Key](/admin/tool/img/google_APIKey.jpg)
4. Configure startup parameters
InGoogle Fill in the configuration of the above parameters in the startup parameters of the search function and enable the function。
![Startup parameters](/admin/tool/img/google_setting.jpg)
5. Use in the application
In the Advanced Orchestration app, click Add Component->function library->GoogleSearch, set usage parameters。
![Used in the application](/admin/tool/img/google_app_used.jpg)
