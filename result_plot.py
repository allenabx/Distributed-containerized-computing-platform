from matplotlib import pyplot
import time

if __name__ == '__main__':
    with open('walkout') as f:
        lines = f.readlines()
        score = [float(k) for k in [_[:-1].split(' ')[-1] for _ in lines]]


    pyplot.plot(score, '.')
    pyplot.title(' score as times')
    pyplot.xlabel('try times')
    pyplot.ylabel(' distance')
    best = [max(score[:i + 1]) for i, e in enumerate(score)]
    pyplot.plot(best, 'r')
    pyplot.savefig('scores.png')
    pyplot.show()
