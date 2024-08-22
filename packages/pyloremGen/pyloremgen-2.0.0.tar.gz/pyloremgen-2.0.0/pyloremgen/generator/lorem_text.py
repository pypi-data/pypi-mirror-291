import random

from pyloremgen.utilities.file_helper import get_data_json


class LoremIpsumError(Exception):
    """
    Custom exception class for LoremIpsum errors.
    """

    def __init__(self, message):
        super().__init__(message)


class LoremIpsum:
    """
    LoremIpsum class

    This class generates lorem ipsum text.
    It provides methods for generating paragraphs, words, and a shopping list of random items.

    Methods:
        __init__():
            Initializes a new instance of the class.

        __initialize_paragraphs_words():
            Initializes the number of words in each paragraph.

        __generate_paragraph():
            Generates a random paragraph by joining a list of random words.

        paragraphs(paragraphs_numbers: int, start_with_lorem_ipsum: bool = True) -> str:
            Generates a specified number of lorem ipsum paragraphs.

        words(words_numbers: int) -> str:
            Generates a string of random words.

        shopping_list(items_count: int) -> str:
            Generates a shopping list of randomly selected items.

    Fields:
        paragraph_lorem: list
            A list to store lorem ipsum paragraphs.

        words_lorem: list
            A list to store lorem ipsum words.

        items_lorem: list
            A list to store lorem ipsum items.

        paragraphs_words: int
            The number of words in each paragraph.

        start_with_lorem_ipsum: str
            A string that represents the start of a lorem ipsum text.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        This constructor initializes the following instance variables:
        - `paragraph_lorem`: A list to store lorem ipsum paragraphs.
        - `words_lorem`: A list to store lorem ipsum words.
        - `items_lorem`: A list to store lorem ipsum items.
        - `paragraphs_words`: A variable to store the number of words in each paragraph.
        - `start_with_lorem_ipsum`: A string that represents the start of a lorem ipsum text.

        Parameters:
        None

        Returns:
        None
        """
        self.paragraph_lorem = []
        self.words_lorem = []
        self.items_lorem = []
        self.paragraphs_words = None
        self.start_with_lorem_ipsum = " ".join(get_data_json("lorem_ipsum_start"))
        self.start_with_lorem_ipsum = " ".join(get_data_json("lorem_ipsum_start"))
        self.__initialize_paragraphs_words()

    def __initialize_paragraphs_words(self):
        """
        Initializes the number of words in each paragraph.

        This function is called internally by the class to set
        the initial value of the `paragraphs_words` attribute.
        If the attribute is already set, the function does nothing.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        if self.paragraphs_words is None:
            self.paragraphs_words = random.randint(12, 20)

    def __generate_paragraph(self):
        """
        Generate a random paragraph by joining a list of random words.

        Returns:
            str: A randomly generated paragraph.

        Parameters:
            self: The instance of the class.

        Raises:
            LoremIpsumError: If an error occurs during the generation of the paragraph.
        """
        try:
            return " ".join(random.choices(get_data_json(), k=self.paragraphs_words))
        except Exception as e:
            raise LoremIpsumError(f"Error generating paragraph: {str(e)}") from e

    def paragraphs(
        self,
        paragraphs_numbers: int = 1,
        size: str = "medium",
        start_with_lorem_ipsum: bool = True,
    ) -> str:
        """
        Generate a specified number of lorem ipsum paragraphs with specified size.

        Parameters:
            paragraphs_numbers (int): The number of paragraphs to generate.
            size (str, optional): The size of the paragraphs. Can be "small", "medium", or "large". Defaults to "medium".
            start_with_lorem_ipsum (bool, optional):
            start_with_lorem_ipsum (bool, optional):
            Whether to start with a "Lorem ipsum" paragraph. Defaults to False.

        Returns:
            str: The generated paragraphs joined by newline characters.

        Raises:
            LoremIpsumError: If an error occurs during the generation of paragraphs.
        """
        try:
            paragraph_size = {"small": 3, "medium": 5, "large": 9}.get(size.lower(), 5)
            paragraphs = []

            if start_with_lorem_ipsum:
                paragraphs.append(self.start_with_lorem_ipsum)

            for _ in range(paragraphs_numbers):
                paragraph = [self.__generate_paragraph() for _ in range(paragraph_size)]
                paragraphs.append("\n".join(paragraph))

            return "\n".join(paragraphs)
        except Exception as e:
            raise LoremIpsumError(f"Error generating paragraphs: {str(e)}") from e

    def words(self, words_numbers: int) -> str:
        """
        Generate a string of random words.

        Args:
            words_numbers (int): The number of words to generate.

        Returns:
            str: A string containing the generated words separated by spaces.

        Raises:
            LoremIpsumError: If an error occurs during the generation of words.
        """
        try:
            words = " ".join(random.choices(get_data_json(), k=words_numbers))
            self.words_lorem.append(words)
            return "\n".join(self.words_lorem)
        except Exception as e:
            raise LoremIpsumError(f"Error generating words: {str(e)}") from e

    def shopping_list(self, items_count: int = None) -> str:
        """
        Generates a shopping list of randomly selected items.
        Args:
            items_count (int): The number of items to include in the shopping list.
        Returns:
            str: The shopping list as a string, with each item on a new line.
        Raises:
            LoremIpsumError: If an error occurs during the generation of the shopping list.
        """
        items_count = random.randint(5, 100) if items_count is None else items_count
        try:
            data_json = get_data_json()
            if items_count > len(data_json):
                # Repetir o data_json para alcançar o items_count
                repeated_data = (
                    data_json * (items_count // len(data_json))
                    + data_json[: items_count % len(data_json)]
                )
                items = random.choices(repeated_data, k=items_count)
            else:
                items = random.choices(data_json, k=items_count)
                self.items_lorem.append("Shopping List:")
                self.items_lorem.extend(items)
                return "\n".join(self.items_lorem)
        except Exception as e:
            raise LoremIpsumError(f"Error generating shopping list: {str(e)}") from e
