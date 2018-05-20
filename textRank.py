# -*- coding: utf-8 -*-
import networkx
import re

class RawSentence:
    def __init__(self, textIter):
        if type(textIter) == str:
            self.textIter = textIter.split('\n')
        else:
            self.textIter = textIter
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in self.textIter:
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s: continue
                yield s


class RawSentenceReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in open(self.filepath, encoding='utf-8'):
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s: continue
                yield s


class RawTagger:
    def __init__(self, textIter, tagger=None):
        if tagger:
            self.tagger = tagger
        else:
            from konlpy.tag import Komoran
            self.tagger = Komoran()
        if type(textIter) == str:
            self.textIter = textIter.split('\n')
        else:
            self.textIter = textIter
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in self.textIter:
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s: continue
                yield self.tagger.pos(s)


class RawTaggerReader:
    def __init__(self, filepath, tagger=None):
        if tagger:
            self.tagger = tagger
        else:
            from konlpy.tag import Komoran
            self.tagger = Komoran()
        self.filepath = filepath
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in open(self.filepath, encoding='utf-8'):
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s: continue
                yield self.tagger.pos(s)


class TextRank:
    def __init__(self, **kargs):
        self.graph = None
        self.window = kargs.get('window', 5)
        self.coef = kargs.get('coef', 1.0)
        self.threshold = kargs.get('threshold', 0.005)
        self.dictCount = {}
        self.dictBiCount = {}
        self.dictNear = {}
        self.nTotal = 0

    def load(self, sentenceIter, wordFilter=None):
        def insertPair(a, b):
            if a > b:
                a, b = b, a
            elif a == b:
                return
            self.dictBiCount[a, b] = self.dictBiCount.get((a, b), 0) + 1

        def insertNearPair(a, b):
            self.dictNear[a, b] = self.dictNear.get((a, b), 0) + 1

        for sent in sentenceIter:
            for i, word in enumerate(sent):
                if wordFilter and not wordFilter(word): continue
                self.dictCount[word] = self.dictCount.get(word, 0) + 1
                self.nTotal += 1
                if i - 1 >= 0 and (not wordFilter or wordFilter(sent[i - 1])): insertNearPair(sent[i - 1], word)
                if i + 1 < len(sent) and (not wordFilter or wordFilter(sent[i + 1])): insertNearPair(word, sent[i + 1])
                for j in range(i + 1, min(i + self.window + 1, len(sent))):
                    if wordFilter and not wordFilter(sent[j]): continue
                    if sent[j] != word: insertPair(word, sent[j])

    def loadSents(self, sentenceIter, tokenizer=None):
        import math
        def similarity(a, b):
            n = len(a.intersection(b))
            return n / float(len(a) + len(b) - n) / (math.log(len(a) + 1) * math.log(len(b) + 1))

        if not tokenizer: rgxSplitter = re.compile('[\\s.,:;-?!()"\']+')
        sentSet = []
        for sent in filter(None, sentenceIter):
            if type(sent) == str:
                if tokenizer:
                    s = set(filter(None, tokenizer(sent)))
                else:
                    s = set(filter(None, rgxSplitter.split(sent)))
            else:
                s = set(sent)
            if len(s) < 2: continue
            self.dictCount[len(self.dictCount)] = sent
            sentSet.append(s)

        for i in range(len(self.dictCount)):
            for j in range(i + 1, len(self.dictCount)):
                s = similarity(sentSet[i], sentSet[j])
                if s < self.threshold: continue
                self.dictBiCount[i, j] = s

    def getPMI(self, a, b):
        import math
        co = self.dictNear.get((a, b), 0)
        if not co: return None
        return math.log(float(co) * self.nTotal / self.dictCount[a] / self.dictCount[b])

    def getI(self, a):
        import math
        if a not in self.dictCount: return None
        return math.log(self.nTotal / self.dictCount[a])

    def build(self):
        self.graph = networkx.Graph()
        self.graph.add_nodes_from(self.dictCount.keys())
        for (a, b), n in self.dictBiCount.items():
            self.graph.add_edge(a, b, weight=n * self.coef + (1 - self.coef))

    def rank(self):
        return networkx.pagerank(self.graph, weight='weight')

    def extract(self, ratio=0.1):
        ranks = self.rank()
        cand = sorted(ranks, key=ranks.get, reverse=True)[:int(len(ranks) * ratio)]
        pairness = {}
        startOf = {}
        tuples = {}
        for k in cand:
            tuples[(k,)] = self.getI(k) * ranks[k]
            for l in cand:
                if k == l: continue
                pmi = self.getPMI(k, l)
                if pmi: pairness[k, l] = pmi

        for (k, l) in sorted(pairness, key=pairness.get, reverse=True):
            print(k[0], l[0], pairness[k, l])
            if k not in startOf: startOf[k] = (k, l)

        for (k, l), v in pairness.items():
            pmis = v
            rs = ranks[k] * ranks[l]
            path = (k, l)
            tuples[path] = pmis / (len(path) - 1) * rs ** (1 / len(path)) * len(path)
            last = l
            while last in startOf and len(path) < 7:
                if last in path: break
                pmis += pairness[startOf[last]]
                last = startOf[last][1]
                rs *= ranks[last]
                path += (last,)
                tuples[path] = pmis / (len(path) - 1) * rs ** (1 / len(path)) * len(path)

        used = set()
        both = {}
        for k in sorted(tuples, key=tuples.get, reverse=True):
            if used.intersection(set(k)): continue
            both[k] = tuples[k]
            for w in k: used.add(w)

        # for k in cand:
        #    if k not in used or True: both[k] = ranks[k] * self.getI(k)

        return both

    def summarize(self, ratio=0.333):
        r = self.rank()
        ks = sorted(r, key=r.get, reverse=True)[:int(len(r) * ratio)]
        return ' '.join(map(lambda k: self.dictCount[k], sorted(ks)))





