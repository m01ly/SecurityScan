# -*- coding: utf-8 -*
from requests.compat import chardet


# 第一层提取
def convent(data):
    new_data = []
    data = data.replace("[\"" , "")
    data = data.replace("\"]", "")
    data = data.split('","')
    for d in data:
        new_data.append(d)
    return '@'.join(new_data)

#USN-6039-1 应用libssl1.1 1.1.1f-1ubuntu2.8 修复版本1.1.1f-1ubuntu2.18,应用openssl 1.1.1f-1ubuntu2.8 修复版本1.1.1f-1ubuntu2.18
def convent2(data):
    new_data = []
    dlist = data.split(',')
    if len(dlist) ==1:
        new_data.append(dlist[0])
    else:
        vunlid = dlist[0].split(' ')[0]
        if vunlid != "USN-":  # --数据超出限制，蜂巢导出限制
            for item in dlist:
                item=item.replace(vunlid+" ", "")
                #row=vunlid+item.split(' ')[0]+item.split(' ')[1]+item.split(' ')[2]
                new_data.append(vunlid+" "+item)
    return '@'.join(new_data)

if __name__ == '__main__':
    import pandas as pd

    # 检测文件编码
    with open('imageos.csv', 'rb') as f:
        result = chardet.detect(f.read())
        print(result)

    # 读取包含复杂文本的CSV文件
    df = pd.read_csv("imageos.csv", encoding='UTF-8-SIG')
    ##第一次提取出补丁
    # 提取所需信息并处理成所需格式
    df['安全补丁'] = df['安全补丁'].apply(convent)
    # 将包含多个值的单元格拆分为多行
    df['安全补丁'] = df['安全补丁'].str.split('@')
    df = df.explode('安全补丁')

    ##进一步提取
    df['安全补丁'] = df['安全补丁'].apply(convent2)
    # 将包含多个值的单元格拆分为多行
    df['安全补丁'] = df['安全补丁'].str.split('@')
    df = df.explode('安全补丁')
    ##拆分USN-6039-1 应用libssl1.1 1.1.1f-1ubuntu2.8 修复版本1.1.1f-1ubuntu2.18

    # 根据空格拆分 C 列，并将结果添加到新列
    split_columns = df['安全补丁'].str.split(' ',expand=True)

    # 将拆分后的列合并到原 DataFrame
    df = pd.concat([df, split_columns], axis=1)

    # 可选：重命名新列以便于识别
    df.columns = ['Repository','tag','安全补丁汇总信息','imageID','操作系统','镜像大小','创建时间','镜像属性','关联镜像数','关联运行容器','节点信息(主机名:IP地址)','补丁数','安装包数','安装包','安全补丁id','受影响应用包','受影响应用包原有版本','修复版本','kong']

    # 打印处理后的DataFrame
    df.to_csv("output.csv", encoding='UTF-8-SIG', index=False)
