from multiprocessing import Process,Pipe,connection

def whileSub(pip:connection.PipeConnection):
    for k in pip.recv():
        print(k)
    print(pip.poll())
    return 1

def test_destruct(item:dict,ref:list):
    for i,value in enumerate(item):
        ref[i] = value


if __name__ == "__main__":
    hello = 1
    gg = 'st'

    di = {
        'hello':2,
        'gg':'sadaojwjd'
    }
    test_destruct(di,[hello,gg])
    print(hello)
    # connection1,connection2 = Pipe()
    # p = Process(
    #     target=whileSub,args=(connection2,)
    # )
    # p.start()
    # connection1.send('1')
    # connection1.send('2')
    # p.join()
