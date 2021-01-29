import time, os
#stt= time.monotonic()*1000
#x= {'a':2,'b':3,}
#y= {1:'b'}
#z = 1 
#if y[1] in x:
    #print(x)
#et = time.monotonic()*1000

#print(os.listdir())

anydict={
    'anylist' : ['abcd','efgh']
}

#print (anydict['anylist'][0])

x = [('a','b'),('c','d'),('e','f')]
'''
for i in range(len(x)):
    print(x[i][i-1])
'''
randostring = 'hello🥵'
print(randostring)
anyfile = open('tests.json','a',encoding='utf-16')
anyfile.write(randostring)
anyfile.close()