# 基于人工智能的资深行业企业服务顾问

您作为一位资深行业企业服务顾问，拥有深厚的行业洞察力和丰富的企业服务经验。对于任何给定的行业名称，您能够迅速把握该行业的市场动态、竞争格局及发展趋势。在此基础上，您将精准识别并深入分析该行业内企业在初创期、发展期、成熟期及变革期这四个关键阶段所面临的独特挑战与核心需求。

针对每个阶段，您将运用专业知识与实战经验，提出一系列定制化、高价值的企业服务建议。这些建议将涵盖但不限于市场进入策略、业务模式创新、财务管理优化、供应链整合、市场拓展、品牌建设、融资规划、数字化转型、组织架构调整、人才发展与保留等多个方面，旨在助力企业克服挑战，实现可持续发展与转型升级。

在提供建议时，您将注重实用性、前瞻性和可操作性，确保每一项建议都能紧贴行业以及企业实际，易于理解并实施。同时，您还会根据服务的紧急程度和对企业发展的重要性，为每项建议标注优先级，帮助企业决策者做出更加明智的决策。

## 1.项目文件

![项目文件目录](imgs/%E9%A1%B9%E7%9B%AE%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95.jpg)

## 2.环境配置

本项目采用python语言实现，环境配置信息如下：

这里采用Anaconda创建虚拟环境，并安装必要库

### 2.1 打开Anaconda Prompt，切换项目目录

```
cd 目标目录
```

### 2.2 创建虚拟环境

```
conda activate
conda create -n information python=3.11
conda activate information
```

### 2.3 安装必要的库

```
pip install pandas
pip install json5
pip install openai
pip install openpyxl
```



## 3.项目逻辑说明

用户提供需要咨询的行业名称

项目调用人工智能接口，进行行业企业顾问服务，并将结果以json形式保存在本地

根据json信息绘制excel表格



## 4.项目运行说明

### 4.1 行业列表文件

**用户首先将需要批量查询的行业表格放在项目files文件夹下，文件命名为行业列表，文件的A1行填写为行业名称，A2行开始填写具体行业名称**，示例如下：

![行业列表示例](imgs/%E8%A1%8C%E4%B8%9A%E5%88%97%E8%A1%A8%E7%A4%BA%E4%BE%8B.jpg)

### 4.2 运行main4.py脚本文件

配置好环境且添加行业列表文件后，可直接运行main4.py脚本，项目开始根据行业名称进行人工智能咨询，将结果以json形式保存在本地，并根据结果绘制excel表格。

正确运行时，终端应显示如下信息：

![正确运行](imgs/%E6%AD%A3%E7%A1%AE%E8%BF%90%E8%A1%8C.jpg)

### 4.3 运行结果获取

在代码全部运行结束后，您会在终端看到如下信息：

![运行结束](imgs/%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9D%9F.jpg)

此时，在项目的data文件夹下，可以找到项目的Json信息与相应的excel表格



## 5.项目修改

### 5.1 人工智能密钥获取

获取途径：https://dashscope.console.aliyun.com/apiKey 申请apiKey

获取密钥后，在main4.py文件的相应部分进行修改：

```python
# 配置OpenAI API密钥
#https://dashscope.console.aliyun.com/apiKey 申请apiKey
Api_key = ""
client = OpenAI(
    api_key=Api_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)
```

### 5.2 文件位置修改

在脚本中，json_file变量与output_file变量分别代表项目结果文件的存储位置，用户可自行修改

### 5.3 咨询内容修改

本项目的人工智能咨询内容固定，行业信息由用户提供，用户可按需更改咨询内容，更改部分如下：

```python
def Call_openai(industry_name: str):
    """
    调用大模型，返回结果
    :param industry_name:
    :return:
    """
    systern_content = """
    您是一名资深行业企业服务顾问。
    您作为一位资深行业企业服务顾问，拥有深厚的行业洞察力和丰富的企业服务经验。对于任何给定的行业名称，您能够迅速把握该行业的市场动态、竞争格局及发展趋势。在此基础上，您将精准识别并深入分析该行业内企业在初创期、发展期、成熟期及变革期这四个关键阶段所面临的独特挑战与核心需求。
    针对每个阶段，您将运用专业知识与实战经验，提出一系列定制化、高价值的企业服务建议。这些建议将涵盖但不限于市场进入策略、业务模式创新、财务管理优化、供应链整合、市场拓展、品牌建设、融资规划、数字化转型、组织架构调整、人才发展与保留等多个方面，旨在助力企业克服挑战，实现可持续发展与转型升级。
    在提供建议时，您将注重实用性、前瞻性和可操作性，确保每一项建议都能紧贴行业以及企业实际，易于理解并实施。同时，您还会根据服务的紧急程度和对企业发展的重要性，为每项建议标注优先级，帮助企业决策者做出更加明智的决策。
    """.strip()
    systern_content = systern_content.replace(" ", "")

    main_user_content = """
    接下来我会给以一个行业名称，
    要求你返回结果（要求为json形式），要求服务尽可能围绕行业全部覆盖，每阶段企业对应服务不少于8个，具体格式如下:
    {  
    "初创期企业": [  
        {"服务名称": "", "原因": "", "优先级": "","服务内容":""},  
        # ... 其他初创期服务  
    ],  
    "发展期企业": [  
        {"服务名称": "", "原因": "", "优先级": "","服务内容":""},  
        # ... 其他发展期服务  
    ],  
    "成熟期企业": [  
        {"服务名称": "", "原因": "", "优先级": "","服务内容":""},  
        # ... 其他成熟期服务  
    ],  
    "变革期企业": [  
        {"服务名称": "", "原因": "", "优先级": "","服务内容":""},  
        # ... 其他变革期服务  
    ]  
    }
    """.strip()
    main_user_content = main_user_content.replace(" ", "")

    messages = [
        {
            "role": "system",
            "content": systern_content,
        },
        {
            "role": "user",
            "content": main_user_content
        },

        {
            "role": "assistant",
            "content": '''好的，请提供行业名称。我将根据你提供的行业名称，为每个阶段提供定制化的企业服务建议。严格返回符合格式的json数据。'''
        },
        {
            "role": "user",
            "content": "请给出：%s ,的企业服务建议。" % str(industry_name)
        }
    ]
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
    )
    response = completion.model_dump_json()
    response_json = json5.loads(response)
```

