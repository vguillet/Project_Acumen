import tkinter as tk
import GUI_Restructured
class TKinterTestCase(unittest.TestCase):
    """These methods are going to be the same for every GUI test,
    so refactored them into a separate class
    """
    def setUp(self):
        self.root=tk.Tk()
        self.pump_events()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pump_events()

    def pump_events(self):
        while self.root.dooneevent(_tk.ALL_EVENTS | _tk.DONT_WAIT):
            pass

class TestRenameTopic(TKinterTestCase):
    def test_enter(self):
        v = renameTopic(self.root,value=u"йцу")  # the class implementing the dialog;
                                                  # not included in the example
        self.pump_events()
        v.e.focus_set()
        v.e.insert(tk.END,u'кен')
        v.e.event_generate('<Return>')
        self.pump_events()

        self.assertRaises(tk.TclError, lambda: v.top.winfo_viewable())
        self.assertEqual(v.value,u'йцукен')

if __name__ == '__main__':
    import unittest
    unittest.main()
