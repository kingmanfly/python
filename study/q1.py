import queue

a = queue.Queue()
a.put("Python")
a.put("Java")
a.put("C")
a.put("C++")
a.task_done()

print(a.get())
print(a.get())
print(a.get())
print(a.get())