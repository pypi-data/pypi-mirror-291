import random
import math
from ail_typo_squatting import runAll
from leet import leet

class Variation:
    def __init__(self):
        pass

    def typosquatting(self, domain: str, format: str = "yara") -> list:
        """
        Generates typo-squatting domain variations for a given domain.
        
        Args:
            domain (str): The domain name to generate variations for.
            format (str): The output format (e.g., 'yara'). Default is 'yara'.

        Returns:
            list: A list of generated domain variations.
        """
        result_list = []
        path_output = "."
        result_list = runAll(
            domain=domain, 
            limit=math.inf, 
            formatoutput=format, 
            pathOutput=path_output, 
            verbose=False, 
            givevariations=False,
            keeporiginal=False
        )
        return result_list

    def generate_leet(self, text: str) -> list:
        """
        Applies leet transformations to a given text.

        Args:
            text (str): The text to transform.

        Returns:
            list: A list of leet-transformed variations of the text.
        """
        return leet(text)

    def generate_variations(self, text: str) -> list:
        """
        Generates variations of a given text by duplicating characters,
        inserting underscores, and altering capitalization.

        Args:
            text (str): The text to generate variations for.

        Returns:
            list: A list of generated text variations.
        """
        variations = []
        
        for i in range(len(text)):
            variations.append(text[:i] + text[i] + text[i:] + str(random.randint(1, 9)))

        for i in range(1, len(text)):
            variations.append(text[:i] + "_" + text[i:])

        variations.append(text.capitalize())
        variations.append(text.upper())

        return variations
