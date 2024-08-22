import abc
import enum
import io
import os
import sys
import typing


class Level(enum.Enum):
    """
    An enum to represent severity of the :class:`DataSanityIssue`.
    """

    WARN = enum.auto()
    """
    Warning is an issue when something not entirely right. However, unlike :class:`Level.ERROR`,
    the analysis should complete albeit with sub-optimal results 😧.
    """

    ERROR = enum.auto()
    """
    Error is a serious issue in the input data and the downstream analysis may not complete or the analysis results
    may be malarkey 😱.
    """

    def __str__(self):
        return self.name


class Issue:
    """
    `Issue` summarizes an issue found in the input data.

    The issue has a :attr:`level`, a :attr:`message` with human-friendly description,
    and an optional :attr:`solution` for addressing the issue.
    """

    def __init__(
        self,
        level: Level,
        message: str,
        solution: typing.Optional[str] = None,
    ):
        self._level = level
        self._message = message
        self._solution = solution

    @property
    def level(self) -> Level:
        return self._level

    @property
    def message(self) -> str:
        return self._message

    @property
    def solution(self) -> typing.Optional[str]:
        return self._solution

    def __str__(self):
        return f"Issue(level={self._level}, message={self._message}, solution={self._solution})"

    def __repr__(self):
        return str(self)


class Notepad(metaclass=abc.ABCMeta):
    """
    Record issues encountered during parsing/validation of a hierarchical data structure.

    The issues can be organized in sections. `Notepad` keeps track of issues in one section
    and the subsections can be created by calling :func:`add_subsection`.
    The function returns an instance responsible for issues of a subsection.

    A collection of the issues from the current section are available via :attr:`issues` property
    and the convenience functions provide iterators over error and warnings.
    """

    def __init__(
        self,
        label: str,
        level: int,
    ):
        self._label = label
        self._level = level
        self._issues: typing.MutableSequence[Issue] = []

    @abc.abstractmethod
    def add_subsection(self, label: str) -> "Notepad":
        """
        Add a labeled subsection.

        Returns:
            Notepad: a notepad for recording issues within the subsection.
        """
        pass

    @abc.abstractmethod
    def iter_sections(self) -> typing.Iterator["Notepad"]:
        """
        Iterate over nodes in the depth-first fashion.

        Returns: a depth-first iterator over :class:`Notepad` nodes.
        """
        pass

    @property
    def label(self) -> str:
        """
        Get the section label.
        """
        return self._label

    @property
    def level(self) -> int:
        """
        Get the level of the notepad node (distance from the top-level hierarchy node).
        """
        return self._level

    @property
    def issues(self) -> typing.Sequence[Issue]:
        """
        Get an iterable with the issues of the current section.
        """
        return self._issues

    def add_issue(
        self, level: Level, message: str, solution: typing.Optional[str] = None
    ):
        """
        Add an issue with certain `level`, `message`, and an optional `solution`.
        """
        self._issues.append(Issue(level, message, solution))

    def add_error(self, message: str, solution: typing.Optional[str] = None):
        """
        A convenience function for adding an *error* with a `message` and an optional `solution`.
        """
        self.add_issue(Level.ERROR, message, solution)

    def errors(self) -> typing.Iterator[Issue]:
        """
        Iterate over the errors of the current section.
        """
        return filter(lambda dsi: dsi.level == Level.ERROR, self.issues)

    def error_count(self) -> int:
        """
        Returns:
            int: count of errors found in this section.
        """
        return sum(1 for _ in self.errors())

    def has_errors(self, include_subsections: bool = False) -> bool:
        """
        Returns:
            bool: `True` if one or more errors were found in the current section or its subsections.
        """
        if include_subsections:
            for node in self.iter_sections():
                for _ in node.errors():
                    return True
        else:
            for _ in self.errors():
                return True

        return False

    def add_warning(self, message: str, solution: typing.Optional[str] = None):
        """
        A convenience function for adding a *warning* with a `message` and an optional `solution`.
        """
        self.add_issue(Level.WARN, message, solution)

    def warnings(self) -> typing.Iterator[Issue]:
        """
        Iterate over the warnings of the current section.
        """
        return filter(lambda dsi: dsi.level == Level.WARN, self.issues)

    def has_warnings(self, include_subsections: bool = False) -> bool:
        """
        Returns:
            bool: `True` if one or more warnings were found in the current section or its subsections.
        """
        if include_subsections:
            for node in self.iter_sections():
                for _ in node.warnings():
                    return True
        else:
            for _ in self.warnings():
                return True

        return False

    def warning_count(self) -> int:
        """
        Returns:
            int: count of warnings found in this section.
        """
        return sum(1 for _ in self.warnings())

    def has_errors_or_warnings(self, include_subsections: bool = False) -> bool:
        """
        Returns:
            bool: `True` if one or more errors or warnings were found in the current section or its subsections.
        """
        if include_subsections:
            for node in self.iter_sections():
                for _ in node.warnings():
                    return True
                for _ in node.errors():
                    return True
        else:
            for _ in self.warnings():
                return True
            for _ in self.errors():
                return True

        return False

    def visit(
        self,
        visitor: typing.Callable[
            [
                "Notepad",
            ],
            None,
        ],
    ):
        """
        Performs a depth-first search on the notepad nodes and calls `visitor` with all nodes.
        Args:
            visitor: a callable that takes the current notepad node as the only argument.
        """
        for node in self.iter_sections():
            visitor(node)

    def summarize(
        self,
        file: io.TextIOBase = sys.stdout,
        indent: int = 2,
    ):
        assert isinstance(indent, int) and indent >= 0

        n_errors = sum(node.error_count() for node in self.iter_sections())
        n_warnings = sum(node.warning_count() for node in self.iter_sections())
        if n_errors > 0 or n_warnings > 0:
            file.write("Showing errors and warnings")
            file.write(os.linesep)

            for node in self.iter_sections():
                if node.level != 0:
                    file.write(os.linesep)
                if node.has_errors_or_warnings(include_subsections=True):
                    # We must report the node label even if there are no issues with the node.
                    l_pad = " " * ((node.level + 1) * indent)
                    file.write(l_pad + node.label)
                    file.write(os.linesep)

                    if node.has_errors():
                        file.write(l_pad + "errors:")
                        file.write(os.linesep)
                        for error in node.errors():
                            file.write(
                                l_pad
                                + "- "
                                + error.message
                                + (f"· {error.solution}" if error.solution else "")
                            )
                            file.write(os.linesep)
                    if node.has_warnings():
                        file.write(l_pad + "warnings:")
                        file.write(os.linesep)
                        for warning in node.warnings():
                            file.write(
                                l_pad
                                + "- "
                                + warning.message
                                + (f"· {warning.solution}" if warning.solution else "")
                            )
                            file.write(os.linesep)
        else:
            file.write("No errors or warnings were found")


