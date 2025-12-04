from manager.models.config import Config

def fuso(cr):
    return Config.get_fuso(cr)