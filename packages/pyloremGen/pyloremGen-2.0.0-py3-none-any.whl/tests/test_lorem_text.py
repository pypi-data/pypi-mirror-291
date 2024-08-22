import unittest

from pyloremgen.generator.lorem_text import LoremIpsum


class TestLoremIpsum(unittest.TestCase):

    # Generates paragraphs of the specified size with fixed assertion
    def test_generates_paragraphs_of_specified_size_with_fixed_assertion(self):
        # Arrange
        lorem_ipsum = LoremIpsum()
        paragraphs_numbers = 2
        size = "small"
        start_with_lorem_ipsum = False

        # Act
        result = lorem_ipsum.paragraphs(paragraphs_numbers, size, start_with_lorem_ipsum)
        generated_paragraphs = result.split("\n\n\n")

        # Assert
        for paragraph in generated_paragraphs:
            self.assertEqual(len(paragraph.split("\n")), 3 * paragraphs_numbers)

        # Handles invalid size parameter gracefully

    def test_handles_invalid_size_parameter_gracefully(self):
        # Arrange
        lorem_ipsum = LoremIpsum()
        paragraphs_numbers = 2
        size = "invalid_size"
        start_with_lorem_ipsum = False

        # Act
        result = lorem_ipsum.paragraphs(paragraphs_numbers, size, start_with_lorem_ipsum)
        generated_paragraphs = result.split("\n\n")

        # Assert
        for paragraph in generated_paragraphs:
            self.assertEqual(len(paragraph.split("\n")), 10)

    def test_generates_zero_paragraphs_when_paragraphs_numbers_is_zero(self):
        # Arrange
        lorem_ipsum = LoremIpsum()
        paragraphs_numbers = 0
        size = "medium"
        start_with_lorem_ipsum = False

        # Act
        result = lorem_ipsum.paragraphs(paragraphs_numbers, size, start_with_lorem_ipsum)

        # Assert
        self.assertEqual(result, "")

    # Generates 0 words.
    def test_generate_zero_words(self):
        """
        Generate the function comment for the given function body in a markdown code block with the correct language syntax.

        :param self: The instance of the test class.
        :return: None
        """
        # Arrange
        lorem = LoremIpsum()
        words_numbers = 0

        # Act
        result = lorem.words(words_numbers)

        # Assert
        self.assertEqual(len(result.split()), words_numbers)

    # Generates 1 word.
    def test_generate_one_word(self):
        """
        Test the `words` method of the `LoremIpsum` class when generating one word.

        This test case checks if the `words` method of the `LoremIpsum` class correctly generates the specified number of words. The test first arranges the necessary variables by creating an instance of the `LoremIpsum` class and setting the `words_numbers` variable to 1. Then, the test acts by calling the `words` method with the `words_numbers` parameter. Finally, the test asserts that the length of the result, after splitting it into a list of words, is equal to the specified `words_numbers`.

        This test helps ensure that the `words` method of the `LoremIpsum` class behaves as expected when generating one word.

        :param self: The test case instance.
        """

        # Arrange
        lorem = LoremIpsum()
        words_numbers = 1

        # Act
        result = lorem.words(words_numbers)

        # Assert
        self.assertEqual(len(result.split()), words_numbers)

    def test_generate_random_words(self):
        """
        Generates a random sequence of words using the LoremIpsum class.

        Parameters:
            self (TestClass): The current instance of the test class.

        Returns:
            None
        """
        # Arrange
        lorem = LoremIpsum()
        words_numbers = 10

        # Act
        result = lorem.words(words_numbers)

        # Assert
        self.assertEqual(len(result.split()), words_numbers)

    # Generates a shopping list of randomly selected items.
    def test_generate_shopping_list(self):
        """
        Test the generate shopping list function.

        This function tests the functionality of the `shopping_list` method in the `LoremIpsum` class. It verifies that the returned shopping list has the expected number of items and starts with the correct header.

        Parameters:
            self (object): The current instance of the `TestCase` class.

        Returns:
            None
        """
        # Arrange
        lorem = LoremIpsum()
        items_count = 5

        # Act
        result = lorem.shopping_list(items_count)

        # Assert
        self.assertEqual(len(result.split("\n")), items_count + 1)
        self.assertTrue(result.startswith("Shopping List:"))
