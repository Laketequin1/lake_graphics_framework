"""
Validates variable types for the project lake_graphics_framework.

Used to validate user parameters being passed into the
lake_graphics_framework functions.
"""


from .._src._global_type_hinting import (
    Any,
    NoReturn,
    Real,
    Sequence,
    PositiveInt,
    Coordinate,
    Size,
    AnyString,
    ColorRGBA
)


def validate_types(
        expected_types: list[tuple[str, Any, type]]
    ) -> None | NoReturn:
    """
    Validate variables against their expected types. Raises a TypeError
    or ValueError if validation fails.

    Args:
        expected_types (list[tuple[str, Any, type]]): A list of tuples
            containing the validation rules. Each tuple must be
            formatted as (variable_name, variable_value, expected_type).

    Raises:
        TypeError: If a variable does not conform to its expected type.
        ValueError: If a variable does not meet value constraints.
    """
    for expected_type in expected_types:
        validate_type(*expected_type)

def validate_type(
        name: str,
        var: Any,
        expected_type: type
    ) -> None | NoReturn:
    """
    Validate variables against their expected types. Raises a TypeError
    or ValueError if validation fails.

    Parameters:
        name (str): The name of the variable being validated.
        var (Any): The variable to be validated.
        expected_type (type): The expected type for the variable.

    Raises:
        TypeError: If all components don't match types.
        ValueError: If the value doesn't conform to the correct range.
    """
    if expected_type is PositiveInt:
        _validate_positiveint(name, var)
        return # Validation success

    if expected_type is Coordinate:
        _validate_coordinate(name, var)
        return # Validation success

    if expected_type is Size:
        _validate_size(name, var)
        return # Validation success

    if expected_type is ColorRGBA:
        _validate_color_rgba(name, var)
        return # Validation success

    if not isinstance(var, expected_type):
        raise TypeError(
            f"Invalid type for {name}. "
            f"Expected {expected_type}, got {type(var)}."
            )
    return # Validation success

def _validate_positiveint(name: str, var: Any) -> None | NoReturn:
    """
    [Private]
    Validates that the variable is a positive integer.
    The function will raise an error if valitadion statement is invalid,
    otherwise continues.

    Parameters:
        name (str): The name of the variable being validated.
        var (Any): The variable to be validated.

    Raises:
        TypeError: If not an int.
        ValueError: If the number is non-negative.
    """
    if not isinstance(var, int):
        raise TypeError(
            f"Invalid type for {name}. "
            f"Expected {int}, got {type(var)}."
        )

    if var < 0:
        raise ValueError(
            f"Invalid value for {name}. "
            f"PositiveInt numbers must be non-negative."
        )

def _validate_coordinate(name: str, var: Any) -> None | NoReturn:
    """
    [Private]
    Validates that the variable is a sequence of two numbers
    representing coordinates. The function will raise an error if
    valitadion statement is invalid, otherwise continues.

    Parameters:
        name (str): The name of the variable being validated.
        var (Any): The variable to be validated, expected to be a
            sequence of two numbers.
    
    Raises:
        TypeError: If not a sequence, wrong sequence size, or doesn't
            contain numbers.
    """
    if not isinstance(var, Sequence) or isinstance(var, AnyString):
        raise TypeError(
            f"Invalid type for Coordinate '{name}'. "
            f"Expected {Sequence}, got {type(var)}."
        )

    if len(var) != 2: # type: ignore
        raise TypeError(
            f"Invalid length for Coordinate '{name}'. "
            f"Coordinate must be two numbers."
        )

    for i in [0, 1]:
        if not isinstance(var[i], Real):
            raise TypeError(
                f"Invalid type for Coordinate[{i}] '{name}'. "
                f"Expected {Real}, got {type(var[i])}." # type: ignore
            )

def _validate_size(name: str, var: Any) -> None | NoReturn:
    """
    [Private]
    Validates that the variable is a sequence of two positive numbers
    representing size. The function will raise an error if valitadion
    statement is invalid, otherwise continues.

    Parameters:
        name (str): The name of the variable being validated.
        var (Any): The variable to be validated, expected to be a
            sequence of two real numbers.

    Raises:
        TypeError: If not a sequence, wrong sequence size, or doesn't
            contain numbers.
        ValueError: If the number contents are non-negative.
    """
    if not isinstance(var, Sequence) or isinstance(var, AnyString):
        raise TypeError(
            f"Invalid type for Size '{name}'. "
            f"Expected {Sequence}, got {type(var)}."
        )

    if len(var) != 2: # type: ignore
        raise TypeError(
            f"Invalid length for Size '{name}'. "
            f"Size must be two numbers."
        )

    for i in [0, 1]:
        if not isinstance(var[i], Real):
            raise TypeError(
                f"Invalid type for Size[{i}] '{name}'. "
                f"Expected {Real}, got {type(var[i])}." # type: ignore
            )

    for i in [0, 1]:
        if var[i] < 0:
            raise ValueError(
                f"Invalid value for Size[{i}] '{name}'. "
                f"All size numbers must be non-negative, got {var}."
            )

def _validate_color_rgba(name: str, var: Any) -> None | NoReturn:
    """
    [Private]
    Validates that the variable is a sequence of 4 positive
    floats ranging from 0 to 1 representing nomalised rgba:
    Red, Green, Blue, Alpha. The function will raise an error if
    valitadion statement is invalid, otherwise continues.

    Parameters:
        name (str): The name of the variable being validated.
        var (Any): The variable to be validated, expected to be a
            sequence of 4 real positive floats.

    Raises:
        TypeError: If not a sequence, wrong sequence size, or doesn't
            contain numbers.
        ValueError: If the number contents don't range between 0 to 1.
    """
    if not isinstance(var, Sequence) or isinstance(var, AnyString):
        raise TypeError(
            f"Invalid type for the Color '{name}'. "
            f"Expected {Sequence}, got {type(var)}."
        )

    if len(var) != 4: # type: ignore
        raise TypeError(
            f"Invalid length for the Color '{name}'. "
            f"Color must be contain four channels: Red, Green, Blue, Alpha."
        )

    for i in range(4):
        if not isinstance(var[i], Real):
            raise TypeError(
                f"Invalid type for the Color[{i}] '{name}'. "
                f"Expected {Real}, got {type(var[i])}." # type: ignore
            )

    for i in range(4):
        if var[i] < 0 or var[i] > 1:
            raise ValueError(
                f"Invalid value for the Color[{i}] '{name}'. "
                f"Color numbers must be between 0 and 1 inclusive, "
                f"but the value was {var[i]}."
            )
