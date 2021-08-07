from dql import *
random.seed(1)


q = QL(40)
# q.load(open('q.p', 'rb'))
q.train(0.1, 0.9, 10000000, 0.0)
q.save(open('q.p', 'wb'))
q.size = 40



