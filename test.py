from src.time_normalizer import TimeNormalizer

if __name__ == '__main__':
    tn = TimeNormalizer()
    test_list = ["薛之谦两年前的演唱会",
                 "薛之谦两周前的演唱会",
                 "我想听邓丽君八十年代到九十年代的安静的歌",
                 "我想听周杰伦去年的歌",
                 "我想听王菲上个月的歌",
                 "昨天的表演",
                 "下午三点开会",
                 "明天上午8点到下午3点",
                 "三天前",
                 "去年三月到五月"]
    for query in test_list:
        res = tn.parse(query)
        print(query)
        for r in res:
            print(r.time_expression, r.time)
        print("----------------------")
