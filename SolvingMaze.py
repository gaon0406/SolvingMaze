#======================#
#                      #
#       version        #
#     2.1 alpha 6      #
#                      #
#======================#


import sys
import tkinter
global a
global window

air = 0
wall = 1
blocked = 2
path = 3


def event(i):
    global a
    if str(i)==".!button":
        name = 1
    else:
        name = int(str(i)[8:])
    if name in a:
        i.configure(background='black')
        a.remove(name)
        if len(startlist)>0 and startlist[0][0]==(name+sizex-1)%sizex and startlist[0][1]==(name-1)//sizex:
            del startlist[0]
        elif len(startlist)==2 and startlist[1][0]==(name+sizex-1)%sizex and startlist[1][1]==(name-1)//sizex:
            del startlist[1]
    else:
        i.configure(background='white')
        a.append(name)

def close(a):
    global window
    window.destroy()
    makemap(a)

def start(c):
    global a
    if str(c.widget)==".!button":
        name = 1
    else:
        name = int(str(c.widget)[8:])
    if name in a:
        if len(startlist)>=1 and startlist[0][1]==(name+sizex-1)%sizex and startlist[0][0]==(name-1)//sizex:
            del startlist[0]
            c.widget.configure(bg='black')
            a.remove(name)
        elif len(startlist)==2 and startlist[1][1]==(name+sizex-1)%sizex and startlist[1][0]==(name-1)//sizex:
            del startlist[1]
            c.widget.configure(bg='black')
            a.remove(name)
        elif len(startlist)==2:
            return
        else:
            a.append(name)
            c.widget.configure(bg='yellow')
            startlist.append([(name-1)//sizex, (name+sizex-1)%sizex])
    else:
        if len(startlist)==2:
            return 
        a.append(name)
        c.widget.configure(bg='yellow')
        startlist.append([(name-1)//sizex, (name+sizex-1)%sizex])
        
def findMapPath(x,y,Map):
    global start
    sizey=len(Map)
    sizex=len(Map[0])
    if x<0 or y<0 or x>=sizey or y>=sizex:
        return False
    elif Map[x][y]!=0:
        return False
    elif x==startlist[1][0] and y==startlist[1][1]:
        Map[x][y] = path
        return True
    else:
        Map[x][y] = path
        if findMapPath(x+1, y, Map) or findMapPath(x, y+1, Map) or findMapPath(x-1, y, Map) or findMapPath(x,y-1,Map):
            return True
        Map[x][y]=blocked
        return False

def makemap(a):
    Map=[]
    a.sort()
    for j in range(sizey):
        Map.append([])
    for i in range(sizex*sizey):
        if (i+1) in a:
            Map[i//sizex].append(0)
        else:
            Map[i//sizex].append(1)
    showresult(Map)
    return Map
    
def showresult(Map):
    sys.setrecursionlimit(1000000)
    if findMapPath(startlist[0][0],startlist[0][1],Map):
        print("Yes")
        window_result = tkinter.Tk()
        window_result.title('RESULT')
        pixel=tkinter.PhotoImage(width=1, height=1)
        Map[startlist[0][0]][startlist[0][1]]=4
        Map[startlist[1][0]][startlist[1][1]]=4
        for i in range(sizey):
            for j in range(sizex):
                if Map[i][j]==1:
                    tkinter.Button(window_result, text="", image=pixel, width=50, height=50, compound='c', bg='black').place(x=10+50*j, y=10+50*i)
                if Map[i][j]==2 or Map[i][j]==0:
                    tkinter.Button(window_result, text="", image=pixel, width=50, height=50, compound='c', bg='white').place(x=10+50*j, y=10+50*i)
                if Map[i][j]==3:
                    tkinter.Button(window_result, text="", image=pixel, width=50, height=50, compound='c', bg='pink').place(x=10+50*j, y=10+50*i)           
                if Map[i][j]==4:
                    tkinter.Button(window_result, text="", image=pixel, width=50, height=50, compound='c', bg='yellow').place(x=10+50*j, y=10+50*i)
    else:
        print("No")

a=[]
startlist=[]

if __name__=='__main__':
    sys.setrecursionlimit(10000)
    sizex=int(input('미로의 가로 사이즈를 정해주세요'))
    sizey=int(input('미로의 세로 사이즈를 정해주세요'))
    window=tkinter.Tk()
    window.title('miro')
    pixelVirtual=tkinter.PhotoImage(width=1, height=1)
    for i in range(sizex*sizey):
        button = tkinter.Button(window, text="", image=pixelVirtual, width=50, height=50, compound='c', bg='black')
        button.place(x=10+50*(i%sizex), y=10+50*(i//sizex))
        button.configure(command=lambda b=button:event(b))
        button.bind("<Button-3>", start)
    tkinter.Button(window, text="결과보기", command=lambda:close(a)).place(x=10, y=sizey*50+20)
