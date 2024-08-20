'''
因为cython的缘故，server.py拆成了 server.py 和 app.py. server.py 可以cython, app.py不用，直接编译

那么又因为uvicorn的调用问题，调用自己的话，会有重复的问题。所以又加了这个launch.py
unicorn.run 直接用app, 不能用reload. 用字符串,例如 run("server:app", realod=True) 才能加reload
'''

#这里只要分析命令行参数就行

'''
在setup.py中entrypoint, 
    entry_points={
        "console_scripts": ["ss = launch:start"]
    }
'''

import uvicorn
import argparse
import os

def start():
    # 创建解析器对象
    parser = argparse.ArgumentParser(description='Process some integers.')
    # 添加需要的参数
    parser.add_argument('userscript', type=str, help='a string for processing')
    # 添加端口参数
    parser.add_argument('--port', type=int, default=8000, help='port number to use')
    
    parser.add_argument('-V', '--version', action='version', version='SimpleStart 0.0.1.16')

    # 解析参数
    args = parser.parse_args()

    print('Received string is:', args.userscript)
    print('Port number is:', args.port)
    
    #common.init()
    #host = '127.0.0.1'
    host = '0.0.0.0'
    port = args.port ###8000 ###ss.config.port ###8000
    
    print('''
    Welcome to use SimpleStart forum
    https://forum.simplestart.cc
    https://forum.h5book.cn
    ''')



    #if len(sys.argv) > 1:
    #    port = int(sys.argv[1])
    '''
    os.environ['host'] = str(host)
    os.environ['port'] = str(port)
    os.environ['protocol'] = "http"
    '''
    
    #如果是app.py, 那么启动用户脚本的时候，就不能叫app.py了，否则就module loaded. 所以这里加一个_
    uvicorn.run("_app:app", host=host, port=port, reload = True)
