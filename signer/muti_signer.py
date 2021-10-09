import shutil
import os

"""
1.安装Python27，配置环境变量。
2.配置apksinger的环境变量。
3.把xxx.jks、xxx.apk（支持多个）放入和MultiSigner.py同目录下。
4.双击MultiSigner.py，出现命令行窗体，等待。
5.按任意键结束。
6.查看output目录下已签好的apk文件。
"""
# jks签名证书（放在当前目录中）
jksFile = 'debug.keystore'
# KeyStore密码
storePassword = 'android'
# 生成jks时指定的alias
keyAlias = 'androiddebugkey'
# 签署者的密码，即生成jks时指定alias对应的密码
keyPassword = 'android'

# 获取当前目录中所有的apk源包
src_apks = []
os.chdir("res")
for file in os.listdir():
    if os.path.isfile(file):
        extension = os.path.splitext(file)[1][1:]
        if extension in 'apk':
            src_apks.append(file)
try:
    for src_apk in src_apks:
        print(src_apk)
        # file name (with extension)
        src_apk_file_name = os.path.basename(src_apk)
        # 分割文件名与后缀
        temp_list = os.path.splitext(src_apk_file_name)
        # name without extension
        src_apk_name = temp_list[0]
        # 后缀名，包含.   例如: ".apk "
        src_apk_extension = temp_list[1]
        # 创建生成目录
        output_dir = 'output/'
        # 目录不存在则创建
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # 目标文件路径
        target_apk = output_dir + src_apk_name + src_apk_extension
        # 签名后的文件路径
        signer_apk = output_dir + src_apk_name + '_signer' + src_apk_extension
        # 拼装签名命令
        signer_str = 'apksigner sign --ks ' + jksFile + ' --ks-pass pass:' + storePassword + \
                     ' --ks-key-alias ' + keyAlias + ' --out ' + signer_apk + ' ' + src_apk
        print(signer_str)
        # 执行签名命令
        os.chdir("D:/PyCharm 2021.2.1/code/xapk-downloader/signer/res")
        os.system(signer_str)
except Exception:
    print(Exception)
