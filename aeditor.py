from pydub import AudioSegment
import wx
import wx.media
import re
tim=re.compile(r'^\d\d:[0-5]\d:[0-5]\d$')
fil=re.compile(r'\.((mp3)|(wma)|(wav))$')
fname=re.compile(r'^[a-zA-Z0-9_' ']+\.((mp3)|(wma)|(wav))$')
direct=''
l=[]
i=1
mw=None
def aedit():
    global mw
    app= wx.App()
    class Aedit(wx.Frame):
        def __init__(self,parent,title):
            super(Aedit, self).__init__(parent,title=title,size=(1075,650))
            ico = wx.Icon('Image/icon.ico',wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)
            self.mp=wx.Panel(self,size=(800,600))
            self.Centre()

    class VPanel(wx.Panel):
        def __init__(self,parent):
            super(VPanel, self).__init__(parent)
            
            
    m=Aedit(None,title='Audio Editor')
    mw=m.mp
    mw.SetBackgroundColour((21,21,21))
    def addnew(event=None):
        global i
        if i<10:
            a=item(i)
            i+=1
            l.append(a)
    
    class item:
    
        def __init__(self,i):
            global posy,outl,outlab,outbrowse,outlab1,outfn,edbut,l,mw
            self.i=i
            self.label = wx.StaticText(mw,-1,label="File: ",pos=(25,25*(2*i+2)))
            self.label.SetForegroundColour((255,255,255))
            self.fn=''
            self.label1 = wx.StaticText(mw,-1,label="Begin:",pos=(450,(25*(2*i+2))-5))
            self.label1.SetForegroundColour((255,255,255))
            self.beg=0
            self.slider1 = wx.Slider(mw,wx.ID_ANY,size = (300,-1),pos=(500,(25*(2*i+2))-10))
            self.slider2 = wx.Slider(mw,wx.ID_ANY,size = (300,-1),pos=(500,(25*(2*i+2))+10),style=wx.SL_HORIZONTAL|wx.SL_TOP)
            self.slider1.Enable(False)
            self.slider2.Enable(False)
            self.label2 = wx.StaticText(mw,-1,label="End:",pos=(450,(25*(2*i+2))+15))
            self.label2.SetForegroundColour((255,255,255))
            self.end=0
            self.clip=None
            self.size=0
            self.browse = wx.Button(mw,label="Browse",pos=(350,25*(2*i+2)))
            self.browse.Bind(wx.EVT_BUTTON,self.browsefile)
            self.play=wx.BitmapButton(mw,wx.ID_ANY,wx.Bitmap('Image/play.png'),pos=(800,25*(2*i+2)-5))
            self.play.Bind(wx.EVT_BUTTON,self.onPlay)
            self.pause=wx.BitmapButton(mw,wx.ID_ANY,wx.Bitmap('Image/pause.png'),pos=(850,25*(2*i+2)-5))
            self.pause.Bind(wx.EVT_BUTTON,self.onPause)
            self.play.Enable(False)
            self.pause.Enable(False)
            self.rem=wx.BitmapButton(mw,wx.ID_ANY,wx.Bitmap('Image/remove.png'),pos=(900,25*(2*i+2)-5))
            self.rem.Bind(wx.EVT_BUTTON,self.remove)
            self.up=wx.BitmapButton(mw,wx.ID_ANY,wx.Bitmap('Image/up.png'),pos=(950,25*(2*i+2)-5))
            self.up.Bind(wx.EVT_BUTTON,self.moveup)
            self.down=wx.BitmapButton(mw,wx.ID_ANY,wx.Bitmap('Image/down.png'),pos=(1000,25*(2*i+2)-5))
            self.down.Bind(wx.EVT_BUTTON,self.movedown)
            self.player=wx.media.MediaCtrl(mw,style=wx.SIMPLE_BORDER)
            self.down.Enable(False)
            if self.i==0:
                self.up.Enable(False)
                self.rem.Enable(False)
            if len(l)>=1:
                l[0].rem.Enable(True)
                l[len(l)-1].down.Enable(True)
            posy+=50
            outl.MoveXY(x=25,y=posy)
            outlab.MoveXY(x=125,y=posy)
            outbrowse.MoveXY(x=400,y=posy)
            outlab1.MoveXY(x=500,y=posy)
            outfn.MoveXY(x=600,y=posy)
            edbut.MoveXY(x=725,y=posy)
            self.timer = wx.Timer(self.slider2)
            self.slider2.Bind(wx.EVT_TIMER,self.OnTimer)

        def onPlay(self,event=None):
            global l
            for i in l:
                i.player.Pause()
                i.timer.Stop()
            print self.player.Length()
            self.slider1.SetRange(0,self.player.Length())
            self.slider2.SetRange(0,self.player.Length())
            self.slider1.Enable(True)
            self.slider2.Enable(True)
            self.player.Play()
            self.timer.Start(100)

        def onPause(self,event=None):
            self.player.Pause()
            self.timer.Stop()

        def stopSeek(self,event=None):
            self.timer.Stop()
                
        def seek(self,event=None):
            self.player.Seek(self.slider2.GetValue())
            self.timer.Start(100)

        def OnTimer(self,event=None):
            current = self.player.Tell()
            self.slider2.SetValue(current)
            
        def browsefile(self,event=None):
            global mw
            filters="Waveform Audio Files(*.wav)|*.wav|Windows Media Audio Files(*.wma)|*.wma|MPEG-2 Files(*.mp3)|*.mp3|All Audio Files(*.wav,*.wma,*.mp3)|*.wav;*.wma;*.mp3;"
            dlg = wx.FileDialog(mw, message="Open File", wildcard=filters, style=wx.OPEN)
            dlg.SetFilterIndex(4)
            if dlg.ShowModal() == wx.ID_OK:
                self.fn = dlg.GetPath()
            dlg.Destroy()
            global fil
            result=fil.search(self.fn)
            if result:
                self.play.Enable(True)
                self.pause.Enable(True)
                fn=self.fn.split("\\")
                self.label.SetLabel("File: "+fn[len(fn)-1])
                self.player.Load(self.fn)
                self.size=self.player.Length()
                self.slider2.Bind(wx.EVT_SCROLL,self.stopSeek)
                self.slider2.Bind(wx.EVT_SCROLL_CHANGED,self.seek)


        def moveup(self,event=None):
            global l
            temp=l[self.i-1].label.GetLabel()
            l[self.i-1].label.SetLabel(self.label.GetLabel())
            self.label.SetLabel(temp)
            l[self.i-1].fn,self.fn=self.fn,l[self.i-1].fn
            temp=l[self.i-1].slider1.IsEnabled()
            l[self.i-1].slider1.Enable(self.slider1.IsEnabled())
            self.slider1.Enable(temp)
            a,b=l[self.i-1].slider1.GetValue(),self.slider1.GetValue()
            l[self.i-1].slider1.SetValue(b)
            self.slider1.SetValue(a)
            l[self.i-1].beg,self.beg=self.beg,l[self.i-1].beg
            temp=l[self.i-1].slider2.IsEnabled()
            l[self.i-1].slider2.Enable(self.slider2.IsEnabled())
            self.slider2.Enable(temp)
            a,b=l[self.i-1].slider2.GetValue(),self.slider2.GetValue()
            l[self.i-1].slider2.SetValue(b)
            self.slider2.SetValue(a)
            l[self.i-1].player,self.player=self.player,l[self.i-1].player
            l[self.i-1].size,self.size=self.size,l[self.i-1].size
            temp=l[self.i-1].play.IsEnabled()
            l[self.i-1].play.Enable(self.play.IsEnabled())
            self.play.Enable(temp)
            temp=l[self.i-1].pause.IsEnabled()
            l[self.i-1].pause.Enable(self.pause.IsEnabled())
            self.pause.Enable(temp)
        
        def movedown(self,event=None):
            global l
            temp=l[self.i+1].label.GetLabel()
            l[self.i+1].label.SetLabel(self.label.GetLabel())
            self.label.SetLabel(temp)
            l[self.i+1].fn,self.fn=self.fn,l[self.i+1].fn
            temp=l[self.i+1].slider1.IsEnabled()
            l[self.i+1].slider1.Enable(self.slider1.IsEnabled())
            self.slider1.Enable(temp)
            a,b=l[self.i+1].slider1.GetValue(),self.slider1.GetValue()
            l[self.i+1].slider1.SetValue(b)
            self.slider1.SetValue(a)
            l[self.i+1].beg,self.beg=self.beg,l[self.i+1].beg
            temp=l[self.i+1].slider2.IsEnabled()
            l[self.i+1].slider2.Enable(self.slider2.IsEnabled())
            self.slider2.Enable(temp)
            a,b=l[self.i+1].slider2.GetValue(),self.slider2.GetValue()
            l[self.i+1].slider2.SetValue(b)
            self.slider2.SetValue(a)
            l[self.i+1].player,self.player=self.player,l[self.i+1].player
            l[self.i+1].size,self.size=self.size,l[self.i+1].size
            temp=l[self.i+1].play.IsEnabled()
            l[self.i+1].play.Enable(self.play.IsEnabled())
            self.play.Enable(temp)
            temp=l[self.i+1].pause.IsEnabled()
            l[self.i+1].pause.Enable(self.pause.IsEnabled())
            self.pause.Enable(temp)
                    
        def remove(self,event=None):
            global i,l,posy,outl,outlab,outbrowse,outlab1,outfn,edbut
            if i>1:
                a= l[self.i]
                a.label.Destroy()
                a.label1.Destroy()
                a.label2.Destroy()
                a.browse.Destroy()
                a.play.Destroy()
                a.pause.Destroy()
                a.slider1.Destroy()
                a.slider2.Destroy()
                a.player.Destroy()
                a.rem.Destroy()
                a.up.Destroy()
                a.down.Destroy()
                for j in range(self.i+1,len(l)):
                    l[j].i-=1
                    l[j].label.MoveXY(x=25,y=25*(2*l[j].i+2))
                    l[j].browse.MoveXY(x=350,y=25*(2*l[j].i+2))
                    l[j].label1.MoveXY(x=450,y=25*(2*l[j].i+2)-5)
                    l[j].slider1.MoveXY(x=500,y=25*(2*l[j].i+2)-10)
                    l[j].label2.MoveXY(x=450,y=25*(2*l[j].i+2)+15)
                    l[j].slider2.MoveXY(x=500,y=25*(2*l[j].i+2)+10)
                    l[j].play.MoveXY(x=800,y=25*(2*l[j].i+2)-5)
                    l[j].pause.MoveXY(x=850,y=25*(2*l[j].i+2)-5)
                    l[j].rem.MoveXY(x=900,y=25*(2*l[j].i+2)-5)
                    l[j].up.MoveXY(x=950,y=25*(2*l[j].i+2)-5)
                    l[j].down.MoveXY(x=1000,y=25*(2*l[j].i+2)-5)
                i-=1
                posy-=50
                outl.MoveXY(x=25,y=posy)
                outlab.MoveXY(x=125,y=posy)
                outbrowse.MoveXY(x=400,y=posy)
                outlab1.MoveXY(x=500,y=posy)
                outfn.MoveXY(x=600,y=posy)
                edbut.MoveXY(x=725,y=posy)
                if self.i==i:
                    l[i-1].down.Enable(False)
                if self.i==0:
                    l[1].up.Enable(False)
                del l[self.i]
                if i==1:
                    l[0].rem.Enable(False)
            
    def browsedir(event=None):
        global direct,outlab,mw
        dlg = wx.DirDialog(mw, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            direct=dlg.GetPath()
        dlg.Destroy()
        outlab.SetLabel('Directory: '+direct)

    def con(clip):
        global direct,outfn
        audio = clip[0]
        for i in range(1,len(clip)):
            audio+=clip[i]
        audio.export(direct+'/'+outfn.GetValue(),format=outfn.GetValue()[-3:0])
    
    def edit(event=None):
        global mw,l,direct,outfn,posy
        print outfn.GetValue(),'hello'
        for k in l:
            if k.fn=='':
                dlg=wx.MessageDialog(mw,"Invalid File Path",'Error',wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return
        if direct=='':
            dlg=wx.MessageDialog(mw,"Invalid Directory Path",'Error',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif outfn.GetValue()=='':
            dlg=wx.MessageDialog(mw,"Invalid Output File Name",'Error',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            clip=[]
            for k in l:
                cl=AudioSegment.from_file(k.fn)
                k.player.Pause()
                clip.append(cl[k.slider1.GetValue():k.slider2.GetValue()])
            con(clip)
            temp=range(len(clip))
            for k in temp:
                del clip[0]
            del clip
            temp=range(len(l))
            for k in temp:
                l[0].label.Destroy()
                l[0].label1.Destroy()
                l[0].slider1.Destroy()
                l[0].label2.Destroy()
                l[0].slider2.Destroy()
                l[0].browse.Destroy()
                l[0].play.Destroy()
                l[0].pause.Destroy()
                l[0].rem.Destroy()
                l[0].up.Destroy()
                l[0].down.Destroy()
                l[0].player.Destroy()
                posy-=50
                del l[0]
            global i
            i=1
            outl.MoveXY(x=25,y=posy)
            outlab.MoveXY(x=125,y=posy)
            outlab.SetLabel('')
            outbrowse.MoveXY(x=400,y=posy)
            outlab1.MoveXY(x=500,y=posy)
            outfn.MoveXY(x=600,y=posy)
            direct=''
            edbut.MoveXY(x=725,y=posy)
            l.append(item(0))
            dlg=wx.MessageDialog(mw,"Editing Completed Successfully",'Success',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            temp=outfn.Destroy()
            outfn=wx.TextCtrl(mw,pos=(600,posy))
            outfn.Bind(wx.EVT_KILL_FOCUS, checkfn)
        
    def checkfn(event=None):
        global fname,outfn,mw,posy
        result=fname.search(outfn.GetValue())
        if result or outfn.GetValue()=='':
            temp= outfn.GetValue()
            outfn.Destroy()
            outfn=wx.TextCtrl(mw,pos=(600,posy))
            outfn.Bind(wx.EVT_KILL_FOCUS, checkfn)
            outfn.SetValue(temp)
            
        else:
            dlg=wx.MessageDialog(mw,"Invalid File Name",'Error',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            outfn.Destroy()
            outfn=wx.TextCtrl(mw,pos=(600,posy))
            outfn.Bind(wx.EVT_KILL_FOCUS, checkfn)
            

    global posy,outl,outlab,outbrowse,outlab1,outfn,edbut
    lab=wx.StaticText(mw,label="Input Files:",pos=(100,12))
    lab.SetForegroundColour((255,255,255))
    add=wx.Button(mw,label="Add",pos=(500,12))
    add.Bind(wx.EVT_BUTTON,addnew)
    posy=62
    outl=wx.StaticText(mw,label='Output File: ',pos=(25,posy))
    outl.SetForegroundColour((255,255,255))
    outlab=wx.StaticText(mw,label='Directory: ',pos=(125,posy))
    outlab.SetForegroundColour((255,255,255))
    outbrowse=wx.Button(mw,label="Browse",pos=(400,posy))
    outbrowse.Bind(wx.EVT_BUTTON,browsedir)
    outlab1=wx.StaticText(mw,label='File Name: ',pos=(500,posy))
    outlab1.SetForegroundColour((255,255,255))
    outfn=wx.TextCtrl(mw,pos=(600,posy))
    outfn.Bind(wx.EVT_KILL_FOCUS, checkfn)
    edbut=wx.Button(mw,label="Edit",pos=(725,posy))
    edbut.Bind(wx.EVT_BUTTON,edit)
    l.append(item(0))
    m.Show()
    mw.Refresh()
    app.MainLoop()

if __name__ == '__main__':
    aedit()
