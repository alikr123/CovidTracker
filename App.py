import threading
import time
import signal
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
import CovidPkRequest


WAIT_TIME=3600 #1 hour
THREAD_RUN=True

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    global THREAD_RUN
    THREAD_RUN=False
    exit(0)

c=CovidPkRequest.collectData()
data=c.get_data()

class FetchData(threading.Thread):
    """
    Thread to start Web Server
    """
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if THREAD_RUN==False:
                print("I AM BREAKING")
                break
            global data
            data = c.get_data()
            time.sleep(WAIT_TIME)


class Pakistan(GridLayout):
    def __init__(self, **kwargs):
        super(Pakistan, self).__init__(**kwargs)
        self.cols=2
        self.rows=4
        self.columnNames=[]
        self.columnValues=[]
        self.extract_data_Pakistan()
        self.create_labels()
        Clock.schedule_interval(lambda dt: self.update_vals(), WAIT_TIME)

    def create_labels(self):
        for i in range(0,self.rows):
            self.add_widget(Label(text = str(self.columnNames[i])))
            self.add_widget(Label(text = str(self.columnValues[i])))

    def update_labels(self):
        widget_list=[]
        for widget in self.walk():
            widget_list.append(widget)
        widget_list=widget_list[1:len(widget_list)]
        j=0
        for i in range(0,self.rows+self.cols+1,2):
            widget_list[i].text = str(self.columnNames[j])
            widget_list[i+1].text = str(self.columnValues[j])
            j=j+1


    def extract_data_Pakistan(self):
        for graph in data:
            if graph['Title']=='Overview of Cases in Pakistan':
                for columns in graph['data']:
                    self.columnNames.append(columns['columnName'])
                    self.columnValues.append(int(columns['column_data'][int(len(columns['column_data'])-1)]))

        self.columnNames = self.columnNames[1:len(self.columnNames)]
        self.columnValues = self.columnValues[1:len(self.columnValues)]


    def update_vals(self):
        print("Updating Labels")
        self.columnNames.clear()
        self.columnValues.clear()
        self.extract_data_Pakistan()
        self.update_labels()
    # #pass
    # def __init__(self, **kwargs):
    #     super(MyGrid, self).__init__(**kwargs)
    #     #self.cols = 2
    #
    #     self.ct=Covid_tracker.CovidTrackerPk()
    #     self.ct.update_values()
    #     self.get_values()
    #     Clock.schedule_interval(lambda dt: self.update_vals(), 60)
    #
    # def get_values(self):
    #     print("a")
    #     # (self.ids['cases']).text = self.ct.get_cases()
    #     # (self.ids['deaths']).text = self.ct.get_deaths()
    #     # (self.ids['recoverd']).text = self.ct.get_recoverd()
    #     # (self.ids['sindh']).text = self.ct.get_sindh()
    #     # (self.ids['punjab']).text = self.ct.get_punjab()
    #     # (self.ids['balochistan']).text = self.ct.get_balochistan()
    #     # (self.ids['kpk']).text = self.ct.get_kpk()
    #     # (self.ids['ajk']).text = self.ct.get_ajk()
    #     # (self.ids['gb']).text = self.ct.get_gb()
    #     # (self.ids['ict']).text = self.ct.get_ict()
    #
    # def update_vals(self):
    #     self.ct.update_values()
    #     self.get_values()

class Provinces(GridLayout):
    def __init__(self, **kwargs):
        super(Provinces, self).__init__(**kwargs)
        self.cols=5
        self.rows=8
        self.columnNames=[]
        self.columnValues=[]
        self.extract_data_Provinces()
        self.create_labels()

    def create_labels(self):
        for i in range(0,self.cols):
            self.add_widget(Label(text = str(self.columnNames[i])))

        for value in self.columnValues:
            try:
                value=int(value)
            except:
                pass
            self.add_widget(Label(text = str(value)))

        # self.add_widget(Label(text = str(self.columnValues[i])))

    def extract_data_Provinces(self):
        for graph in data:
            if graph['Title']=='Provinces Details':
                for columns in graph['data']:
                    self.columnNames.append(columns['columnName'])
                    self.columnValues.append(columns['column_data'])

        rows_list=[]
        for i in range(0,self.rows-1):
            for list in self.columnValues:
                rows_list.append(list[i])

        self.columnValues=rows_list


#
class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        # layout =BoxLayout(orientation='horizontal')
        # a=MyGrid()
        # b=MyGrid1()
        # layout.add_widget(a)
        # layout.add_widget(b)

class CovidTrackerApp(App):
    def build(self):
        self.title = 'COVID TRACKER'
        #return MyGrid()
        return ContainerBox()

    def on_stop(self):
        # self.textpopup(title='Exit', text='Are you sure?')
        print("Kivy app closing")
        global THREAD_RUN
        THREAD_RUN = False
        return True

if __name__ == "__main__":
    FETCH_DATA_THREAD = FetchData()
    FETCH_DATA_THREAD .start()
    print("Thread started")

    # Config.set('graphics', 'fullscreen', 'auto')
    # Config.set('graphics', 'window_state', 'maximized')
    # Config.write()
    try:
        Window.fullscreen = False
        # Config.set('graphics', 'width', '320')
        # Config.set('graphics', 'height', '240')
        # Config.write()
    except:
        pass
    CovidTrackerApp().run()
    print("App Started")
