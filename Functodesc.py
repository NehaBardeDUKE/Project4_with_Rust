def function_description_to_index(description, function_descriptions):
    """
    Maps a function description to its corresponding index in the list of function descriptions.

    Parameters:
    - description (str): The function description to map.
    - function_descriptions (list of str): List of all function descriptions in the same order as db_description_embeddings.

    Returns:
    - int: The index of the function description in the list.

    Raises:
    - ValueError: If the description is not found in the function_descriptions list.
    """
    try:
        return function_descriptions.index(description)
    except ValueError:
        raise ValueError(f"Function description '{description}' not found in the provided list.")
