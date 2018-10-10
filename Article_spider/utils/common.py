import hashlib
# 常数
def get_md5(url):
    if isinstance(url, str):
    # 此处str 相当于unicode，即isinstance(url, unicode)若为unicode编码则转为utf-8
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


# 测试
if __name__ == "__main__":
    print(get_md5("https://www.baidu.com".encode("utf-8")))