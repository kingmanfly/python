from threading import Thread

class A(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range (10):
            print("我是线程A")

class B(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range (10):
            print("我是线程B")

a = A()
a.start()

b = B()
b.start()