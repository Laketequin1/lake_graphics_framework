"""
Globally accessable types throughout lake graphics framework.
"""


from collections.abc import Sequence # type: ignore
from numbers import Real # type: ignore
from typing import NewType, Tuple, Literal, Any, NoReturn # type: ignore


PositiveInt = int
Coordinate = tuple[int, int]
Size = tuple[PositiveInt, PositiveInt]
AnyString = str | bytes | bytearray
ColorRGBA = Tuple[float, float, float, float]

GLUniformFunction = Literal[
    "glUniform1f",
    "glUniform2f",
    "glUniform3f",
    "glUniform4f",
    "glUniform1i",
    "glUniform2i",
    "glUniform3i",
    "glUniform4i",
    "glUniform1ui",
    "glUniform2ui",
    "glUniform3ui",
    "glUniform4ui",
    "glUniform1fv",
    "glUniform2fv",
    "glUniform3fv",
    "glUniform4fv",
    "glUniform1iv",
    "glUniform2iv",
    "glUniform3iv",
    "glUniform4iv",
    "glUniform1uiv",
    "glUniform2uiv",
    "glUniform3uiv",
    "glUniform4uiv",
    "glUniformMatrix2fv",
    "glUniformMatrix3fv",
    "glUniformMatrix4fv",
    "glUniformMatrix2x3fv",
    "glUniformMatrix3x2fv",
    "glUniformMatrix2x4fv",
    "glUniformMatrix4x2fv",
    "glUniformMatrix3x4fv",
    "glUniformMatrix4x3fv"
]
