import csv

def main(text):
    # 一元语法模型
    def sgram(sets):
        dic = {}
        dic['#始始#'] = 0
        dic['#末末#'] = 0
        for data in sets:
            for item in data:
                if item in dic:
                    dic[item] = dic[item] + 1
                else:
                    dic[item] = 1
            dic['#始始#'] += 1
            dic['#末末#'] += 1
        return dic

    # 二元语法模型
    def bgram(sets):
        dic = {}
        dic["#始始#"] = dict()
        for data in sets:
            for i in range(len(data) - 1):
                if data[i] not in dic:
                    dic[data[i]] = dict()
                    dic[data[i]][data[i + 1]] = 1
                else:
                    if data[i + 1] in dic[data[i]]:
                        dic[data[i]][data[i + 1]] += 1
                    else:
                        dic[data[i]][data[i + 1]] = 1
            if data[0] not in dic["#始始#"]:
                dic["#始始#"][data[0]] = 1
            else:
                dic["#始始#"][data[0]] += 1

            if data[len(data) - 1] not in dic:
                dic[data[len(data) - 1]] = dict()
                dic[data[len(data) - 1]]["#末末#"] = 1
            elif "#末末#" not in dic[data[len(data) - 1]]:
                dic[data[len(data) - 1]]["#末末#"] = 1
            else:
                dic[data[len(data) - 1]]["#末末#"] += 1

        return dic

    def fen_ci(text, si_grams, bi_grams):
        # 生成一元语法词网
        def gen_wordnet(gram, text):
            net = []
            for i in range(len(text) + 2):
                net.append(list())
            for i in range(len(text)):
                for j in range(i + 1, len(text) + 1):
                    word = text[i:j]
                    if word in gram:
                        net[i + 1].append(word)
            i = 1
            while i < len(net) - 1:
                if len(net[i]) == 0:  # 计算空白行
                    j = i + 1

                    for j in range(i + 1, len(net) - 1):
                        # 寻找第一个非空行
                        if len(net[j]) != 0:
                            break
                    net[i].append(text[i - 1:j - 1])
                    i = j
                else:
                    i += len(net[i][-1])
            return net

        def ca_gram_num(gram):
            num = 0
            for gk in gram.keys():
                num += sum(gram[gk].values())
            return num

        def ca_weight(gram, word_first, word_second, gram_sum):
            if word_first in gram:
                word_first_all = gram[word_first].values()
                if word_second in gram[word_first]:
                    return (gram[word_first][word_second] + 1) / (sum(word_first_all) + gram_sum)
                else:
                    return 1 / (sum(word_first_all) + gram_sum)
            else:
                return 1 / gram_sum

        bi_grams_num = ca_gram_num(bi_grams)

        def viterbi(wordnet):
            dis = []
            for i in range(len(wordnet)):
                dis.append(dict())
            node = []
            for i in range(len(wordnet)):
                node.append(dict())
            word_line = []
            for i in range(len(wordnet)):
                word_line.append(dict())
            wordnet[len(wordnet) - 1].append("#末末#")
            # 更新第一行
            for word in wordnet[1]:
                dis[1][word] = ca_weight(bi_grams, "#始始#", word, ca_gram_num(bi_grams))
                node[1][word] = 0
                word_line[1][word] = "#始始#"

            # 遍历wordnet的每一行
            for i in range(1, len(wordnet) - 1):
                for word in wordnet[i]:
                    # 更新加上这个单词的距离之后那个位置的所有单词的距离
                    for to in wordnet[i + len(word)]:
                        if word in dis[i]:
                            if to in dis[i + len(word)]:
                                # 只要最大频率
                                if dis[i + len(word)][to] < dis[i][word] * ca_weight(bi_grams, word, to, bi_grams_num):
                                    dis[i + len(word)][to] = dis[i][word] * ca_weight(bi_grams, word, to, bi_grams_num)
                                    node[i + len(word)][to] = i
                                    word_line[i + len(word)][to] = word
                            else:
                                dis[i + len(word)][to] = dis[i][word] * ca_weight(bi_grams, word, to, bi_grams_num)
                                node[i + len(word)][to] = i
                                word_line[i + len(word)][to] = word

            # 回溯
            path = []
            f = node[len(node) - 1]["#末末#"]
            fword = word_line[len(word_line) - 1]["#末末#"]
            path.append(fword)
            while f:
                tmpword = fword
                fword = word_line[f][tmpword]
                f = node[f][tmpword]
                path.append(fword)
            path = path[:-1]
            path.reverse()
            return dis, node, word_line, path

        si_net = gen_wordnet(si_grams, text)
        (dis, _, _, path) = viterbi(si_net)

        return path

    fenci_file = open("renmin.csv", "r", encoding="UTF-8")  # 读入分词文件，为后续词性标注做准备
    fenci_reader = csv.reader(fenci_file)
    fenci_sets = []
    for i in fenci_reader:
        sets = []
        for item in i:
            sets.append(item.strip())
        fenci_sets.append(sets)

    si_gram = sgram(fenci_sets)
    bi_gram = bgram(fenci_sets)

    ans = fen_ci(text, si_gram, bi_gram)
    res = ""
    for item in ans:
        res += item + " "
    return res

