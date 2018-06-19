CTscan_parameter = {
    "G1光栅周期P": 2,  # 周期 P
    "G1光栅步进步数N": 2,  # N - 1 次， 每次步进 P / N
    "样品转台采集次数K": 10,  # 一圈要采集 K 次, 每次动 2π / K
    "样品高度H": 4,
    "样品视场Y方向长度L": 5,
    "样品台轴向步进层数M": 1,  # 步数 M = [H / L] 向上取整 ， 每次走L， 样品高度 H
    "扫描模式": 2  # 0:保留字段， 1:传统相位步进， 2：周步进， 3：免步进
}

para = bytes("{},{},{},{},{},{},{}".format(CTscan_parameter["G1光栅周期P"],
                                        CTscan_parameter["G1光栅步进步数N"],
                                        CTscan_parameter["样品转台采集次数K"],
                                        CTscan_parameter["样品高度H"],
                                        CTscan_parameter["样品视场Y方向长度L"],
                                        CTscan_parameter["样品台轴向步进层数M"],
                                        CTscan_parameter["扫描模式"]), encoding="utf-8")
paralen = bytes(hex(len(para)), encoding="utf-8")


print(para)
print(paralen)

