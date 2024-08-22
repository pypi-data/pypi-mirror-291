from importlib import metadata

from nautobot.extras.plugins import PluginConfig

__version__ = metadata.version(__name__)


class DeepCopyConfig(PluginConfig):
    name = "nautobot_deepcopy"
    verbose_name = "Deep Copy"
    description = "A plugin for copying devices and their components"
    version = __version__
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = "nautobot_deepcopy"
    required_settings = []
    default_settings = {}
    middleware = []


config = DeepCopyConfig
