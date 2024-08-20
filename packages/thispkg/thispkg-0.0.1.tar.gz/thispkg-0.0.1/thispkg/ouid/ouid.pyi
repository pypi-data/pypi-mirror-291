def ouid(class_name: str) -> str:
    """
    Generate a unique ID for a given class name.

    Args:
        class_name (str): The name of the Python class.

    Returns:
        str: A unique ID string in the format '__class__.__name__.xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx',
             where 'x' is a hexadecimal digit and 'y' is one of '8', '9', 'a', or 'b'.
    """
    ...
