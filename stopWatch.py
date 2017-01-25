import tkinter as tk
import time


class StopWatch(tk.Frame):
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        tk.Frame.__init__(self, parent, kw)

        self.start = 0.0
        self.endtime = 0.0
        self.elapsedtime = 0.0
        self.running = 0
        self.Endminutes = 0
        self.Endseconds = 0
        self.Endhseconds = 0
        self.timestr = tk.StringVar()

    def update(self):
        """ Update the label with elapsed time. """
        self.elapsedtime = time.time() - self.start
        self.setTime(self.elapsedtime)
        self.timer = self.after(50, self.update)

    def setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        self.Endminutes = int(elap/60)
        self.Endseconds = int(elap - self.Endminutes*60.0)
        self.Endhseconds = int((elap - self.Endminutes*60.0 - self.Endseconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (self.Endminutes, self.Endseconds, self.Endhseconds))

    def getEndtime(self):

        self.endtime = self.timestr.get()


    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self.running:
            self.start = time.time() - self.elapsedtime
            self.update()
            self.running = 1

    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self.running:
            self.getEndtime()
            self.after_cancel(self.timer)
            self.elapsedtime = time.time() - self.start
            self.setTime(self.elapsedtime)
            self.running = 0

    def Reset(self):                                  
        """ Reset the stopwatch. """
        self.start = time.time()
        self.elapsedtime = 0.0
        self.setTime(self.elapsedtime)


def main():
    root = tk.Tk()
    sw = StopWatch(root)
    sw.pack(side=tk.TOP)

    tk.Button(root, text='Start', command=sw.Start).pack(side=tk.LEFT)
    tk.Button(root, text='Stop', command=sw.Stop).pack(side=tk.LEFT)
    tk.Button(root, text='Reset', command=sw.Reset).pack(side=tk.LEFT)
    tk.Button(root, text='Quit', command=root.quit).pack(side=tk.LEFT)

    root.mainloop()

if __name__ == '__main__':
    main()