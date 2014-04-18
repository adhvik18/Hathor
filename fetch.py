import wx
class Dialog(wx.Dialog):
    def __init__(self):
        super(Dialog,self).__init__(None,title="Enter Details",size=(220,220))
        self.label1=wx.StaticText(self,-1,label="Unable to automatically fetch lyrics.",pos=(10,10))
        self.label2=wx.StaticText(self,-1,label="Enter the following details to fetch.",pos=(10,30))
        self.title=wx.TextCtrl(self,-1,pos=(80,60))
        self.tlabel=wx.StaticText(self,-1,label="Title:",pos=(30,60))
        self.artist=wx.TextCtrl(self,-1,pos=(80,110))
        self.alabel=wx.StaticText(self,-1,label="Artist:",pos=(30,110))
        self.button=wx.Button(self,wx.ID_OK,label="OK",pos=(100,160))
        self.button.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)

    def onOk(self,event=None):
        self.Destroy()
        self.Close()
        
def getLyrics(filename):
    import urllib2
    import re
    import pydub
    info=pydub.utils.mediainfo(filename)
    if 'TAG' in info and 'artist' in info['TAG'] and 'title' in info['TAG']:
        artist=info['TAG']['artist'].lower().replace(' ','').strip()
        title=info['TAG']['title'].lower().replace(' ','').strip()
    else:
        dlg=Dialog()
        artist,title='',''
        dlg.ShowModal()
        artist=dlg.artist.GetValue().lower().replace(' ','').strip()
        title=dlg.title.GetValue().lower().replace(' ','').strip()
        print artist,title
        dlg.Destroy()
    url = "http://www.azlyrics.com/lyrics/"+artist+"/"+title+".html"
    print url
    response = urllib2.urlopen(url)
    if response:
        html = response.read()
        creg = re.compile(r'<!-- start of lyrics -->(.*)<!-- end of lyrics -->',re.S)
        result = creg.findall(html)
        if result:
            lyrics=re.sub("<br />|<i>(.*)</i>","",result[0])
            lyrics=re.sub(r'\n+','\n',lyrics)
            return lyrics
        return 'Unable To Fetch Lyrics.'
    return 'Unable To Fetch Lyrics.'

    
