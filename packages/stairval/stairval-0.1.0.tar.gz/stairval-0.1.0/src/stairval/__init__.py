"""
Stairval is a framework for validating hierarchical data structures.
"""


from ._auditor import Auditor, Notepad, ITEM, Issue, Level

__version__ = "0.1.0"

__all__ = [
    "Auditor", "Notepad", "Issue", "Level", "ITEM",
]
