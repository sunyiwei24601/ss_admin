import json
import subprocess
from subprocess import Popen
import time 
import csv
#本算法中的时间计算系统按照美国西部时区进行计算
ssadmin_path = "~/documents/.ssmgr/ss-bash/ssadmin.sh"
MONTH_SECONDS = 31 * 60 * 60 * 24
TIME_GAP = 8 * 60 * 60

def run_cmd(cmd):
    c = Popen(cmd, shell=True, stdout=subprocess.PIPE)
    results = c.stdout.readlines()
    return results 

def add_port(port, password, limit):
    cmd_head = ssadmin_path +" add " + str(port) + " " + password + " " + limit
    results = run_cmd(cmd_head)
    return results 

def del_port(port):
    cmd_head = ssadmin_path + " del " + str(port) 
    results = run_cmd(cmd_head)
    return results

#重置用量
def reset_used(port):
    cmd_head = ssadmin_path + " rused " + str(port) 
    results = run_cmd(cmd_head)
    return results

#显示各端口总用量，可以指定某一端口
def show_port(port=None):
    cmd_head = ssadmin_path +" show" 
    if port:
        cmd_head += (" " +str(port))
    results = run_cmd(cmd_head)
    return results[1:]

def ss_start():
    cmd_head = ssadmin_path + " start"
    return run_cmd(cmd_head)

def ss_restart():
    cmd_head = ssadmin_path + " restart"
    return run_cmd(cmd_head)

class users():
    #strptime是把字符串转化为struct
    #strftime是把strcut转化为字符串
    #ctime是把时间戳转化为字符串
    #asctime是接受时间元组并返回一个可读的字符串形式
    #mktime是接受时间元组返回时间戳----这个时间戳是将时间元组按照本地时间方式来计算
    #time.time()返回当前的时间戳
    #localtime是接受时间戳，返回元组，没有参数就返回当前的时间元组

    def __init__(self, email, port, password, js=None):
        if js:
            self.email = js.get('email')
            self.port = js.get('port')
            self.password = js.get('password')
            self.end_date = js.get('password')
            self.active = js.get('active')
            self.limit = js.get('limit')
        else:    
            self.email = email
            self.port = port 
            self.password = password
            self.end_date = time.time() 
            self.active = False
            self.limit = "50G"
            
    #设置结束时间，如果还未结束就在现有结束时间上增加，如果已经结束，那么就重新设置起始时间为当前
    def prolong_end_date(self, month):
        if self.active:
            self.end_date += int(month) * MONTH_SECONDS
        else:
            self.start_date = time.time()
            self.end_date = self.start_date + int(month) * MONTH_SECONDS
            self.add_port()
            self.active = True

    def add_port(self):
        add_port(self.port, self.password, self.limit)

    def close_port(self):
        self.active = False
        del_port(self.port) 

    def check_reset_usage(self):
        current_time = time.time()
        if current_time - self.start_date >= MONTH_SECONDS:
            reset_used(self.port)
            self.start_date = current_time
            return 1 #重置成功返回1
        else:    
            return 0 #无需重置返回0

    def check_usage(self):
        pass 

    def to_json(self):
        user_json = {}
        user_json['email'] = self.email
        user_json['active'] = self.active
        user_json['end_date'] = self.end_date
        user_json['port'] = self.port
        user_json['limit'] = self.limit
        user_json['start_date'] = self.start_date
        user_json['password'] = self.password
        return user_json 
    
    


def read_csv(filepath):
    f = csv.reader(open(filepath))
    records = [i for i in f]
    records = records[1:]
    return records

def search_users(l, email): #根据邮箱来寻找用户，如果没有则返回None
    for user in l:
        if user.email == email:
            return user
        else:
            return None

def main_process():
    while(True):
        #这里应该git pull一下
        run_cmd("git pull origin master")
        records = read_csv("Records.csv")
        if len(records) > record_nums:
            new_records = records[record_nums:]
        
        #检查出有新的交易记录，首先审核用户是否存在，存在则更新，不存在则新建用户
        if new_records:
            for record in new_records:
                email = record[1]
                month = record[2]
                trs_time = record[3]
                port = record[4]
                password = record[5]

                user = search_users(users_list, email)
                if user:
                    #更新截止日期
                    user.prolong_end_date(month)
                else:
                    user = users(email, port, password)                
                    #更新截止信息
                    user.prolong_end_date(month) 
                    users_list.append(user)
        ss_start() #修改结束之后要记得重新启动一下
        #ss_restart()
        # break
        #交易数据更新结束之后，检查各个用户流量限制，时间限制，是否应该清零流量
        for user in users_list:
            current_time_stamp = time.time()
            end_date = user.end_date
            port = user.port 
            #到期则删除该port
            if current_time_stamp > end_date:
                user.close_port()
            else: #未到期则检查是否应该重置端口
                user.check_reset_usage()

        for i in range(60):
            time.sleep(1)
            print("Program suspend, if need check pause Ctrl+C")

    


if __name__ =="__main__":
    record_nums = 1 #记录的总数目，在比对之后考虑是否加入新的交易记录
    users_list = [] #记录用户类的列表，搜索用户的工作在此进行
    main_process()





















