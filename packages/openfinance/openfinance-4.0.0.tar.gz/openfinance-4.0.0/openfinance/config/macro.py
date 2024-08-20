from openfinance.utils.log import get_logger

EXE_MODE = 0

MLOG = get_logger(
    filename="main.log",
    verbosity=EXE_MODE,
    name="main"
)

ChatLOG = get_logger(
    filename="chat.log",
    verbosity=EXE_MODE,
    name="chat"
)

HOMELOG = get_logger(
    filename="home.log",
    verbosity=EXE_MODE,
    name="home"
)