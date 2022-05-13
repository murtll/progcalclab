from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_file('calc.kv')
Builder.load_file('selectors.kv')

class CalcActionSelector(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.actions = []

    def actions_click(self, instance, active, action):
        if active:
            self.actions.append(action)
        else:
            self.actions.remove(action)


class RectActionSelector(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.actions = []

    def actions_click(self, instance, active, action):
        if active:
            self.actions.append(action)
        else:
            self.actions.remove(action)

class MainLayout(Widget):

    def __init__(self):        
        self.prev_a = ''
        self.prev_b = ''
        
        self.calc_selector = CalcActionSelector(cols=2)
        self.rect_selector = RectActionSelector(cols=2)
        
        self.kind = 'calc'

        super().__init__()

        self.ids.controlbox.add_widget(self.calc_selector)


    def validate_input(self):
        a = self.ids.a.text
        b = self.ids.b.text

        if a == '' or (a == '-' and self.kind != 'rect'):
            self.prev_a = self.ids.a.text
        else:
            try:
                if float(a) > 0 or self.kind != 'rect':
                    self.prev_a = self.ids.a.text
                else:
                    self.ids.a.text = self.prev_a
            except:
                self.ids.a.text = self.prev_a
    
        if b == '' or (b == '-' and self.kind != 'rect'):
            self.prev_b = self.ids.b.text
        else:
            try:
                if float(b) > 0 or self.kind != 'rect':
                    self.prev_b = self.ids.b.text
                else:
                    self.ids.b.text = self.prev_b
            except:
                self.ids.b.text = self.prev_b

    def can_calculate(self):
        a = self.ids.a.text
        b = self.ids.b.text

        try:
            if (float(b) > 0 and float(a) > 0) or self.kind != 'rect':
                return True
            else:
                return False
        except:
            return False
    
    def kind_click(self, instance, active, kind):
        if not active:
            return
        
        self.kind = kind
    
        self.ids.controlbox.clear_widgets()

        if self.kind == 'rect':
            self.ids.controlbox.add_widget(self.rect_selector)

            self.ids.a.text = self.ids.a.text.replace('-', '')
            self.ids.b.text = self.ids.b.text.replace('-', '')

        elif self.kind == 'calc':
            self.ids.controlbox.add_widget(self.calc_selector)

    def calculate(self):
        ok = self.can_calculate()

        if ok:
            a = float(self.ids.a.text)
            b = float(self.ids.b.text)

            ans = ''
            
            if self.kind == 'calc':
                for action in self.calc_selector.actions:
                    if action == 'sum':
                        ans += '\nSum: %.2f' % (a + b)
                    elif action == 'sub':
                        ans += '\nSub: %.2f' % (a - b)
                    elif action == 'mul':
                        ans += '\nMul: %.2f' % (a * b)
                    elif action == 'div':
                        ans += '\nDiv: %.2f' % (a / b)
            elif self.kind == 'rect':
                for action in self.rect_selector.actions:
                    if action == 'per':
                        ans += '\nPer: %.2f' % (2 * a + 2 * b)
                    elif action == 'sqr':
                        ans += '\nSqr: %.2f' % (a * b)

            self.ids.answer.color = '#ffffff'
            self.ids.answer.text = f'Answers:\n{ans}'

        else:
            self.ids.answer.color = '#ff0000'
            self.ids.answer.text = 'Invalid input'

    def clear(self):
        self.ids.a.text = ''
        self.ids.b.text = ''

        self.ids.answer.text = ''
        
    def swap(self):
        a = self.ids.a.text
        b = self.ids.b.text

        self.clear()

        self.ids.a.text = b
        self.ids.b.text = a


class CalcApp(App):

    def build(self):
        return MainLayout()


if __name__ == '__main__':
    CalcApp().run()
