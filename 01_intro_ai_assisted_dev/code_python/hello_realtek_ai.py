"""
這個檔案在上課時，會由 ChatGPT/OpenWebUI 根據 hello_realtek_manual.py 改寫而來。
上課前可以先故意留白或只放註解。
"""
def greet(name: str) -> str:
    """
    這個函數接收使用者輸入的名字，並印出問候語 "Hello, {name} from Realtek!"。
    如果使用者沒有輸入名字，則預設值為 "Engineer"。
    """
    if name:
        return f"Hello, {name} from Realtek!"
    else:
        return "Hello, Engineer from Realtek!"

def main():
    name = input("請輸入你的名字：")
    print(greet(name))

if __name__ == "__main__":
    main()

    