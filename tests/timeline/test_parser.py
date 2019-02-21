from unittest import TestCase
from lark import Lark


class TestLarkParser(TestCase):

    def test_parse_tree_creation(self):
        timeline_grammar = """
            start: instruction+
            instruction: "- " time            
            time: DIGIT ~ 2 ":" DIGIT ~ 2
            DIGIT: "0".."9" 
            %import common.NEWLINE
            %import common.WS
            %ignore WS
        """

        sample_grammar = """
            start: instruction+
            instruction: MOVEMENT NUMBER            -> movement
                       | "c" COLOR [COLOR]          -> change_color
                       | "fill" code_block          -> fill
                       | "repeat" NUMBER code_block -> repeat
            code_block: "{" instruction+ "}"
            MOVEMENT: "f"|"b"|"l"|"r"
            COLOR: LETTER+
            %import common.LETTER
            %import common.INT -> NUMBER
            %import common.WS
        """

        timeline_example = """
            -  16:00
            -  18:00
        """
        parser = Lark(timeline_grammar)
        lark_parse_tree = parser.parse(timeline_example)

        for entry in lark_parse_tree.children:
            print(entry)

        self.assertTrue(len(lark_parse_tree.children) == 2)