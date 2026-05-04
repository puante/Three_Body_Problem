import json


class TBPjson:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, "r", encoding="utf-8") as f:
            self.file_data = json.load(f)

    def get_value(self):
        pd = self.file_data["planetdata"]
        return pd["p1"], pd["p2"], pd["p3"]

    def edit_value(self, data):
        f = {
            "_coment1": "안녕하세요!",
            "_coment2": "값을 넣어주세요.",
            "planetdata": data
        }
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(json.dumps(f, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    R = TBPjson("Ex_datas/test1.json")
    print(R.get_value())
