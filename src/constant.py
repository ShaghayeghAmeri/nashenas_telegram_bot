from types import SimpleNamespace

from utils.keyboards import create_keyboards

keys = SimpleNamespace(
    random_conect=':busts_in_silhouette: Random Conect',
    settings=':wrench: Settings', 
    exit=':cross_mark: Exit'
)

keyboards = SimpleNamespace(
    main=create_keyboards(keys.random_conect, keys.settings), 
    exit=create_keyboards(keys.exit)
)

states = SimpleNamespace(
    random_connect='RANDOM_CONNECT',
    main='MAIN',
    connected='CONNECTED'
)

