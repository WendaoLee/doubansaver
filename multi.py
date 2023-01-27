"""

What I expect:
    - 一个CLI主进程，有以下几个命令
        - start 打开SSE监听进程，启动Web服务，开启API
        - log
"""

if __name__ =='__main__':
    isTerminated = False
    while isTerminated is False:
        cmd = input('\033[35m[INFO]\033[0m 输入help显示帮助\n')
        if cmd == 'help':
            continue
        if cmd == 'exit':
            isTerminated = True
        if cmd == 'test':
            print(1)