from pynd.dobject.dobject import Dobject


# DISCLAIMER
# Race is not well defined in biology whereas species is.
# In the context of DnD race is more appropriate, unless someone
# wants to classify everything according to modern taxonomy;
# I'll be happy to make it a part of the code,
# until then..
# Have fun :)


class Race(Dobject):
    CONFIG = {

    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
