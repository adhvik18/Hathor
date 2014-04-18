import os
import wx
from PIL import Image as ImageEditor
class PhotoCtrl(wx.App):
    
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Image Editor',pos=(0,0),size=(700,500))
        self.panel = wx.Panel(self.frame,size=(600,400))
        self.panel.SetBackgroundColour((21,21,21))
        ico = wx.Icon('Image/icon.ico',wx.BITMAP_TYPE_ICO)
        self.frame.SetIcon(ico)
        self.i=0   
        self.PhotoMaxSize = 300
 
        self.createWidgets()
        self.frame.Center()
        self.frame.Show()

    def createWidgets(self):
        instructions = 'Browse for an image'
        self.img = wx.EmptyImage(400,300)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(self.img),pos=(20,20))
 
        instructLbl = wx.StaticText(self.panel, label=instructions,pos=(20,350))
        instructLbl.SetForegroundColour((255,255,255))
        instructLbl.SetBackgroundColour((21,21,21))
        
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1),pos=(150,350))
        browseBtn = wx.Button(self.panel, label='Browse',pos=(400,349))
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
		
        rotateBtn=wx.Button(self.panel,label="Rotate",pos=(550,250))
        rotateBtn.Bind(wx.EVT_BUTTON, self.onRotate)
        WText="Crop Width by: "
        HText="Crop Height by :"
        wTextLbl = wx.StaticText(self.panel, label=WText ,pos=(450,100),style=wx.TRANSPARENT_WINDOW)
        wTextLbl.SetForegroundColour((255,255,255))
        hTextLbl = wx.StaticText(self.panel, label=HText, pos=(450,150))
        hTextLbl.SetForegroundColour((255,255,255))
        self.cropX = wx.TextCtrl(self.panel, pos=(550,100),size=(50,-1))
        self.cropY = wx.TextCtrl(self.panel, pos=(550,150),size=(50,-1))
        cropBtn=wx.Button(self.panel,label="Resize",pos=(450,200))
        cropBtn.Bind(wx.EVT_BUTTON, self.onResize)
        originalBtn=wx.Button(self.panel,label="Original",pos=(550,200))
        originalBtn.Bind(wx.EVT_BUTTON, self.Original)
        saveBtn=wx.Button(self.panel,label="Save",pos=(550,349))
        saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        bandMergeBtn=wx.Button(self.panel,label="Greyscale",pos=(450,250))
        bandMergeBtn.Bind(wx.EVT_BUTTON, self.bandMerge) 		
 
        self.panel.Layout()
    def onSave(self,event):
        """
        """
        self.pil.save("editedimage"+str(self.i)+".jpg")
        self.i=self.i+1	
    def onRotate(self, event):
        """	 
        """	
        img_centre = wx.Point( self.img.GetWidth()/2,self.img.GetHeight()/2 )
        self.img=self.img.Rotate90()
        W = self.img.GetWidth()
        H = self.img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        self.img = self.img.Scale(NewW,NewH)
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.img))
        self.panel.Refresh() 		
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.onView()
    def bandMerge(self,event):
        r, g, b = self.pil.split()
        im = ImageEditor.merge("RGB", (g,g,g))
        im.save("MERGE.jpg")
        image = wx.EmptyImage(im.size[0],im.size[1])
        new_image= im.convert('RGB')
        data = new_image.tostring()
        self.img.SetData(data)
        self.img = self.img.Scale(self.originalW,self.originalH)		
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.img))
        self.panel.Refresh()
        im.save("MERGE.jpg")		
    def Original(self,event):
        """
        """  				
        self.img = self.img.Scale(self.originalW,self.originalH)		
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.img))
        self.panel.Refresh()
        self.pil = ImageEditor.new('RGB', (self.originalW,self.originalH)) 
        self.pil.fromstring(self.img.GetData())		
    def onResize(self,event):
        """
        """
        x=self.cropX.GetValue()
        y=self.cropY.GetValue()
        if(x!=""):
            x=int(x)
        else:
            x=0
        if(y!=""):
            y=int(y)
        else:
            y=0			
        print(x,y) 		
        G=self.img.GetWidth()-x	
        H=self.img.GetHeight()-y		
         		
        box=(0,0,10,10) 		 
        self.pil=self.pil.crop(box)        
        self.img = self.img.Scale(G,H)		
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.img))
        self.panel.Refresh()
    def onView(self):
        filepath = self.photoTxt.GetValue()
        if(filepath==""):
            return
        self.img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        self.origin=self.img
        W = self.img.GetWidth()
        H = self.img.GetHeight()
        
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        self.originalW=NewW
        self.originalH=NewH	
        self.img = self.img.Scale(NewW,NewH)
        self.pil = ImageEditor.new('RGB', (NewW,NewH))
        self.pil.fromstring(self.img.GetData())
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.img))
        self.panel.Refresh()
		
	
if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
