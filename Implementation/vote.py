import os


#   统计投票结果函数
def statisticVote(parameter_list):
    result = {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    }  # 用字典存储统计结果01234分别代表ABCDE
    for vote in parameter_list:
        index = vote.index('1')
        result[str(index)] += 1
    return result


# 是否需要进入STV流程
def boolneedSTV(voteresult, quata):
    achievednumber = 0  # 达到quata的人数
    for value in voteresult.values():
        if (value >= quata):
            achievednumber += 1
    if (achievednumber < 2):  # <2的情况下，进入STV系统
        return True
    else:
        return False


# STV流程
def STVSystem(minindex, VoteSum):
    for i in range(len(VoteSum)):
        if (VoteSum[i][int(minindex)] == '1'):  # 如果给淘汰候选人投'1'，则转移
            temp = list(VoteSum[i])  # 更改str str转list，改值，再转str
            temp[int(minindex)], temp[temp.index('2')] = '0', '1'
            VoteSum[i] = ''.join(temp)
    return VoteSum


filename = input('filename(with extension):')  # 带扩展名
path1 = os.path.abspath('.')  # 相对路径
filepath = path1 + '\\' + filename  # 拼接绝对路径
reflect = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E'}
VoteSum = list()  # VoteSum用来存储所有人的投票数据，一个人的数据为一个字符串，例如'00123'
eliminated = list()  # 存储淘汰候选人
STVtimes = 0  # 存储进入STV系统的次数
# STVtimes作用是得到最小值下标的时候，第一次选择最小，第二次则选择第二小的，因为第一次淘汰的候选人票数为0，仍为最小
with open(filename) as file:  # 读取文件内容
    while True:
        line = file.readline().strip()  # 一行一行的读取，strip是为了去除换行符'/n'
        if not line:
            break
        votelist = line.split(',')  # 去除每一行的逗号，结果为一个list
        # voteforone = Vote_class(votelist)
        s = "".join(votelist)  # 将list拼成一个字符串
        if (''.join(sorted(s)) == '00123'):  # 验证数据有效性
            VoteSum.append(s)  # 有效则加入到投票统计中
    voteresult = statisticVote(VoteSum)  # 统计投票结果
    quata = int(len(VoteSum) / 3) + 1  # 计算quata值
    while True:  # 投票过程为死循环，得到结果break输出
        if (boolneedSTV(voteresult, quata)):  # 是否需要进入STV系统
            if (len(eliminated) == 2):  # 淘汰人数等于2 重新选举
                print('Re-election Called')
                break
            else:
                minindex = int(
                    sorted(voteresult,
                           key=voteresult.get)[STVtimes])  # 得到最投票数的下标
                eliminated.append(str(minindex))  # 淘汰人数+1
                VoteSum = STVSystem(minindex, VoteSum)  # 淘汰流程
                STVtimes += 1  # 进入淘汰流程次数+1
                voteresult = statisticVote(VoteSum)  # 重新计算投票结果
        else:  # 输出结果
            firstselected = sorted(voteresult, key=voteresult.get)[-1]
            secondselected = sorted(voteresult, key=voteresult.get)[-2]
            print(reflect[firstselected], reflect[secondselected],
                  'are elected.')
            if (len(eliminated) != 0):
                for eliminateditem in eliminated:
                    print(reflect[eliminateditem], end=' ')
                print('are eliminated.')
            break