class NotepadTree(Notepad):
    """
    `NotepadTree` implements :class:`Notepad` using a tree where each tree node corresponds to a (sub)section. The node
    can have `0..n` children.

    Each node has a :attr:`label`, a collection of issues, and children with subsections. For convenience, the node
    has :attr:`level` to correspond to the depth of the node within the tree (the level of the root node is `0`).

    The nodes can be accessed via :attr:`children` property or through convenience methods for tree traversal,
    either using the visitor pattern (:func:`visit`) or by iterating over the nodes via :func:`iterate_nodes`.
    In both cases, the traversal is done in the depth-first fashion.
    """

    def __init__(
        self,
        label: str,
        level: int,
    ):
        super().__init__(label, level)
        self._children = []

    def add_subsection(self, identifier: str) -> "NotepadTree":
        sub = NotepadTree(identifier, self._level + 1)
        self._children.append(sub)
        return sub

    def iter_sections(self) -> typing.Iterator["Notepad"]:
        """
        Iterate over nodes in the depth-first fashion.

        Returns: a depth-first node iterator.
        """
        stack = [
            self,
        ]
        while stack:
            node = stack.pop()
            stack.extend(reversed(node._children))
            yield node

    def __str__(self):
        return (
            "NotepadTree("
            f"label={self._label}, "
            f"level={self._level}, "
            f"children={[ch.label for ch in self._children]}"
            ")"
        )


ITEM = typing.TypeVar("ITEM")
"""
The input for the :class:`Auditor`.
"""


class Auditor(typing.Generic[ITEM], metaclass=abc.ABCMeta):
    """
    `Auditor` checks the inputs for sanity issues and relates the issues with sanitized inputs
    as :class:`SanitationResults`.

    The auditor may sanitize the input as a matter of discretion and returns the input as `OUT`.
    """

    @staticmethod
    def prepare_notepad(label: str) -> Notepad:
        """
        Prepare a :class:`Notepad` for recording issues and errors.

        Args:
            label: a `str` with the top-level section label.

        Returns:
            NotepadTree: an instance of :class:`NotepadTree`.
        """
        return NotepadTree(label, level=0)

    @abc.abstractmethod
    def audit(
        self,
        item: ITEM,
        notepad: Notepad,
    ):
        """
        Audit the `item` and record any issues into the `notepad`.
        """
        pass
