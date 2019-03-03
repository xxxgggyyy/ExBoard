from business import ExInterFace
from .MainPlugin import MainPlugin
mp = MainPlugin("DxfPlugin")
ExInterFace.register(mp)