# import time
#
# def time_count(func):
#     def wraper(*args, **kwargs):
#         a = time.time()
#         func()
#         b = time.time()
#         print('函数运行的时间{}：'.format(b-a))
#
#     return wraper
#
#
# @time_count
# def dayin():
#     print('dayinyijuhua')
#
# dayin()



s = 'xixi'
print(s.join(['1','2','3']))
print(s)
