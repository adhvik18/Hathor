import wx
import wx.media
import wx.lib.agw.peakmeter as PM
import wx.lib
import record
import multiprocessing
import os

os.chdir(os.getcwd()+'/Data')

class Hathor(wx.Frame):
        
        def __init__(self,parent,title):
                super(Hathor,self).__init__(parent,title=title,size=(816,600))
                self.InitUI()
                self.Centre()
                self.Show()
        
        def InitUI(self):
                self.AddIcon()
                self.AddMenuBar()
                self.AddMainUI()
                
                
                
        
                
        def AddMainUI(self):
                self.mainPanel = wx.Panel(self)
                self.mainPanel.Bind(wx.EVT_PAINT,self.OnPaint)
                self.scroll = wx.ScrolledWindow(self.mainPanel,-1,pos=(600,0),size=(200,520))
                self.scroll.SetBackgroundColour((21,21,21))
                self.Bitmap=None
                self.disp=None
                sizer = wx.GridBagSizer(6,6)
                
                self.statusBar = self.CreateStatusBar()
                self.statusBar.SetStatusText('No File specified')
                
                self.imagePanel=wx.Panel(self.mainPanel,pos=(0,0),size=(550,400))
                self.player = wx.media.MediaCtrl(self.imagePanel,size=(550,400),style=wx.SIMPLE_BORDER)
                
                self.play = wx.BitmapButton(self.mainPanel,wx.ID_ANY,wx.Bitmap('Image/play.png'),pos=(0,430))
                self.play.Bind(wx.EVT_BUTTON,self.playFile)
                self.pause = wx.BitmapButton(self.mainPanel,wx.ID_ANY,wx.Bitmap('Image/pause.png'),pos=(40,430))
                self.pause.Bind(wx.EVT_BUTTON,self.pauseFile)
                self.rec = wx.BitmapButton(self.mainPanel,wx.ID_ANY,wx.Bitmap('Image/mike.png'),pos=(80,430))
                self.rec.Bind(wx.EVT_BUTTON,self.recFile)
                self.slider = wx.Slider(self.mainPanel,wx.ID_ANY,size = (550,-1),pos=(0,400))
                self.slider.SetBackgroundColour((21,21,21))
                self.slider.Bind(wx.EVT_SCROLL,self.stopSeek)
                self.slider.Bind(wx.EVT_SCROLL_CHANGED,self.seek)
                self.slider1 = wx.Slider(self.mainPanel,wx.ID_ANY,size = (76,-1),pos=(474,445),style=wx.SL_HORIZONTAL|wx.SL_TOP)
                self.peak = PM.PeakMeterCtrl(self.mainPanel, -1, style=wx.SIMPLE_BORDER, pos=(487,425),agwStyle=PM.PM_HORIZONTAL,size=(50,20))
                self.peak.SetMeterBands(1, 12)
                self.slider1.SetRange(0,100)
                self.peak.SetData((50,), 0, 1)
                self.slider1.SetValue(50)
                self.slider1.Bind(wx.EVT_SCROLL,self.volume)
                self.slider1.SetBackgroundColour((21,21,21))
                self.timer = wx.Timer(self)
                self.Bind(wx.EVT_TIMER,self.OnTimer)

        def OnPaint(self,e):
                bdc=wx.PaintDC(self.mainPanel)
                dc=wx.GCDC(bdc)
                dc.Clear()
                dc.DrawBitmap(wx.Bitmap('Image/background.jpg'),0,0,True)

                
        def recFile(self,e):
                self.statusBar.SetStatusText('Recording....')
                record.record_to_file()
                self.statusBar.SetStatusText('Done Recording!!!') 

                
        def playFile(self,e):
                print "playing"
                self.player.Play()
                self.slider.SetRange(0,self.player.Length())
                self.player.SetVolume(float(self.slider1.GetValue())/100)
                self.timer.Start(100)
        
        def pauseFile(self,e):
                self.player.Pause()
                self.timer.Stop()

        def volume(self,e):
                self.peak.SetData((self.slider1.GetValue(),),0,1)
                self.player.SetVolume(float(self.slider1.GetValue())/100)

        def stopSeek(self,e):
                self.timer.Stop()
                
        def seek(self,e):
                self.player.Seek(self.slider.GetValue())
                self.timer.Start(100)
                
        def AddIcon(self):
                ico = wx.Icon('Image/icon.ico',wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
                
        def AddMenuBar(self):
                menus = wx.MenuBar()
                fileMenu = wx.Menu()
                openItem = wx.MenuItem(fileMenu,0,'&Open\tCtrl+O')
                openItem.SetBitmap(wx.Bitmap('Image/open.png'))
                quitItem = wx.MenuItem(fileMenu,1,'&Quit\tCtrl+Q')
                quitItem.SetBitmap(wx.Bitmap('Image/exit.png'))
                fileMenu.AppendItem(openItem)
                fileMenu.AppendItem(quitItem)
                menus.Append(fileMenu,'&File')
                editMenu = wx.Menu()
                editVid=wx.MenuItem(editMenu,2,'&Edit Video\tCtrl+1')
                editVid.SetBitmap(wx.Bitmap('Image/vedit.png'))
                editAud=wx.MenuItem(editMenu,3,'&Edit Audio\tCtrl+2')
                editAud.SetBitmap(wx.Bitmap('Image/aedit.png'))
                editIm=wx.MenuItem(editMenu,4,'&Edit Image\tCtrl+3')
                editIm.SetBitmap(wx.Bitmap('Image/iedit.png'))
                editMenu.AppendItem(editVid)
                editMenu.AppendItem(editAud)
                editMenu.AppendItem(editIm)
                menus.Append(editMenu,'&Edit')
                helpMenu = wx.Menu()
                helpHelp=wx.MenuItem(helpMenu,5,'&Help Contents\tF1')
                helpHelp.SetBitmap(wx.Bitmap('Image/help.png'))
                helpAbt=wx.MenuItem(helpMenu,6,'&About\tF2')
                helpAbt.SetBitmap(wx.Bitmap('Image/about.png'))
                helpMenu.AppendItem(helpHelp)
                helpMenu.AppendItem(helpAbt)
                menus.Append(helpMenu,'&Help')
                self.Bind(wx.EVT_MENU,self.onOpen,openItem)
                self.Bind(wx.EVT_MENU,self.onQuit,quitItem)
                self.Bind(wx.EVT_MENU,self.editVideo,editVid)
                self.Bind(wx.EVT_MENU,self.editAudio,editAud)
                self.Bind(wx.EVT_MENU,self.editImage,editIm)
                self.Bind(wx.EVT_MENU,self.helpcontents,helpHelp)
                self.Bind(wx.EVT_MENU,self.aboutpage,helpAbt)
                
                self.SetMenuBar(menus)

        def helpcontents(self,e):
                import webbrowser
                webbrowser.get("windows-default").open("http://www.hathor.net78.net/help.html")

        def aboutpage(self,e):
                description='''                                         Hathor is a multimedia player/editor for the Windows operating system.                 
Features include audio/video player, image viewer, voice recorder, audio/video/image editor, and a lyrics fetcher.          '''
                licence='''Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to dealin the Software without restriction, including without limitation the rightsto use, copy, modify, merge, publish, distribute, sublicense, and/or sellcopies of the Software, and to permit persons to whom the Software isfurnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''
                info = wx.AboutDialogInfo()
                info.SetIcon(wx.Icon('Image/about.png', wx.BITMAP_TYPE_PNG))
                info.SetName('Hathor')
                info.SetVersion('1.0')
                info.SetDescription(description)
                info.SetCopyright('(C) 2014 Media++')
                info.SetWebSite(('http://www.hathor.net78.net/home.html',"Hathor Website"))
                info.SetLicence(licence)
                info.SetDevelopers(['Akshata Bhat(Team Leader)','Mukund M K(Subordinate)','Adhvik Shetty','Amar Ichangimath','Chandrakanth Cheturvedi','Chandrika Amarkhed','Gurudatta A','Jyothi P'])
                wx.AboutBox(info)

        
        def onOpen(self,e):     
                filters = 'Audio Files (*.wav,*.mp3)|*.wav;*.mp3|Video Files (*.wmv,*.mp4,*.avi,*.mkv)|*.wmv;*.mp4;*.avi;*.mkv|Image Files (*.png,*.jpg,*.jpeg,*.gif,*.bmp)|*.png;*.jpg;*.jpeg;*.gif;*.bmp'
                dlg = wx.FileDialog(self, message="Open File", wildcard=filters, style=wx.OPEN)
                if dlg.ShowModal() == wx.ID_OK:
                        filename = dlg.GetPath()
                        fil= dlg.GetFilterIndex()
                        self.statusBar.SetStatusText(filename);
                        self.onLoad(filename,fil)
                        print 'Opening ',filename
                dlg.Destroy()   
                
        def onLoad(self,filename,fil):
                if self.Bitmap!=None:
                        self.Bitmap.Destroy()
                        self.Bitmap=None
                if fil==2:
                        self.Bitmap = wx.StaticBitmap(self.imagePanel,-1,wx.BitmapFromImage(wx.Image(filename,wx.BITMAP_TYPE_ANY,-1)))
                else:
                        if not self.player.Load(filename):
                                wx.MessageBox("Unable to load file")
                        else:
                                self.slider.SetRange(0,self.player.Length())
                                self.player.Play()
                                if fil==0:
                                        import fetch
                                        self.lyrics = fetch.getLyrics(filename)
                                        a=self.lyrics.split('\n')
                                        height=len(a)
                                        if self.disp!=None:
                                                self.disp.Destroy()
                                                self.scroll.SetScrollbars(0,0,0,0)
                                        if height<=32:
                                                self.scroll.SetScrollbars(0,0,0,0)
                                        else:
                                                self.scroll.SetScrollbars(0,int(500//30),0,height)
                                        self.disp = wx.StaticText(self.scroll,-1,label=self.lyrics)
                                        self.disp.SetForegroundColour((255,255,255))
                
        def onQuit(self,e):
                print 'Quit'
                self.Close()

        def editVideo(self,e):
                print 'Edit Video'
                import veditor
                veditor.vedit()
                pass
        
        def editAudio(self,e):
                print 'Edit Audio'
                import aeditor
                aeditor.aedit()
                pass

        def editImage(self,e):
                print 'Edit Image'
                import ieditor
                a=ieditor.PhotoCtrl()
                a.MainLoop()
                pass
        
        
        def OnTimer(self,e):
                current = self.player.Tell()
                self.slider.SetValue(current)
        
if __name__ == '__main__':
        app = wx.App()
        Hathor(None,title = "Hathor")
        app.MainLoop()
        
