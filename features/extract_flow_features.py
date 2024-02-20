import numpy as np
import random
import scipy.stats as stats
import math



"""
    返回17个统计特征
"""
def get_packet_size_feature(data):
    if len(data) == 0:
        return [-1]*17
    feature = []
    feature.append(np.min(data))
    feature.append(np.max(data))
    feature.append(np.mean(data))
    feature.append(stats.median_abs_deviation(data))
    feature.append(np.std(data))
    feature.append(np.var(data))
    feature.append(stats.skew(data))
    feature.append(stats.kurtosis(data))
    for p in range(10,100,10):
        feature.append(np.percentile(data,p))

    return feature


def extract_packet_size_features(flow):
    flow = np.array(flow)
    flow = flow[:,1:]
    # 分出两个方向上的数据流
    index_1 = np.argwhere(flow[:,0] == 1).flatten().tolist()
    index_2 = np.argwhere(flow[:,0] == -1).flatten().tolist()
    flow_1 = flow[index_1,1].flatten()
    flow_2 = flow[index_2, 1].flatten()
    flow_3 = flow[:,1]
    features = []
    features.extend(get_packet_size_feature(flow_1))
    features.extend(get_packet_size_feature(flow_2))
    features.extend(get_packet_size_feature(flow_3))
    return features


"""
    提取基本特征
    包括:
        多少个数据包是正向、负向、所有
"""
def extract_basic_features(input_flow):
    flow = np.array(input_flow)
    # flow = flow[:,1:]
    # 分别提取出方向为1和-1的行索引
    index_1 = np.argwhere(flow[:,1] == 1).flatten().tolist()
    index_2 = np.argwhere(flow[:,1] == -1).flatten().tolist()
    # flow1 正向 flow2 反向 flow3 全部
    flow_1 = flow[index_1,:]
    flow_2 = flow[index_2, :]
    flow_3 = flow[:]
    features = []
    # 分别的数量，比例
    num_1 = flow_1.shape[0]
    num_2 = flow_2.shape[0]
    num_3 = flow_3.shape[0]
    features.append(num_1)
    features.append(num_2)
    features.append(num_3)
    features.append(float(num_1)/num_3)
    features.append(float(num_2) / num_3)
    # 流长度总和大小
    byte_1 = np.sum(flow_1[:,2])
    byte_2 = np.sum(flow_2[:, 2])
    features.append(byte_1)
    features.append(byte_2)
    # 流持续时间
    duration = np.max(flow[:,0])-np.min(flow[:,0])
    features.append(duration)
    return features


def cumul_n(trace_data,num):
    result = []
    # num = 100
    data_len = len(trace_data)
    lens = []
    total_length = 0
    sizes = trace_data
    for size in sizes:
        total_length += size
        lens.append(total_length)
    x = np.arange(data_len)

    interval = float(data_len) / num
    x_new = np.arange(0, data_len-1e-5, interval)
    x_new += interval/2

    y_new = np.interp(x_new, x, lens)
    result.extend(list(y_new))
    return result


def extract_interactive_features(input_flow):
    flow = np.array(input_flow)
    sizes = flow[:,1]*flow[:,2]
    features = cumul_n(sizes.tolist(),20)
    return features


def neighborhood(iterable):
    iterator = iter(iterable)
    prev = (0)
    item = next(iterator)
    for next_ in iterator:
        yield (prev, item, next_)
        prev = item
        item = next_
    yield (prev, item, None)


def chunk(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

"""
    划分一系列时间大小为1秒的窗口，统计数据
"""
def number_per_sec(trace_data):
    last_time = trace_data[-1][0]
    last_second = math.ceil(last_time)
    temp = []
    l = []

    # 划分时间段
    for i in range(1, int(last_second) + 1):
        c = 0
        for p in trace_data:
            # 统计时间段内数据包的数量 = c
            if p[0] <= i:
                c += 1
        temp.append(c)
    # temp存储了各个时间段的数据包数量
    if len(temp) == 0:
        return [1, 0, 1, 1, 1]
    for prev, item, next_ in neighborhood(temp):
        x = item - prev
        l.append(x)
    alt_per_sec = [sum(x) for x in chunk(l, 20)]
    # return [np.mean(l), np.std(l), np.percentile(l, 50), np.min(l), np.max(l), np.sum(alt_per_sec)]
    if len(l)>=1:
        return [np.mean(l), np.std(l), np.min(l), np.max(l), np.median(l)]
    else:
        return [-1,-1,-1,-1,-1]


def extract_packet_rate_features(input_flow):
    features = number_per_sec(input_flow)
    return features


# 获取4个统计特征
def get_interval_statistic(flow):
    time = flow[:, 0]
    if len(time) <= 1:
        return [-1,-1,-1,-1]
    interval = time[1:] - time[:-1]
    features = []
    features.append(np.max(interval))
    features.append(np.min(interval))
    features.append(np.mean(interval))
    features.append(np.std(interval))
    return features


# 获取9个特征，百分数
def get_time_percentile(flow):
    time = flow[:, 0]
    if len(time)==0:
        return [-1]*9
    features = []
    for p in range(10,100,10):
        features.append(np.percentile(time,p))
    return features


def extract_temporal_features(input_flow):
    flow = np.array(input_flow)
    index_1 = np.argwhere(flow[:, 1] == 1).flatten().tolist()
    index_2 = np.argwhere(flow[:, 1] == -1).flatten().tolist()
    flow_1 = flow[index_1, :]
    flow_2 = flow[index_2, :]
    flow_3 = flow[:]
    features = []
    features.extend(get_interval_statistic(flow_1))
    features.extend(get_interval_statistic(flow_2))
    features.extend(get_interval_statistic(flow_3))

    features.extend(get_time_percentile(flow_1))
    features.extend(get_time_percentile(flow_2))
    features.extend(get_time_percentile(flow_3))

    return features


def extract_flow_features(my_flow):
    my_flow = np.array(my_flow)
    my_flow[:,0] = my_flow[:,0]-my_flow[0,0]
    features_0 = extract_basic_features(my_flow)
    features_1 = extract_interactive_features(my_flow)
    features_2 = extract_packet_rate_features(my_flow)
    features_3 = extract_temporal_features(my_flow)
    features_4 = extract_packet_size_features(my_flow)
    features = []
    features.extend(features_0)
    features.extend(features_1)
    features.extend(features_2)
    features.extend(features_3)
    features.extend(features_4)
    return features

if __name__ == '__main__':
    direction = []
    direction = [1 for _ in range(100)]
    direction.extend([-1 for _ in range(100)])
    random.shuffle(direction)
    time = np.random.random((len(direction),1))
    time = np.sort(time,axis=0)
    size = np.random.random((len(direction),1))
    direction = np.array(direction).reshape((-1,1))
    my_flow = np.hstack([time, direction, size])
    features = extract_flow_features(my_flow)
    print('Done!')