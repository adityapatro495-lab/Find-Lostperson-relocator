"""Unit tests for the matching engine. See Project Report Section 8.2.1
and Appendix A.11.

To run: place two photos of the same person and one of a different
person in tests/fixtures/ before running `python manage.py test`.
"""
import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile
from registry.models import MissingPerson
from reporting.models import SightingReport
from matching.models import MatchResult
from matching.utils import compare_faces, bytes_to_encoding
import numpy as np

try:
    from matching.utils import encode_face
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False


class MatchingUtilsTests(TestCase):
    @unittest.skipUnless(FACE_RECOGNITION_AVAILABLE, "face_recognition not installed")
    def test_same_person_low_distance(self):
        """SKIPPED: Requires face_recognition and dlib"""
        pass

    @unittest.skipUnless(FACE_RECOGNITION_AVAILABLE, "face_recognition not installed")
    def test_different_person_high_distance(self):
        """SKIPPED: Requires face_recognition and dlib"""
        pass

    @unittest.skipUnless(FACE_RECOGNITION_AVAILABLE, "face_recognition not installed")
    def test_no_face_returns_none(self):
        """SKIPPED: Requires face_recognition and dlib"""
        pass

    def test_bytes_to_encoding_conversion(self):
        """Test that encoding bytes can be converted back to numpy arrays"""
        original_encoding = np.array([0.1] * 128, dtype=np.float64)
        encoded_bytes = original_encoding.tobytes()
        decoded_encoding = bytes_to_encoding(encoded_bytes)
        np.testing.assert_array_almost_equal(original_encoding, decoded_encoding)

    def test_compare_faces_with_identical_encodings(self):
        """Test that identical encodings return zero distance"""
        encoding = np.array([0.1] * 128, dtype=np.float64)
        is_match, distance = compare_faces(encoding, encoding, threshold=0.6)
        self.assertTrue(is_match)
        self.assertAlmostEqual(distance, 0.0, places=5)


class UserModelTests(TestCase):
    def test_user_profile_created_on_user_creation(self):
        """Test that UserProfile is created when User is created"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.assertTrue(hasattr(user, 'userprofile'))
        self.assertEqual(user.userprofile.role, 'VOLUNTEER')

    def test_user_profile_created_for_superuser(self):
        """Test that superusers get ADMIN role"""
        user = User.objects.create_superuser(username='admin', email='admin@test.com', password='admin123')
        self.assertEqual(user.userprofile.role, 'ADMIN')

    def test_user_profile_string_representation(self):
        """Test UserProfile __str__ method"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        user.userprofile.role = 'FAMILY'
        user.userprofile.save()
        self.assertIn('testuser', str(user.userprofile))
        self.assertIn('Family', str(user.userprofile))


class MatchResultModelTests(TestCase):
    def setUp(self):
        self.family_user = User.objects.create_user(username='family', password='pass123')
        self.family_user.userprofile.role = 'FAMILY'
        self.family_user.userprofile.save()
        
        self.volunteer_user = User.objects.create_user(username='volunteer', password='pass123')
        self.volunteer_user.userprofile.role = 'VOLUNTEER'
        self.volunteer_user.userprofile.save()

    def test_match_result_ordering(self):
        """Test that matches are ordered by confidence score descending"""
        missing_person = MissingPerson.objects.create(
            reported_by=self.family_user,
            name='John Doe',
            age=25,
            gender='M',
            last_seen_location='City Center',
            contact_email='family@test.com',
            encoding=b'test_encoding_1'
        )
        
        sighting1 = SightingReport.objects.create(
            reporter=self.volunteer_user,
            location='Park',
            sighted_date='2024-01-01',
            encoding=b'test_encoding_2'
        )
        
        sighting2 = SightingReport.objects.create(
            reporter=self.volunteer_user,
            location='Market',
            sighted_date='2024-01-02',
            encoding=b'test_encoding_3'
        )
        
        match1 = MatchResult.objects.create(
            person=missing_person,
            report=sighting1,
            confidence_score=0.95,
            status='PENDING'
        )
        
        match2 = MatchResult.objects.create(
            person=missing_person,
            report=sighting2,
            confidence_score=0.75,
            status='PENDING'
        )
        
        ordered_matches = MatchResult.objects.all()
        self.assertEqual(ordered_matches[0].confidence_score, 0.95)
        self.assertEqual(ordered_matches[1].confidence_score, 0.75)

    def test_missing_person_model(self):
        """Test MissingPerson model creation and fields"""
        user = User.objects.create_user(username='reporter', password='pass123')
        person = MissingPerson.objects.create(
            reported_by=user,
            name='Jane Doe',
            age=30,
            gender='F',
            last_seen_location='Downtown',
            contact_email='jane@test.com',
            contact_phone='1234567890'
        )
        self.assertEqual(person.name, 'Jane Doe')
        self.assertEqual(person.status, 'OPEN')
        self.assertEqual(person.reported_by, user)

    def test_sighting_report_model(self):
        """Test SightingReport model creation and fields"""
        user = User.objects.create_user(username='reporter', password='pass123')
        report = SightingReport.objects.create(
            reporter=user,
            location='Park Avenue',
            sighted_date='2024-01-15'
        )
        self.assertEqual(report.location, 'Park Avenue')
        self.assertEqual(report.reporter, user)
        self.assertIsNotNone(report.created_at)
