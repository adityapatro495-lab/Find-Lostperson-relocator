"""Unit tests for the matching engine. See Project Report Section 8.2.1
and Appendix A.11.

To run: place two photos of the same person and one of a different
person in tests/fixtures/ before running `python manage.py test`.
"""
from django.test import TestCase
from matching.utils import encode_face, compare_faces


class MatchingUtilsTests(TestCase):
    def test_same_person_low_distance(self):
        enc_a = encode_face('tests/fixtures/person_a_1.jpg')
        enc_b = encode_face('tests/fixtures/person_a_2.jpg')
        is_match, distance = compare_faces(enc_a, enc_b)
        self.assertTrue(is_match)
        self.assertLess(distance, 0.6)

    def test_different_person_high_distance(self):
        enc_a = encode_face('tests/fixtures/person_a_1.jpg')
        enc_c = encode_face('tests/fixtures/person_c_1.jpg')
        is_match, distance = compare_faces(enc_a, enc_c)
        self.assertFalse(is_match)

    def test_no_face_returns_none(self):
        result = encode_face('tests/fixtures/no_face.jpg')
        self.assertIsNone(result)