for j in range(1, 6):
    for i in range(1, 7):
        tr = TextRank()
        # print('Load...')
        from konlpy.tag import Komoran
        tagger = Komoran()
        stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('【서울=뉴시스】', 'VV'),('이에 따라', 'VV'), ('그러나', 'VV')])
        tr.loadSents(RawSentenceReader("C:\\Users\\Honeyoon\\PycharmProjects\\crolling2\\textfile\\lank{0}-{1}.txt".format(j,i)), lambda sent: filter(lambda x: x not in stopword and x[1] in ('NNG', 'NNP', 'VV', 'VA'),
                                                                                     tagger.pos(sent)))
        # print('Build...')
        tr.build()
        ranks = tr.rank()
        # for k in sorted(ranks, key=ranks.get, reverse=True)[:100]:
        #      print("\t".join([str(k), str(ranks[k]), str(tr.dictCount[k])]))
        result = tr.summarize(0.2)
        if j == 1:
            if i == 1:
                politic1 = result
                print(politic1)
            elif i == 2:
                economy1 = result
                print(economy1)
            elif i == 3:
                social1 = result
                print(social1)
            elif i == 4:
                culture1 = result
                print(culture1)
            elif i == 5:
                world1 = result
                print(world1)
            elif i == 6:
                IT1 = result
                print(IT1)
        if j == 2:
            if i == 1:
                politic2 = result
                print(politic2)
            elif i == 2:
                economy2 = result
                print(economy2)
            elif i == 3:
                social2 = result
                print(social2)
            elif i == 4:
                culture2 = result
                print(culture2)
            elif i == 5:
                world2 = result
                print(world2)
            elif i == 6:
                IT2 = result
                print(IT2)
        if j == 3:
            if i == 1:
                politic3 = result
                print(politic3)
            elif i == 2:
                economy3 = result
                print(economy3)
            elif i == 3:
                social3 = result
                print(social3)
            elif i == 4:
                culture3 = result
                print(culture3)
            elif i == 5:
                world3 = result
                print(world3)
            elif i == 6:
                IT3 = result
                print(IT3)
        if j == 4:
            if i == 1:
                politic4 = result
                print(politic4)
            elif i == 2:
                economy4 = result
                print(economy4)
            elif i == 3:
                social4 = result
                print(social4)
            elif i == 4:
                culture4 = result
                print(culture4)
            elif i == 5:
                world4 = result
                print(world4)
            elif i == 6:
                IT4 = result
                print(IT4)
        if j == 5:
            if i == 1:
                politic5 = result
                print(politic5)
            elif i == 2:
                economy5 = result
                print(economy5)
            elif i == 3:
                social5 = result
                print(social5)
            elif i == 4:
                culture5 = result
                print(culture5)
            elif i == 5:
                world5 = result
                print(world5)
            elif i == 6:
                IT5 = result
                print(IT5)
