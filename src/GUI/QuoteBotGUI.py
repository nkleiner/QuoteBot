import wx
import tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import os

#function for prompting single-line text from the user
def ask(parent=None, message='', default_value=''):
    dlg = wx.TextEntryDialog(parent, message, value=default_value)
    buttonChoice = dlg.ShowModal()
    result = dlg.GetValue()
    dlg.Destroy()
    if buttonChoice == 5100:
        return result
    else:
        return False


def writeToFile(configDraft):
    
    with open("config.json", "w") as file:
        file.write(configDraft)
        file.close()

    if (os.path.isfile("config.json")):
        message = "config.json file successfully created."
        caption = "File Created"
        confirm=wx.MessageDialog(parent=None, message=message,caption=caption,style=wx.OK|wx.CENTRE, pos=wx.DefaultPosition)
        confirm.ShowModal()
    
#Initialize wx App
app = wx.App()
app.MainLoop()

#Prompts for token
token_value = ask(message = 'Enter Discord token:')
if token_value != False:

    #Writes token to config file
    configDraft='{\n\t"token":"'+token_value+'"'

    #prompts for channel ID
    channelID = ask(message = 'Enter channel ID:')
    if channelID != False:
        configDraft+='\n\t"quoteChannelID":"'+channelID+'"\n}'

        #appends channel ID to config file
        writeToFile(configDraft)
    else:
        #print("Coding is hard")
        message = "config.json file not created."
        caption = "File Error"
        confirm=wx.MessageDialog(parent=None, message=message,caption=caption,style=wx.ICON_ERROR|wx.CENTRE, pos=wx.DefaultPosition)
        confirm.ShowModal()


else:
    #print("Coding is hard")
    message = "config.json file not created."
    caption = "File Error"
    confirm=wx.MessageDialog(parent=None, message=message,caption=caption,style=wx.ICON_ERROR|wx.CENTRE, pos=wx.DefaultPosition)
    confirm.ShowModal()




##
##
##if (os.path.isfile("config.json")):
##    message = "config.json file successfully created."
##    caption = "File Created"
##    confirm=wx.MessageDialog(parent=None, message=message,caption=caption,style=wx.OK|wx.CENTRE, pos=wx.DefaultPosition)
##    confirm.ShowModal()
##    
##else:
##    print("Coding is hard")
##    message = "config.json file not created."
##    caption = "File Error"
##    confirm=wx.MessageDialog(parent=None, message=message,caption=caption,style=wx.ICON_ERROR|wx.CENTRE, pos=wx.DefaultPosition)
##    confirm.ShowModal()





























##class MyFrame(wx.Frame):    
##    def __init__(self):
##        super().__init__(parent=None, title='QuoteBot Setup')
##        panel = wx.Panel(self)        
##        my_sizer = wx.BoxSizer(wx.VERTICAL)        
##        self.text_ctrl = wx.TextCtrl(panel)
##        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
##        my_btn = wx.Button(panel, label='Save Configuration')
##        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
##        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
##        panel.SetSizer(my_sizer)        
##        self.Show()
##
##    def on_press(self, event):
##        value = self.text_ctrl.GetValue()
##        if not value:
##            print("You didn't enter anything!")
##        else:
##            print(f'You typed: "{value}"')
##
##            dirPath = filedialog.askdirectory()
##            fileName = "quoteBot_config.json"
##            file_path = os.path.join(dirPath,fileName)
##            print(file_path)
##            with open(file_path, "w") as file:
##                file.write(f'"token":"{value}"')
##                file.close()
##
##
##if __name__ == '__main__':
##    app = wx.App()
##    frame = MyFrame()
##    app.MainLoop()
