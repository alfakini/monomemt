import threading
from OSC import *
from pymt import *

def binary(n, digits=8):
    '''
    Based on: http://www.daniweb.com/code/snippet216539.html
    '''
    data = '{0:0>{1}}'.format(bin(n)[2:], digits)
    return [int(x) for x in data]

class MTMonome(MTButtonMatrix):
    '''
    An pymt implementation of monome, based on MTButtonMatrix and SerialOSC.
    http://github.com/tehn/serialoscp
    http://monome.org/data/app/monomeserial/osc
    '''

    def __init__(self, **kwargs):
        kwargs.setdefault('matrix_size', (8,8))
        kwargs.setdefault('size', (400, 400))

        super(MTMonome, self).__init__(**kwargs)

        self.prefix = '/box'
        self.address = 'localhost'
        self.output_port = 8000
        self.input_port = 8080

        try:
            self.osc_client = OSCClient()
            self.osc_client.connect((self.address, self.output_port))
        except OSCClientError as e:
            print '[ERROR] OSCClient', e

        try:
            self.osc_server = OSCServer((self.address, self.input_port))
            self.osc_server.addDefaultHandlers()
            self.osc_server.addMsgHandler('default', self.osc_handler)
            self.server_thread = threading.Thread(target=self.osc_server.serve_forever)
            self.server_thread.start()
        except IOError as e:
            print '[ERROR] OSCServer', e


    def on_press(self, state):
        '''
        Send an osc message when a button is touched down an up
        state = (row, column, state)
        /prefix/press [x] [y] [state]
        state: 1 (down) or 0 (up)
        '''
        y = state[0]
        x = state[1]
        state = state[2]

        m = OSCMessage(self.prefix + '/press')
        m.append([y, (self.matrix_size[1]-1)-x, state])

        try:
            self.osc_client.send(m)
        except OSCClientError as e:
            print '[ERROR] OSCClient.send', e

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            i,j = self.collide_point(touch.x, touch.y)
            self.dispatch_event('on_value_change', self.matrix)
            self.dispatch_event('on_press', (i,j, 1))
            self.last_tile = (i,j)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            i,j = self.collide_point(touch.x, touch.y)
            self.dispatch_event('on_value_change', self.matrix)
            self.dispatch_event('on_press', (i,j, 0))
            self.last_tile = (i,j)

    def osc_handler(self, addr, tags, data, client_address):
        '''
        Handle incoming messages
        '''

        print '[OSC]', addr, tags, data, client_address
        
        if addr == self.prefix + '/led':
            '''
            /prefix/led [x] [y] [state]
            state: 1 (on) or 0 (off)
            '''

            x = data[0]
            y = (self.matrix_size[1]-1)-data[1]
            state = data[2]
            
            self.matrix[x][y] = state

        elif addr == self.prefix + '/led_row':
            '''
            /prefix/led_row [row] [data]
            row: which row to update
            data: one byte of data (8 led positions)
            '''

            row = (self.matrix_size[1]-1)-data[0]
            data = binary(data[1]) #ex. [1,0,1,0,1,0,0,1]
                    
            for i in range(self.matrix_size[1]):
                self.matrix[i][row] = data[i]

        elif addr == self.prefix + '/led_col':
            '''
            /prefix/led_col [col] [data]
            col: which column to update
            data: one byte of data (8 led positions)
            '''

            column = data[0]
            data = binary(data[1])

            self.matrix[column] = data

        elif addr == self.prefix + '/frame':
            '''
            /prefix/frame [A B C D E F G H]
            update a display, offset by x and y.
            '''
            
            self.matrix = [binary(y) for y in data]
        
        elif addr == self.prefix + '/clear':
            '''
            /prefix/clear [state]
            state: 0 (off, default if unspecified) or 1 (on)
            '''
      
            if len(data):
                self.clear(data[0])
            else: 
                self.clear(0)

        #Sys Msgs
        elif addr == '/sys/prefix':
            '''
            /sys/prefix [string]
            change prefix to [string]

            Return:
            /sys/prefix [newprefix]
            '''
            
            prefix = data[0]
            self.prefix = prefix

            m = OSCMessage('/sys/press')
            m.append(self.prefix)

            try:
                self.osc_client.send(m)
            except OSCClientError as e:
                print '[ERROR] OSCClient.send', e

            
        elif addr == '/sys/cable':
            '''
            /sys/cable [left|up|right|down]
            changes cable setting for the unit
            '''

            pass

        elif addr == '/sys/offset':
            '''
            /sys/offset x y
            changes offset value for the unit
            '''
            
            pass

        elif addr == '/sys/intensity':
            '''
            /sys/intensity 0.
            changes unit intensity
            '''

            self.intensity(data[0])

        elif addr == '/sys/test':
            '''
            /sys/test [0|1]
            toggles test mode for the unit (turn on/off all leds)
            '''

            if data[0]:
                import time

                for i in range(9):
                    self.clear(i%2)
                    time.sleep(0.5)

        elif addr == '/sys/report':
            '''
            /sys/report
            Return:
            /sys/prefix
            /sys/cable
            /sys/offset
            '''

            pass

        return

    def clear(self, state):
        if state:
            self.matrix = [[1 for i in range(self.matrix_size[1])] for j in range(self.matrix_size[0])]
        else:
            self.reset()

    def intensity(self, intensity):
        r, g, b, i = self.downcolor
        self.downcolor = (r,g,b,intensity)

    def close(self):
        self.osc_client.close()
        self.osc_server.close()
        self.server_thread.join()

class MTScatterMonome(MTScatterWidget):

    def __init__(self, **kwargs):
        self.monome = MTMonome()
        kwargs.setdefault('size', (self.monome.width + 30, self.monome.height + 30))
        super(MTScatterMonome, self).__init__(**kwargs)
        self.monome.pos = (15 + self.monome.x, 15 + self.monome.y)
        self.add_widget(self.monome)

if __name__ == '__main__':

    additional_css = '''
    .simple {
            border-width: 3;
            draw-border: 1;
            bg-color:  rgb(100, 100, 200, 255);
            touch-color: rgba(100, 100, 250, 255);
    }

    .dois {
            border-width: 3;
            draw-border: 1;
            bg-color:  rgb(200, 100, 100, 255);
            touch-color: rgba(100, 100, 250, 255);
    }
    '''

    css_add_sheet(additional_css)

    window = MTWindow()

    #monome = MTMonome()
    #window.add_widget(monome)

    smonome = MTScatterMonome(cls=('simple'))
    window.add_widget(smonome)
    
    try:
        runTouchApp()
    except KeyboardInterrupt:
        #monome.close()
        smonome.monome.close()
