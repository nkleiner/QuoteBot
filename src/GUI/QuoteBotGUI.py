import wx
import tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import os

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='QuoteBot Setup')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        my_btn = wx.Button(panel, label='Save Configuration')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)        
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')

            dirPath = filedialog.askdirectory()
            fileName = "quoteBot_config.json"
            file_path = os.path.join(dirPath,fileName)
            print(file_path)
            with open(file_path, "w") as file:
                file.write(f'userText= {value}')
                file.close()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
