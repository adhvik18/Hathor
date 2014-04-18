from moviepy.editor import *
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader as FReader
import wx
import re
tim=re.compile(r'^\d\d:[0-5]\d:[0-5]\d$')
fil=re.compile(r'\.((mp4)|(avi)|(wmv)|(mkv)|(flv)|(3gp))$')
fname=re.compile(r'^[a-zA-Z0-9_' ']+\.((mp4)|(avi)|(wmv)|(mkv))$')
direct=''
l=[]
i=1
mw=None
def vedit():
    global mw
    app= wx.App()
    class Vedit(wx.Frame):
        def __init__(self,parent,title):
            super(Vedit, self).__init__(parent,title=title,size=(975,650))
            ico = wx.Icon('Image/icon.ico',wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)
            self.mp=wx.Panel(self,size=(800,600))
            self.Centre()

    class VPanel(wx.Panel):
        def __init__(self,parent):
            super(VPanel, self).__init__(parent)
            
            
    m=Vedit(None,title='Video Editor')
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
            self.label1 = wx.StaticText(mw,-1,label="Begin:",pos=(450,25*(2*i+2)))
            self.label1.SetForegroundColour((255,255,255))
            self.tbeg = wx.TextCtrl(mw,-1,pos=(500,25*(2*i+2)))
            self.tbeg.Enable(False)
            self.tbeg.SetValue("00:00:00")
            self.beg=0
            self.tbeg.Bind(wx.EVT_KILL_FOCUS, self.timebeg)
            self.label2 = wx.StaticText(mw,-1,label="End:",pos=(625,25*(2*i+2)))
            self.label2.SetForegroundColour((255,255,255))
            self.tend = wx.TextCtrl(mw,-1,pos=(675,25*(2*i+2)))
            self.tend.Enable(False)
            self.tend.SetValue("00:00:00")
            self.end=0
            self.tend.Bind(wx.EVT_KILL_FOCUS, self.timeend)
            self.clip=None
            self.size=0
            self.browse = wx.Button(mw,label="Browse",pos=(350,25*(2*i+2)))
            self.browse.Bind(wx.EVT_BUTTON,self.browsefile)
            self.rem=wx.BitmapButton(mw,wx.ID_ANY,wx.Bitmap('Image/remove.png'),pos=(800,25*(2*i+2)-5))
            self.rem.Bind(wx.EVT_BUTTON,self.remove)
            self.up=wx.BitmapButton(mw,wx.ID_ANY,wx.Bitmap('Image/up.png'),pos=(850,25*(2*i+2)-5))
            self.up.Bind(wx.EVT_BUTTON,self.moveup)
            self.down=wx.BitmapButton(mw,wx.ID_ANY,wx.Bitmap('Image/down.png'),pos=(900,25*(2*i+2)-5))
            self.down.Bind(wx.EVT_BUTTON,self.movedown)
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
        def browsefile(self,event=None):
            global mw
            filters="Windows Media Video Files(*.wmv)|*.wmv|MPEG-4 Files(*.mp4)|*.mp4|Audio Video Interleave Files(*.avi)|*.avi|Matroska Files(*.mkv)|*.mkv|All Video Files(*.wmv,*.mp4,*.avi,*.mkv)|*.wmv;*.mp4;*.avi;*.mkv"
            dlg = wx.FileDialog(mw, message="Open File", wildcard=filters, style=wx.OPEN)
            dlg.SetFilterIndex(4)
            if dlg.ShowModal() == wx.ID_OK:
                self.fn = dlg.GetPath()
            dlg.Destroy()
            global fil
            result=fil.search(self.fn)
            if result:
                self.tbeg.Enable(True)
                self.tend.Enable(True)
                fn=self.fn.split("\\")
                self.label.SetLabel("File: "+fn[len(fn)-1])
                self.clip=FReader(self.fn)
                self.tbeg.SetValue("00:00:00")
                self.end=self.clip.duration
                def conv(t):
                    if(t<10):
                        return '0'+str(t)
                    return str(t)
                self.size=conv(int(self.clip.duration/3600))+":"+conv(int((int(self.clip.duration)%3600)/60))+":"+conv(int(self.clip.duration)%60)
                self.tend.SetValue(self.size)
                del self.clip
                self.clip=None
            elif self.fn=="":
                pass
            else:
                self.label.SetLabel("")
                dlg=wx.MessageDialog(mw,'Invalid File Type','Error',wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

        def timebeg(self,event=None):
                global tim,mw
                temp= self.tbeg.GetValue()
                self.tbeg.Destroy()
                self.tbeg=wx.TextCtrl(mw,pos=(500,25*(2*self.i+2)))
                self.tbeg.Bind(wx.EVT_KILL_FOCUS, self.timebeg)
                self.tbeg.SetValue(temp)
                temp= self.tend.GetValue()
                result=tim.search(self.tbeg.GetValue())
                if not result:
                    dlg=wx.MessageDialog(mw,"Invalid Time Format (hh:mm:ss)",'Error',wx.OK)
                    dlg.ShowModal()
                    dlg.Destroy()
                    self.beg=0
                    self.tbeg.SetValue("00:00:00")
                else:
                    a=self.tbeg.GetValue().split(':')
                    self.beg=int(a[0])*3600+int(a[1])*60+int(a[2])
                    if self.beg>=self.end:
                        dlg=wx.MessageDialog(mw,"Begin Time Cannot Exceed End Time",'Error',wx.OK)
                        dlg.ShowModal()
                        dlg.Destroy()
                        self.beg=0
                        self.tbeg.SetValue("00:00:00")

        def timeend(self,event=None):
                global tim,mw
                temp= self.tend.GetValue()
                self.tend.Destroy()
                self.tend=wx.TextCtrl(mw,pos=(675,25*(2*self.i+2)))
                self.tend.Bind(wx.EVT_KILL_FOCUS, self.timeend)
                self.tend.SetValue(temp)
                result=tim.search(self.tend.GetValue())
                if not result:
                    dlg=wx.MessageDialog(mw,"Invalid Time Format (hh:mm:ss)",'Error',wx.OK)
                    dlg.ShowModal()
                    dlg.Destroy()
                    self.beg=0
                    self.tend.SetValue(self.size)
                else:
                    a=self.tend.GetValue().split(':')
                    b=self.size.split(':')
                    self.end=int(a[0])*3600+int(a[1])*60+int(a[2])
                    c=int(b[0])*3600+int(b[1])*60+int(b[2])
                    if self.end>c or self.end<=self.beg:
                        t=''
                        if self.end>c:
                            t="End Time Cannot Exceed Duration Of Clip"
                        else:
                            t="End Time Cannot Be Less Than Begin Time"
                        dlg=wx.MessageDialog(mw,t,'Error',wx.OK)
                        dlg.ShowModal()
                        dlg.Destroy()
                        self.end=c
                        self.tend.SetValue(self.size)

        def moveup(self,event=None):
            global l
            temp=l[self.i-1].label.GetLabel()
            l[self.i-1].label.SetLabel(self.label.GetLabel())
            self.label.SetLabel(temp)
            l[self.i-1].fn,self.fn=self.fn,l[self.i-1].fn
            temp=l[self.i-1].tbeg.IsEnabled()
            l[self.i-1].tbeg.Enable(self.tbeg.IsEnabled())
            self.tbeg.Enable(temp)
            a,b=l[self.i-1].tbeg.GetValue(),self.tbeg.GetValue()
            l[self.i-1].tbeg.SetValue(b)
            self.tbeg.SetValue(a)
            l[self.i-1].beg,self.beg=self.beg,l[self.i-1].beg
            temp=l[self.i-1].tend.IsEnabled()
            l[self.i-1].tend.Enable(self.tend.IsEnabled())
            self.tend.Enable(temp)
            a,b=l[self.i-1].tend.GetValue(),self.tend.GetValue()
            l[self.i-1].tend.SetValue(b)
            self.tend.SetValue(a)
            l[self.i-1].clip,self.clip=self.clip,l[self.i-1].clip
            l[self.i-1].size,self.size=self.size,l[self.i-1].size
        
        def movedown(self,event=None):
            global l
            temp=l[self.i+1].label.GetLabel()
            l[self.i+1].label.SetLabel(self.label.GetLabel())
            self.label.SetLabel(temp)
            l[self.i+1].fn,self.fn=self.fn,l[self.i+1].fn
            a,b=l[self.i+1].tbeg.IsEnabled(),self.tbeg.IsEnabled()
            l[self.i+1].tbeg.Enable(b)
            self.tbeg.Enable(a)
            a,b=l[self.i+1].tbeg.GetValue(),self.tbeg.GetValue()
            l[self.i+1].tbeg.SetValue(b)
            self.tbeg.SetValue(a)
            l[self.i+1].beg,self.beg=self.beg,l[self.i+1].beg
            a,b=l[self.i+1].tend.IsEnabled(),self.tend.IsEnabled()
            l[self.i+1].tend.Enable(b)
            self.tend.Enable(a)
            a,b=l[self.i+1].tend.GetValue(),self.tend.GetValue()
            l[self.i+1].tend.SetValue(b)
            self.tend.SetValue(a)
            l[self.i+1].clip,self.clip=self.clip,l[self.i+1].clip
            l[self.i+1].size,self.size=self.size,l[self.i+1].size
                    
        def remove(self,event=None):
            global i,l,posy,outl,outlab,outbrowse,outlab1,outfn,edbut
            if i>1:
                a= l[self.i]
                a.label.Destroy()
                a.label1.Destroy()
                a.tbeg.Destroy()
                a.label2.Destroy()
                a.tend.Destroy()
                a.browse.Destroy()
                a.rem.Destroy()
                a.up.Destroy()
                a.down.Destroy()
                for j in range(self.i+1,len(l)):
                    l[j].i-=1
                    l[j].label.MoveXY(x=25,y=25*(2*l[j].i+2))
                    l[j].browse.MoveXY(x=350,y=25*(2*l[j].i+2))
                    l[j].label1.MoveXY(x=450,y=25*(2*l[j].i+2))
                    l[j].tbeg.MoveXY(x=500,y=25*(2*l[j].i+2))
                    l[j].label2.MoveXY(x=625,y=25*(2*l[j].i+2))
                    l[j].tend.MoveXY(x=675,y=25*(2*l[j].i+2))
                    l[j].rem.MoveXY(x=800,y=25*(2*l[j].i+2)-5)
                    l[j].up.MoveXY(x=850,y=25*(2*l[j].i+2)-5)
                    l[j].down.MoveXY(x=900,y=25*(2*l[j].i+2)-5)
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
        video = concatenate(clip)
        video.to_videofile(direct+'/'+outfn.GetValue(),fps=25, codec='mpeg4')
        temp=range(len(clip))
        for i in temp:
            del clip[0].reader,clip[0].audio.reader,clip[0]
        del clip
    
    def edit(event=None):
        global mw,l,direct,outfn,posy
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
            vid=[]
            clip=[]
            for k in l:
                cl=VideoFileClip(k.fn)
                vid.append(cl)
                clip.append(cl.subclip(k.beg,k.end))
            con(clip)
            temp=range(len(vid))
            for k in temp:
                del vid[0].reader,vid[0].audio.reader,vid[0]

            del vid
            temp=range(len(l))
            for k in temp:
                l[0].label.Destroy()
                l[0].label1.Destroy()
                l[0].tbeg.Destroy()
                l[0].label2.Destroy()
                l[0].tend.Destroy()
                l[0].browse.Destroy()
                l[0].rem.Destroy()
                l[0].up.Destroy()
                l[0].down.Destroy()
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
            outfn.SetValue('')
            direct=''
            edbut.MoveXY(x=725,y=posy)
            dlg=wx.MessageDialog(mw,"Editing Completed Successfully",'Error',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            l.append(item(0))
            outfn.Destroy()
            outfn=wx.TextCtrl(mw,pos=(600,posy))
            outfn.Bind(wx.EVT_KILL_FOCUS, checkfn)
        
    def checkfn(event=None):
        global fname,outfn,mw
            
        result=fname.search(outfn.GetValue())
        if result or outfn.GetValue()=='':
            temp= outfn.GetValue()
            outfn.Destroy()
            outfn=wx.TextCtrl(mw,pos=(600,posy))
            outfn.Bind(wx.EVT_KILL_FOCUS, checkfn)
            outfn.SetValue(temp)
        else:
            outfn.SetValue('')
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
    vedit()
