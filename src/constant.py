from types import SimpleNamespace

from utils.keyboards import create_keyboards

keys = SimpleNamespace(
    random_conect=':busts_in_silhouette: Random Conect',
    settings=':wrench: Settings'
)

keyboards = SimpleNamespace(
    main=create_keyboards(keys.random_conect, keys.settings)
)
