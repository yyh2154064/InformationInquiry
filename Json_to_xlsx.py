import pandas as pd
import json

class IndustryServiceProcessor:
    def __init__(self, json_file, excel_file):
        self.json_file = json_file
        self.excel_file = excel_file
        self.columns = [
            '行业名称',
            '初创期企业-服务名称', '初创期企业-原因', '初创期企业-优先级', '初创期企业-服务内容',
            '发展期企业-服务名称', '发展期企业-原因', '发展期企业-优先级', '发展期企业-服务内容',
            '成熟期企业-服务名称', '成熟期企业-原因', '成熟期企业-优先级', '成熟期企业-服务内容',
            '变革期企业-服务名称', '变革期企业-原因', '变革期企业-优先级', '变革期企业-服务内容'
        ]
    
    def load_json_data(self):
        with open(self.json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def process_data(self, data):
        df = pd.DataFrame(columns=self.columns)

        for industry, stages in data.items():
            max_length = max(len(services) for services in stages.values())
            industry_data = {col: [''] * max_length for col in self.columns}
            industry_data['行业名称'] = [industry] + [''] * (max_length - 1)

            for stage, services in stages.items():
                for i, service in enumerate(services):
                    base_col = self._get_base_col(stage)
                    industry_data[f'{base_col}-服务名称'][i] = service['服务名称']
                    industry_data[f'{base_col}-原因'][i] = service['原因']
                    industry_data[f'{base_col}-优先级'][i] = service['优先级']
                    industry_data[f'{base_col}-服务内容'][i] = service['服务内容']

            temp_df = pd.DataFrame(industry_data)
            df = pd.concat([df, temp_df], ignore_index=True)
        
        return df

    def _get_base_col(self, stage):
        if stage == "初创期企业":
            return '初创期企业'
        elif stage == "发展期企业":
            return '发展期企业'
        elif stage == "成熟期企业":
            return '成熟期企业'
        elif stage == "变革期企业":
            return '变革期企业'
        else:
            raise ValueError(f"Unknown stage: {stage}")

    def save_to_excel(self, df):
        df.to_excel(self.excel_file, index=False)

    def run(self):
        data = self.load_json_data()
        df = self.process_data(data)
        self.save_to_excel(df)