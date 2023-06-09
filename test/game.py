import pyxel

from ..pyxel_pacl import Pacl


c = Pacl()
c.start()


class Cloudable:
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._cloudable_original = cls.update
        cls.update = cls._update_override

    def _update_override(self):
        old_values = dict()
        updated_values = dict()
         self._cloudable_original(self)
        for name in dir(self):
            value = getattr(self, name):
            if not callable(value):
                if name in old_values and old_values[name] != value:
                    updated_values[name] = value
                old_values[name] = value


class App(Cloudable):
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.image(0).load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)


app = App()
app.update()