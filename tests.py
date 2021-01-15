import time, os
stt= time.monotonic()*1000
x= {
    'a':2,
    'b':3,
}
y= {1:'b'}
z = 1 
if y[1] in x:
    print(x)
et = time.monotonic()*1000

print(os.listdir())