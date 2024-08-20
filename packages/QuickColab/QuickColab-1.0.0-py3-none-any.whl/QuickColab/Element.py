import ipywidgets as widgets
from IPython.display import display

class Element:
    display_list = []

    def __init__(self):
        pass

    @classmethod
    def update(cls):
        if cls.display_list:
            display(*cls.display_list)
    @classmethod
    def clear(cls):
        cls.display_list = []

class Button(Element):
    def __init__(self, description: str):
        super().__init__()
        self.button = widgets.Button(description=description)
        if self.button not in self.__class__.display_list:
            self.__class__.display_list.append(self.button)

    def function(self, func):
        self.button.on_click(func)

class TextInput(Element):
    def __init__(self, placeholder: str = '', description: str = ''):
        super().__init__()
        self.text_input = widgets.Text(placeholder=placeholder, description=description)
        self.__class__.display_list.append(self.text_input)

    def __call__(self):
        return self.text_input.value

    def on_change(self, func):
        self.text_input.observe(lambda change: func(change.new), names='value')

class Dropdown(Element):
    def __init__(self, options: list, description: str = ''):
        super().__init__()
        self.dropdown = widgets.Dropdown(options=options, description=description)
        self.__class__.display_list.append(self.dropdown)

    def __call__(self):
        return self.dropdown.value

    def on_change(self, func):
        self.dropdown.observe(lambda change: func(change.new), names='value')

class Checkbox(Element):
    def __init__(self, description: str, value: bool = False):
        super().__init__()
        self.checkbox = widgets.Checkbox(description=description, value=value)
        self.__class__.display_list.append(self.checkbox)

    def __call__(self):
        return self.checkbox.value

    def on_change(self, func):
        self.checkbox.observe(lambda change: func(change.new), names='value')

class Slider(Element):
    def __init__(self, min: int, max: int, step: int = 1, description: str = ''):
        super().__init__()
        self.slider = widgets.IntSlider(min=min, max=max, step=step, description=description)
        self.__class__.display_list.append(self.slider)

    def __call__(self):
        return self.slider.value

    def on_change(self, func):
        self.slider.observe(lambda change: func(change.new), names='value')

class Label(Element):
    def __init__(self, value: str):
        super().__init__()
        self.label = widgets.Label(value=value)
        self.__class__.display_list.append(self.label)

    def __call__(self):
        return self.label.value

    def set_value(self, value: str):
        self.label.value = value

    def __setitem__(self, key, value: str):
        self.set_value(value)
class TextArea(Element):
    def __init__(self, placeholder: str = '', description: str = '', rows: int = 3):
        super().__init__()
        self.textarea = widgets.Textarea(placeholder=placeholder, description=description, rows=rows)
        self.__class__.display_list.append(self.textarea)

    def __call__(self):
        return self.textarea.value

    def on_change(self, func):
        self.textarea.observe(lambda change: func(change.new), names='value')

class RadioButtons(Element):
    def __init__(self, options: list, description: str = ''):
        super().__init__()
        self.radio = widgets.RadioButtons(options=options, description=description)
        self.__class__.display_list.append(self.radio)

    def __call__(self):
        return self.radio.value

    def on_change(self, func):
        self.radio.observe(lambda change: func(change.new), names='value')

class FloatSlider(Element):
    def __init__(self, min: float, max: float, step: float = 0.1, description: str = ''):
        super().__init__()
        self.slider = widgets.FloatSlider(min=min, max=max, step=step, description=description)
        self.__class__.display_list.append(self.slider)

    def __call__(self):
        return self.slider.value

    def on_change(self, func):
        self.slider.observe(lambda change: func(change.new), names='value')

class DatePicker(Element):
    def __init__(self, description: str = ''):
        super().__init__()
        self.date_picker = widgets.DatePicker(description=description)
        self.__class__.display_list.append(self.date_picker)

    def __call__(self):
        return self.date_picker.value

    def on_change(self, func):
        self.date_picker.observe(lambda change: func(change.new), names='value')

class FileUpload(Element):
    def __init__(self, accept: str = '', multiple: bool = False):
        super().__init__()
        self.upload = widgets.FileUpload(accept=accept, multiple=multiple)
        self.__class__.display_list.append(self.upload)

    def __call__(self):
        return self.upload.value

    def on_change(self, func):
        self.upload.observe(lambda change: func(change.new), names='value')

class ToggleButtons(Element):
    def __init__(self, options: list, description: str = ''):
        super().__init__()
        self.toggle = widgets.ToggleButtons(options=options, description=description)
        self.__class__.display_list.append(self.toggle)

    def __call__(self):
        return self.toggle.value

    def on_change(self, func):
        self.toggle.observe(lambda change: func(change.new), names='value')

class HTML(Element):
    def __init__(self, value: str = ''):
        super().__init__()
        self.html = widgets.HTML(value=value)
        self.__class__.display_list.append(self.html)

    def __call__(self):
        return self.html.value

    def set_value(self, value: str):
        self.html.value = value

    def __setitem__(self, key, value: str):
        self.set_value(value)

class Output(Element):
    def __init__(self):
        super().__init__()
        self.output = widgets.Output()
        self.__class__.display_list.append(self.output)

    def __call__(self):
        return self.output

    def clear_output(self):
        self.output.clear_output()

    def append_stdout(self, text: str):
        self.output.append_stdout(text)

    def __enter__(self):
        return self.output.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.output.__exit__(exc_type, exc_val, exc_tb)