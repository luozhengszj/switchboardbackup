#!/usr/local/bin/python3.6
import paramiko
import time
import os
import zipfile
import ast
import pymysql


# HW & H3C
hw = ['screen-length disable', 'dis cur']
# ZTE & CISCO
zte = ['terminal length 0', 'show running-config']


def read(name):
    config_path = 'Config.txt'
    with open(config_path, 'r', encoding='utf-8') as f:
        dict = ast.literal_eval(f.read())
        return dict[name]


# 创建连接
conn = pymysql.connect(host=read('host'), port=3306, user=read('user'), passwd=read('passwd'), db=read('db'), charset='utf8')

# 创建游标
cursor = conn.cursor()


def selects():
    # 创建游标
    cursor = conn.cursor()
    sql = 'select brand,ip,login,pwd,sw_name,danwei from switchboard'
    cursor.execute(sql)
    row = cursor.fetchall()
    return row


def mkdir(tmp):
    tmp = tmp.strip()
    tmp = tmp.rstrip('\\')
    isExists = os.path.exists(tmp)
    if not isExists:
        os.makedirs(tmp)
        return True
    else:
        return False


def get(brand,ip,sw_name,pwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, sw_name, pwd)
        ssh_shell = ssh.invoke_shell()
        time.sleep(3)
        if brand == 'H3C' or brand == 'HW':
            ssh_shell.send(hw[0] + '\n')
            time.sleep(1)
            ssh_shell.send(hw[1] + '\n')
        elif brand == 'ZTE' or brand == 'CISCO':
            ssh_shell.send(zte[0] + '\n')
            time.sleep(1)
            ssh_shell.send(zte[1] + '\n')
        time.sleep(10)
        response = ssh_shell.recv(65535 * 100000)
        response_str = response.decode('GBK')
        ssh.close()
        return response_str, '成功'

    except paramiko.ssh_exception.NoValidConnectionsError:
        return "网络连接失败！", '失败'
    except paramiko.ssh_exception.AuthenticationException:
        return "账号密码错误！", '失败'
    except Exception as e:
        return repr(e), '失败'
    finally:
        ssh.close()


def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()


def main():
    '''
    获取配置文件的内容:
    datapath导出配置的路径 E:/4、职创/0、项目汇总/交换机管理/backup/data/
    zippath压缩包的路径 E:/4、职创/0、项目汇总/交换机管理/backup/zip/
    '''
    datapath = read('datapath')
    zippath = read('zippath')


    # 当前时间 2020-03-24
    time_str = time.strftime('%Y-%m-%d', time.localtime())

    nowdatapath = datapath+time_str
    log_str = time_str + 'luozheng的交换机备份工具  备份日志如下：\n'
    for item in selects():
        cfg_str, flag = get(item[0], item[1], item[2], item[3])

        if (flag == '成功'):
            cfg_str = cfg_str[cfg_str.find('#'): cfg_str.rfind('\n')]
            open(nowdatapath + '/' + item[1] + '.cfg', 'w').write(cfg_str)
            log_str = log_str + item[1] + item[4] + flag + '\n'
        else:
            log_str = log_str + item[1] + item[4] + cfg_str + '\n'

    open(datapath + time_str + '.log', 'w').write(log_str)

    time.sleep(10)
    # 压缩文件，都是绝对路径，前是需要压缩的文件夹，后是压缩的zip文件名称
    make_zip(nowdatapath, zippath + time_str + '.zip')


main()


'''
if __name__ == '__main__':
    
    time_str = time.strftime('%Y-%m-%d', time.localtime())
    
    mkdir(logpath)
    nowdatapath = datapath + time_str
    mkdir(nowdatapath)

    log_str = time_str+'  备份日志如下：\n'
    for item in data.selects()[:5]:
        cfg_str, flag = get(item[0], item[1], item[2], item[3])

        if(flag == '成功'):
            cfg_str = cfg_str[cfg_str.find('#'): cfg_str.rfind('\n')]
            open(nowdatapath + '/' + item[1] + '.cfg', 'w').write(cfg_str)
            log_str = log_str + item[1] + item[4] + flag + '\n'
        else:
            log_str = log_str + item[1] + item[4] + cfg_str + '\n'

    open(logpath + '/' + time_str + '.log', 'w').write(log_str)
'''
