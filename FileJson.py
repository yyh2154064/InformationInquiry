import json

class JsonFileManager:
    def __init__(self, file_path):
        """
        初始化JsonFileManager类的实例。

        :param file_path: JSON文件的路径。
        """
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        """
        私有方法，用于加载JSON文件数据。
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"警告：文件 {self.file_path} 未找到。")
            return {}
        except json.JSONDecodeError:
            print(f"错误：文件 {self.file_path} 格式不正确，无法解析为JSON。")
            return {}

    def update_data(self, key, value):
        """
        更新数据字典中的键值对。

        :param key: 要更新或添加的键。
        :param value: 新的值。
        """
        self.data[key] = value

    def save_data(self):
        """
        保存数据到JSON文件。
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        print("数据已成功保存！")

    def overwrite_data(self, new_data):
        """
        :param new_data:
        :return:
        """
        self.data = new_data
        self.save_data()

# 使用示例
if __name__ == "__main__":
    json_manager = JsonFileManager('data.json')
    json_manager.update_data('exampleKey', 'exampleValue')
    json_manager.save_data()
