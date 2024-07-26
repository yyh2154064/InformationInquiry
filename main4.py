# from MyCategory import dir1_df,dir2_df,dir3_df
import pandas as pd
import json5
from openai import OpenAI
from FileJson import JsonFileManager
from Json_to_xlsx import IndustryServiceProcessor

# 配置OpenAI API密钥
#https://dashscope.console.aliyun.com/apiKey 申请apiKey
Api_key = "sk-670eb2aca49a4b4996d077ce2c7f795a"
client = OpenAI(
    api_key=Api_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

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
    
    if response_json["choices"][0]["finish_reason"] == "stop" and response_json["choices"][0]["message"]["content"]:
        content_str = response_json["choices"][0]["message"]["content"]
               
        try:
            # 尝试直接解析为JSON
            ret_json = json5.loads(content_str)
            return ret_json
        except ValueError as e:
            # 如果直接解析失败，尝试从```json```部分提取内容
            content = content_str[content_str.find("```json") + len("```json"):content_str.rfind("```")]
            try:
                ret_json = json5.loads(content)
                return ret_json
            except ValueError as e:
                raise Exception(f"Failed to parse the returned JSON content: {e}")
    else:
        raise Exception(f"Failed to get a valid response from OpenAI: {response_json}")


def mian():
    industry_df = pd.read_excel(r"files/行业列表.xlsx")
    industry_lst = industry_df["行业名称"].tolist()

    # 创建一个JsonFileManager实例,用于保存结果数据
    json_file = 'data/industry_service_info.json'
    
    ret_json_mamger = JsonFileManager(json_file)
    alredy_industry_lst = ret_json_mamger.data.keys()

    total_industries = len(industry_lst)

    for idx, industry_name in enumerate(industry_lst, start=1):
        print(f"Processing industry {industry_name} ({idx}/{total_industries})...")
        if industry_name in alredy_industry_lst:
            print(f"industry {industry_name} already exists, skipping...")
            continue
        try:
            result = Call_openai(industry_name)
            # 将结果保存到json文件中
            ret_json_mamger.update_data(industry_name, result)
            # ret_json_mamger.save_data()
        except Exception as e:
            print(f"Failed to get a valid response from OpenAI for industry{industry_name}: {e}")
    ret_json_mamger.save_data()

    # 根据json结果绘制表格
    output_file = 'data/行业信息.xlsx'
    print("正在进行表格绘制......")
    # 实例化处理类
    processor = IndustryServiceProcessor(json_file, output_file)
    # 运行处理过程
    processor.run()
    print("表格绘制完成")

    
if __name__ == "__main__":
    print("---------------开始------------------")
    mian()
    print("----------------结束-----------------")
