import unittest


from anchorscad_lib.utils.colours import Colour 
from anchorscad_lib.test_tools import iterable_assert


class ColourTest(unittest.TestCase):
    
    def test_colour_name(self):
        iterable_assert(
            self.assertAlmostEqual, 
            Colour('yellowgreen').value, 
            (154/255, 205/255, 50/255, 1))

    def test_colour_name_with_alpha(self):
        '''Test that we can create a colour by name with an alpha value'''
        c = Colour('red', 0.5)
        self.assertEqual(c.value, (1, 0, 0, 0.5))
        c = Colour('red', a=0.5)
        self.assertEqual(c.value, (1, 0, 0, 0.5))
        
    def test_malformed_name(self):
        
        self.assertRaises(AssertionError, Colour, 'red', 1, 1)
        self.assertRaises(AssertionError, Colour, 'red', 1, a=0.5)
        self.assertRaises(AssertionError, Colour, 'not a colour')
    
    def test_colour_rgb(self):
        '''Test that we can create a colour by name'''
        c = Colour((1, 0, 0))
        self.assertEqual(c.value, (1, 0, 0, 1))
        
    def test_colour_rgba(self):
        '''Test that we can create a colour by name'''
        c = Colour((1, 0, 0))
        self.assertEqual(c.value, (1, 0, 0, 1))
        
        c = Colour((1, 0, 0, 0.5))
        self.assertEqual(c.value, (1, 0, 0, 0.5))
        
        c = Colour((1, 0, 0), 0.5)
        self.assertEqual(c.value, (1, 0, 0, 0.5))
        
        c = Colour((1, 0, 0), a=0.5)
        self.assertEqual(c.value, (1, 0, 0, 0.5))
        
    def test_colour_rgb_malformed(self):
        '''Test that we can create a colour by name'''
        self.assertRaises(AssertionError, Colour, (1, 0, 0, 0.5), a=1)
        self.assertRaises(AssertionError, Colour, (1, 0, 0), 0.5, 0.5)
        self.assertRaises(AssertionError, Colour, (1, 0, 0), b=0.5)
        self.assertRaises(AssertionError, Colour, ('1', 0, 0))
        self.assertRaises(AssertionError, Colour, (1.1, 0, 0, 0.5))
        
    def test_colour_with_colour(self):
        '''Test that we can create a colour by name'''
        c = Colour(Colour('red'))
        self.assertEqual(c.value, (1, 0, 0, 1))
        
    def test_colour_with_colour_malformed(self):
        '''Test that we can create a colour by name'''
        c = Colour('red')
        self.assertRaises(AssertionError, Colour, c, 0.5)
        self.assertRaises(AssertionError, Colour, c, a=0.5)
        
    def test_colour_method(self):
        c = Colour('red')
        self.assertEqual(c.alpha(0.1).value, (1, 0, 0, 0.1))
        self.assertEqual(c.red(0.1).value, (0.1, 0, 0, 1))
        self.assertEqual(c.green(0.1).value, (1, 0.1, 0, 1))
        self.assertEqual(c.blue(0.1).value, (1, 0, 0.1, 1))
        
        self.assertEqual(c.red(0.1).green(0.2).blue(0.3).alpha(0.4).value,
                         (0.1, 0.2, 0.3, 0.4))
        self.assertEqual(c.blend(Colour('blue'), 0.75).value, (0.25, 0, 0.75, 1))
        
    def test_equality(self):
        c1 = Colour('red')
        c2 = Colour('red')
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, Colour('blue'))
        self.assertNotEqual(c1, Colour('red', 0.5))
        
    def test_hex_colour(self):
        c1 = Colour('#fff')
        self.assertEqual(c1.value, (1, 1, 1, 1))
        c1 = Colour('#fff7')
        self.assertEqual(c1.value, (1, 1, 1, 0x77/0xff))
        c1 = Colour('#f0f0f0')
        self.assertEqual(c1.value, (0xf0/0xff, 0xf0/0xff, 0xf0/0xff, 1))
        c1 = Colour('#f0f0f0f0')
        self.assertEqual(c1.value, (0xf0/0xff, 0xf0/0xff, 0xf0/0xff, 0xf0/0xff))
        
        self.assertEqual(c1.to_hex(), "#f0f0f0f0")
    
    def test_hex_colour_malformed(self):
        self.assertRaises(AssertionError, Colour, "#errerr")
        self.assertRaises(AssertionError, Colour, "#err")
        self.assertRaises(AssertionError, Colour, "#errerrff")
        self.assertRaises(AssertionError, Colour, "#errf")
        
        self.assertRaises(AssertionError, Colour, "#f")
        self.assertRaises(AssertionError, Colour, "#faaba")

    def test_hsv(self):
        c1 = Colour('red')
        iterable_assert(self.assertAlmostEqual, c1.to_hsv(), (0, 1, 1, 1))
        
        c1 = Colour('blue')
        iterable_assert(self.assertAlmostEqual, c1.to_hsv(), (0.6666666666666666, 1, 1, 1))
        
        c1 = Colour('yellow')
        iterable_assert(self.assertAlmostEqual, c1.to_hsv(), (0.16666666666666666, 1, 1, 1))
        
        c1 = Colour('cyan')
        iterable_assert(self.assertAlmostEqual, c1.to_hsv(), (0.5, 1, 1, 1))
        
        c1 = Colour('magenta')
        iterable_assert(self.assertAlmostEqual, c1.to_hsv(), (0.8333333333333334, 1, 1, 1))
        
        c1 = Colour('black')
        iterable_assert(self.assertAlmostEqual, c1.to_hsv(), (0, 0, 0, 1))
        
        c1 = Colour('white')
        iterable_assert(self.assertAlmostEqual, c1.to_hsv(), (0, 0, 1, 1))
        
        self.assertEqual(Colour('red'), Colour(hsv=(0, 1, 1, 1)))
        
        self.assertEqual(Colour('white'), Colour(hsv=(0, 0, 1, 1)))
        self.assertEqual(Colour('white', 0.5), Colour(hsv=(0, 0, 1, 0.5)))
        self.assertEqual(Colour('white', 0.5), Colour(hsv=(0, 0, 1), a=0.5))
        
    def test_hsv_malformed(self):
        self.assertRaises(AssertionError, Colour, hsv=(0, 0, 1, 1), a=0.5)
        self.assertRaises(AssertionError, Colour, hsv=(0, 0, 1, 1, 1))
        self.assertRaises(AssertionError, Colour, "white", hsv=(0, 0, 1, 1))
        self.assertRaises(AssertionError, Colour, g=1, hsv=(0, 0, 1, 1))
        self.assertRaises(AssertionError, Colour, b=1, hsv=(0, 0, 1, 1))
        self.assertRaises(AssertionError, Colour, 1, 1, 1, 1, hsv=(0, 0, 1, 1))
        
    def test_copy(self):
        c1 = Colour('red')
        self.assertEqual(c1, Colour(c1))
        
    def test_named_parameters(self):
        '''Test that we can create a colour using named parameters'''
        c = Colour(r=1, g=0, b=0)
        self.assertEqual(c.value, (1, 0, 0, 1))
        
        c = Colour(r=1, g=0, b=0, a=0.5)
        self.assertEqual(c.value, (1, 0, 0, 0.5))
        
        # Test error cases
        self.assertRaises(ValueError, Colour, r=1)  # Missing g and b
        self.assertRaises(ValueError, Colour, r=1, g=0)  # Missing b

    def test_hex_colour_edge_cases(self):
        '''Test edge cases for hex color parsing'''
        # Test short form with alpha
        c = Colour('#fff8')
        self.assertEqual(c.value, (1, 1, 1, 0x88/0xff))
        
        # Test invalid hex characters
        self.assertRaises(AssertionError, Colour, '#xyz')
        self.assertRaises(AssertionError, Colour, '#ffz')
        
        # Test invalid lengths
        self.assertRaises(AssertionError, Colour, '#ff')
        self.assertRaises(AssertionError, Colour, '#fffff')
        self.assertRaises(AssertionError, Colour, '#fffffff')

    def test_hsv_edge_cases(self):
        '''Test edge cases for HSV conversion'''
        # Test grayscale (saturation = 0)
        self.assertEqual(Colour(hsv=(0, 0, 0.5, 1)).value, 
                         (0.5, 0.5, 0.5, 1))
        
        # Test invalid HSV values
        self.assertRaises(AssertionError, Colour, hsv=(2, 1, 1))  # h > 1
        self.assertRaises(AssertionError, Colour, hsv=(-1, 1, 1))  # h < 0
        self.assertRaises(AssertionError, Colour, hsv=(0, 2, 1))  # s > 1
        self.assertRaises(AssertionError, Colour, hsv=(0, 1, 2))  # v > 1
        
        # Test HSV with both tuple alpha and separate alpha
        self.assertRaises(AssertionError, Colour, hsv=(0, 1, 1, 0.5), a=0.3)

    def test_blend_edge_cases(self):
        '''Test edge cases for color blending'''
        c1 = Colour('red')
        c2 = Colour('blue')
        
        # Test weight bounds
        self.assertRaises(AssertionError, c1.blend, c2, -0.1)  # weight < 0
        self.assertRaises(AssertionError, c1.blend, c2, 1.1)   # weight > 1
        
        # Test invalid blend inputs
        self.assertRaises(AssertionError, c1.blend, "blue", 0.5)  # not a Colour
        self.assertRaises(AssertionError, c1.blend, c2, "0.5")    # weight not numeric

    def test_colour_arithmetic(self):
        # Test addition with alpha compositing
        c1 = Colour('red', 0.5)  # (1, 0, 0, 0.5)
        c2 = Colour('blue', 0.5)  # (0, 0, 1, 0.5)
        result = c1.add_and_clamp(c2)
        # Expected: red-biased purple with increased opacity
        iterable_assert(self.assertAlmostEqual, result.value, 
                       (2/3, 0, 1/3, 0.75))

        # Test addition with zero alpha
        c3 = Colour('red', 0)
        c4 = Colour('blue', 0)
        result = c3.add_and_clamp(c4)
        iterable_assert(self.assertAlmostEqual, result.value, 
                       (0, 0, 0, 0))

        # Test subtraction
        c5 = Colour('white', 0.8)  # (1, 1, 1, 0.8)
        c6 = Colour('gray', 0.4)   # (0.5, 0.5, 0.5, 0.4)
        result = c5.subtract_and_clamp(c6)
        iterable_assert(self.assertAlmostEqual, result.value,
                       (0.954367201426025, 0.954367201426025, 0.954367201426025, 0.88))

        # Test scaling with negative factor
        c7 = Colour('red', 0.8)
        result = c7.scale_and_clamp(-0.5)
        iterable_assert(self.assertAlmostEqual, result.value,
                       (0.5, 1, 1, 0.8))  # Inverted and scaled, alpha unchanged

        # Test scaling with factor > 1
        result = c7.scale_and_clamp(1.5)
        iterable_assert(self.assertAlmostEqual, result.value,
                       (1, 0, 0, 0.8))  # Clamped to 1

        # Test addition with full opacity
        c8 = Colour('red')
        c9 = Colour('blue')
        result = c8.add_and_clamp(c9)
        iterable_assert(self.assertAlmostEqual, result.value,
                       (1, 0, 0, 1))  # First color completely obscures second

    def test_arithmetic_operators(self):
        '''Test the arithmetic operator methods'''
        c1 = Colour('red', 0.5)
        c2 = Colour('blue', 0.5)
        
        # Test addition operator
        result = c1 + c2
        iterable_assert(self.assertAlmostEqual, result.value,
                       (2/3, 0, 1/3, 0.75))  # Same as add_and_clamp
        
        # Test subtraction operator
        c3 = Colour('white', 0.8)
        c4 = Colour('gray', 0.4)
        result = c3 - c4
        iterable_assert(self.assertAlmostEqual, result.value,
                       (0.954367201426025, 0.954367201426025, 0.954367201426025, 0.88))
        
        # Test multiplication operators
        c5 = Colour('red', 0.8)
        result = c5 * 0.5
        iterable_assert(self.assertAlmostEqual, result.value,
                       (0.5, 0, 0, 0.8))
        
        # Test reverse multiplication
        result = 0.5 * c5
        iterable_assert(self.assertAlmostEqual, result.value,
                       (0.5, 0, 0, 0.8))
        
        # Test division
        result = c5 / 2
        iterable_assert(self.assertAlmostEqual, result.value,
                       (0.5, 0, 0, 0.8))
        
        # Test invalid operations
        with self.assertRaises(TypeError):
            result = c5 * "0.5"  # Can't multiply by string
        with self.assertRaises(TypeError):
            result = "0.5" * c5  # Can't multiply by string
        with self.assertRaises(TypeError):
            result = c5 / "2"    # Can't divide by string
        with self.assertRaises(TypeError):
            result = c5 + "blue" # Can't add string
        with self.assertRaises(TypeError):
            result = c5 - "blue" # Can't subtract string


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    