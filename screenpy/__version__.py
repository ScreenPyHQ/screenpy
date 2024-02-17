r"""
                 ____                           ____
                / ___|  ___ _ __ ___  ___ _ __ |  _ \ _   _
                \___ \ / __| '__/ _ \/ _ \ '_ \| |_) | | | |
                 ___) | (__| | |  __/  __/ | | |  __/| |_| |
                |____/ \___|_|  \___|\___|_| |_|_|    \__, |
                                                      |___/
"""

import importlib.metadata

metadata = importlib.metadata.metadata("screenpy")

__title__ = metadata["Name"]
__description__ = metadata["Summary"]
__url__ = metadata["Home-page"]
__version__ = metadata["Version"]
__author__ = metadata["Author"]
__author_email__ = metadata["Author-email"]
__license__ = metadata["License"]
__copyright__ = f"2019-2024 {__author__}"
