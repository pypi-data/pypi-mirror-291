"""Unit tests for file attachments and related functionality."""

from __future__ import annotations

import json
import mimeparse
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.safestring import SafeText
from djblets.testing.decorators import add_fixtures
from kgb import SpyAgency

from reviewboard.attachments.forms import UploadFileForm, UploadUserFileForm
from reviewboard.attachments.mimetypes import (MimetypeHandler,
                                               logger as mimetypes_logger,
                                               register_mimetype_handler,
                                               score_match,
                                               unregister_mimetype_handler)
from reviewboard.attachments.models import (FileAttachment,
                                            FileAttachmentHistory)
from reviewboard.diffviewer.models import DiffSet, FileDiff
from reviewboard.scmtools.core import PRE_CREATION
from reviewboard.site.models import LocalSite
from reviewboard.testing import TestCase


class BaseFileAttachmentTestCase(TestCase):
    """Base functionality for FileAttachment test cases."""

    fixtures = ['test_users', 'test_scmtools', 'test_site']

    def make_uploaded_file(self):
        """Create a return a file to use for mocking in forms."""
        filename = os.path.join(settings.STATIC_ROOT,
                                'rb', 'images', 'logo.png')

        with open(filename, 'rb') as fp:
            uploaded_file = SimpleUploadedFile(fp.name, fp.read(),
                                               content_type='image/png')

        return uploaded_file

    def make_filediff(self, is_new=False, diffset_history=None,
                      diffset_revision=1, source_filename='file1',
                      dest_filename='file2'):
        """Create and return a FileDiff with the given data."""
        if is_new:
            source_revision = PRE_CREATION
            dest_revision = ''
        else:
            source_revision = '1'
            dest_revision = '2'

        repository = self.create_repository()

        if not diffset_history:
            user = User.objects.get(username='doc')
            review_request = self.create_review_request(repository=repository,
                                                        submitter=user)
            diffset_history = review_request.diffset_history

        diffset = DiffSet.objects.create(name='test',
                                         revision=diffset_revision,
                                         repository=repository,
                                         history=diffset_history)
        filediff = FileDiff(source_file=source_filename,
                            source_revision=source_revision,
                            dest_file=dest_filename,
                            dest_detail=dest_revision,
                            diffset=diffset,
                            binary=True)
        filediff.save()

        return filediff


class FileAttachmentTests(BaseFileAttachmentTestCase):
    """Tests for the FileAttachment model."""

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_upload_file(self):
        """Testing uploading a file attachment"""
        review_request = self.create_review_request(publish=True)

        file = self.make_uploaded_file()
        form = UploadFileForm(review_request, files={
            'path': file,
        })
        self.assertTrue(form.is_valid())

        file_attachment = form.create()
        file_attachment.refresh_from_db()

        self.assertTrue(os.path.basename(file_attachment.file.name).endswith(
            '__logo.png'))
        self.assertEqual(file_attachment.mimetype, 'image/png')
        self.assertEqual(file_attachment.extra_data, {})

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_upload_file_with_history(self):
        """Testing uploading a file attachment to an existing
        FileAttachmentHistory
        """
        review_request_1 = self.create_review_request(publish=True)
        history = FileAttachmentHistory.objects.create(display_position=0)
        review_request_1.file_attachment_histories.add(history)

        file = self.make_uploaded_file()
        form = UploadFileForm(review_request_1,
                              data={'attachment_history': history.pk},
                              files={'path': file})
        self.assertTrue(form.is_valid())
        form.create()

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_upload_file_with_history_mismatch(self):
        """Testing uploading a file attachment to an existing
        FileAttachmentHistory with a mismatched review request
        """
        review_request_1 = self.create_review_request(publish=True)
        review_request_2 = self.create_review_request(publish=True)
        uploaded_file = self.make_uploaded_file()

        history = FileAttachmentHistory.objects.create(display_position=0)
        review_request_1.file_attachment_histories.add(history)

        form = UploadFileForm(review_request_2,
                              data={'attachment_history': history.pk},
                              files={'path': uploaded_file})
        self.assertFalse(form.is_valid())

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_upload_file_revisions(self):
        """Testing uploading multiple revisions of a file"""
        user = User.objects.create_user(username='testuser')
        review_request = self.create_review_request(publish=True,
                                                    target_people=[user])
        history = FileAttachmentHistory.objects.create(display_position=0)
        review_request.file_attachment_histories.add(history)
        uploaded_file = self.make_uploaded_file()

        # Add a file with the given history
        form = UploadFileForm(review_request,
                              data={'attachment_history': history.pk},
                              files={'path': uploaded_file})
        self.assertTrue(form.is_valid())
        file_attachment = form.create()
        history = FileAttachmentHistory.objects.get(pk=history.pk)
        self.assertEqual(file_attachment.attachment_revision, 1)
        self.assertEqual(history.latest_revision, 1)
        self.assertEqual(history.display_position, 0)

        review_request.get_draft().publish()
        # Post an update
        form = UploadFileForm(review_request,
                              data={'attachment_history': history.pk},
                              files={'path': uploaded_file})
        self.assertTrue(form.is_valid())
        file_attachment = form.create()
        history = FileAttachmentHistory.objects.get(pk=history.pk)
        self.assertEqual(file_attachment.attachment_revision, 2)
        self.assertEqual(history.latest_revision, 2)
        self.assertEqual(history.display_position, 0)

        review_request.get_draft().publish()

        # Post two updates without publishing the draft in between
        form = UploadFileForm(review_request,
                              data={'attachment_history': history.pk},
                              files={'path': uploaded_file})
        self.assertTrue(form.is_valid())
        file_attachment = form.create()
        history = FileAttachmentHistory.objects.get(pk=history.pk)
        self.assertEqual(file_attachment.attachment_revision, 3)
        self.assertEqual(history.latest_revision, 3)
        self.assertEqual(history.display_position, 0)

        form = UploadFileForm(review_request,
                              data={'attachment_history': history.pk},
                              files={'path': uploaded_file})
        self.assertTrue(form.is_valid())
        file_attachment = form.create()
        history = FileAttachmentHistory.objects.get(pk=history.pk)
        self.assertEqual(file_attachment.attachment_revision, 3)
        self.assertEqual(history.latest_revision, 3)
        self.assertEqual(history.display_position, 0)

        # Add another (unrelated) file to check display position
        form = UploadFileForm(review_request,
                              files={'path': uploaded_file})
        self.assertTrue(form.is_valid())
        file_attachment = form.create()
        self.assertEqual(file_attachment.attachment_revision, 1)
        self.assertEqual(file_attachment.attachment_history.latest_revision, 1)
        self.assertEqual(file_attachment.attachment_history.display_position,
                         1)

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_upload_file_with_extra_data(self):
        """Testing uploading a file attachment with extra data"""
        class TestObject():
            def to_json(self):
                return {
                    'foo': 'bar'
                }

        review_request = self.create_review_request(publish=True)

        file = self.make_uploaded_file()
        form = UploadFileForm(
            review_request,
            data={
                'extra_data': {
                    'test_bool': True,
                    'test_date': datetime(2023, 1, 26, 5, 30, 3, 123456),
                    'test_int': 1,
                    'test_list': [1, 2, 3],
                    'test_nested_dict': {
                        'foo': 2,
                        'bar': 'baz',
                    },
                    'test_none': None,
                    'test_obj': TestObject(),
                    'test_str': 'test',
                }
            },
            files={'path': file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create()
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {
            'test_bool': True,
            'test_date': '2023-01-26T05:30:03.123',
            'test_int': 1,
            'test_list': [1, 2, 3],
            'test_nested_dict': {
                'foo': 2,
                'bar': 'baz',
            },
            'test_none': None,
            'test_obj': {
                'foo': 'bar',
            },
            'test_str': 'test',
        })

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_upload_file_with_extra_data_string(self):
        """Testing uploading a file attachment with extra data passed as a
        JSON string
        """
        review_request = self.create_review_request(publish=True)

        file = self.make_uploaded_file()
        form = UploadFileForm(
            review_request,
            data={
                'extra_data': json.dumps({
                    'test_bool': True,
                    'test_int': 1,
                    'test_list': [1, 2, 3],
                    'test_nested_dict': {
                        'foo': 2,
                        'bar': 'baz',
                    },
                    'test_none': None,
                    'test_str': 'test',
                })
            },
            files={'path': file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create()
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {
            'test_bool': True,
            'test_int': 1,
            'test_list': [1, 2, 3],
            'test_nested_dict': {
                'foo': 2,
                'bar': 'baz',
            },
            'test_none': None,
            'test_str': 'test',
        })

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_upload_file_with_extra_data_empties(self):
        """Testing uploading a file attachment with extra data that contains
        empty values
        """
        review_request = self.create_review_request(publish=True)
        file = self.make_uploaded_file()

        form = UploadFileForm(
            review_request,
            data={
                'extra_data': {}
            },
            files={'path': file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create()
        file_attachment.refresh_from_db()
        self.assertEqual(file_attachment.extra_data, {})

        form = UploadFileForm(
            review_request,
            data={
                'extra_data': json.dumps(None)
            },
            files={'path': file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create()
        file_attachment.refresh_from_db()
        self.assertEqual(file_attachment.extra_data, {})

        form = UploadFileForm(
            review_request,
            data={
                'extra_data': None
            },
            files={'path': file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create()
        file_attachment.refresh_from_db()
        self.assertEqual(file_attachment.extra_data, {})

        form = UploadFileForm(
            review_request,
            data={
                'extra_data': {
                    'test_list': [],
                    'test_nested_dict': {},
                    'test_none': None,
                    'test_str': '',
                }
            },
            files={'path': file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create()
        file_attachment.refresh_from_db()
        self.assertEqual(file_attachment.extra_data, {
            'test_list': [],
            'test_nested_dict': {},
            'test_none': None,
            'test_str': '',
        })

    def test_is_from_diff_with_no_association(self):
        """Testing FileAttachment.is_from_diff with standard attachment"""
        file_attachment = FileAttachment()

        self.assertFalse(file_attachment.is_from_diff)

    @add_fixtures(['test_scmtools'])
    def test_is_from_diff_with_repository(self):
        """Testing FileAttachment.is_from_diff with repository association"""
        repository = self.create_repository()
        file_attachment = FileAttachment(repository=repository)

        self.assertTrue(file_attachment.is_from_diff)

    @add_fixtures(['test_scmtools'])
    def test_is_from_diff_with_filediff(self):
        """Testing FileAttachment.is_from_diff with filediff association"""
        filediff = self.make_filediff()
        file_attachment = FileAttachment(added_in_filediff=filediff)

        self.assertTrue(file_attachment.is_from_diff)

    @add_fixtures(['test_users', 'test_scmtools'])
    def test_utf16_thumbnail(self):
        """Testing file attachment thumbnail generation for UTF-16 files"""
        filename = os.path.join(os.path.dirname(__file__),
                                'testdata', 'utf-16.txt')
        with open(filename, 'rb') as f:
            review_request = self.create_review_request(publish=True)

            file = SimpleUploadedFile(
                f.name,
                f.read(),
                content_type='text/plain;charset=utf-16le')
            form = UploadFileForm(review_request, files={'path': file})
            form.is_valid()

            file_attachment = form.create()

            self.assertEqual(
                file_attachment.thumbnail,
                '<div class="file-thumbnail"> <div class="file-thumbnail-clipp'
                'ed"><pre>UTF-16le encoded sample plain-text file</pre><pre>'
                '\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e'
                '\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e'
                '\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e'
                '\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e\u203e</pre>'
                '<pre></pre><pre>Markus Kuhn [\u02c8ma\u02b3k\u028as ku\u02d0'
                'n] &lt;http://www.cl.cam.ac.uk/~mgk25/&gt; \u2014 2002-07-25'
                '</pre><pre></pre><pre></pre><pre>The ASCII compatible UTF-8 '
                'encoding used in this plain-text file</pre><pre>is defined '
                'in Unicode, ISO 10646-1, and RFC 2279.</pre><pre></pre><pre>'
                '</pre><pre>Using Unicode/UTF-8, you can write in emails and '
                'source code things such as</pre><pre></pre><pre>Mathematics '
                'and sciences:</pre><pre></pre><pre>  \u222e E\u22c5da = Q,  '
                'n \u2192 \u221e, \u2211 f(i) = \u220f g(i),      \u23a7\u23a1'
                '\u239b\u250c\u2500\u2500\u2500\u2500\u2500\u2510\u239e\u23a4'
                '\u23ab</pre><pre>                                           '
                ' \u23aa\u23a2\u239c\u2502a\xb2+b\xb3 \u239f\u23a5\u23aa'
                '</pre><pre>  \u2200x\u2208</pre></div></div>')


class UserFileAttachmentTests(BaseFileAttachmentTestCase):
    fixtures = ['test_users']

    def test_user_file_add_file_after_create(self):
        """Testing user FileAttachment create without initial file and
        adding file through update
        """
        user = User.objects.get(username='doc')

        form = UploadUserFileForm(files={})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)
        file_attachment.refresh_from_db()

        self.assertFalse(file_attachment.file)
        self.assertEqual(file_attachment.user, user)
        self.assertEqual(file_attachment.extra_data, {})

        uploaded_file = self.make_uploaded_file()
        form = UploadUserFileForm(files={
            'path': uploaded_file,
        })
        self.assertTrue(form.is_valid())

        file_attachment = form.update(file_attachment)
        file_attachment.refresh_from_db()

        self.assertTrue(os.path.basename(file_attachment.file.name).endswith(
            '__logo.png'))
        self.assertEqual(file_attachment.mimetype, 'image/png')

    def test_user_file_with_upload_file(self):
        """Testing user FileAttachment create with initial file"""
        user = User.objects.get(username='doc')
        uploaded_file = self.make_uploaded_file()

        form = UploadUserFileForm(files={
            'path': uploaded_file,
        })
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)

        self.assertEqual(file_attachment.user, user)
        self.assertTrue(os.path.basename(file_attachment.file.name).endswith(
            '__logo.png'))
        self.assertEqual(file_attachment.mimetype, 'image/png')
        self.assertEqual(file_attachment.extra_data, {})

    def test_user_file_with_extra_data(self):
        """Testing user FileAttachment create with extra data"""
        class TestObject():
            def to_json(self):
                return {
                    'foo': 'bar'
                }

        user = User.objects.get(username='doc')
        uploaded_file = self.make_uploaded_file()

        form = UploadUserFileForm(
            data={
                'extra_data': {
                    'test_bool': True,
                    'test_date': datetime(2023, 1, 26, 5, 30, 3, 123456),
                    'test_int': 1,
                    'test_list': [1, 2, 3],
                    'test_nested_dict': {
                        'foo': 2,
                        'bar': 'baz',
                    },
                    'test_none': None,
                    'test_obj': TestObject(),
                    'test_str': 'test',
                }
            },
            files={'path': uploaded_file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.user, user)
        self.assertTrue(os.path.basename(file_attachment.file.name).endswith(
            '__logo.png'))
        self.assertEqual(file_attachment.mimetype, 'image/png')
        self.assertEqual(file_attachment.extra_data, {
            'test_bool': True,
            'test_date': '2023-01-26T05:30:03.123',
            'test_int': 1,
            'test_list': [1, 2, 3],
            'test_nested_dict': {
                'foo': 2,
                'bar': 'baz',
            },
            'test_none': None,
            'test_obj': {
                'foo': 'bar',
            },
            'test_str': 'test',
        })

    def test_user_file_with_extra_data_string(self):
        """Testing user FileAttachment create with extra data passed as a
        JSON string
        """
        user = User.objects.get(username='doc')
        uploaded_file = self.make_uploaded_file()

        form = UploadUserFileForm(
            data={
                'extra_data': json.dumps({
                    'test_bool': True,
                    'test_int': 1,
                    'test_list': [1, 2, 3],
                    'test_nested_dict': {
                        'foo': 2,
                        'bar': 'baz',
                    },
                    'test_none': None,
                    'test_str': 'test',
                })
            },
            files={'path': uploaded_file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {
            'test_bool': True,
            'test_int': 1,
            'test_list': [1, 2, 3],
            'test_nested_dict': {
                'foo': 2,
                'bar': 'baz',
            },
            'test_none': None,
            'test_str': 'test',
        })

    def test_user_file_with_extra_data_empties(self):
        """Testing user FileAttachment create with extra data that contains
        empty values
        """
        user = User.objects.get(username='doc')
        uploaded_file = self.make_uploaded_file()

        form = UploadUserFileForm(
            data={
                'extra_data': {}
            },
            files={'path': uploaded_file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {})

        form = UploadUserFileForm(
            data={
                'extra_data': json.dumps(None)
            },
            files={'path': uploaded_file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {})

        form = UploadUserFileForm(
            data={
                'extra_data': None
            },
            files={'path': uploaded_file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {})

        form = UploadUserFileForm(
            data={
                'extra_data': {
                    'test_list': [],
                    'test_nested_dict': {},
                    'test_none': None,
                    'test_str': '',
                }
            },
            files={'path': uploaded_file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {
            'test_list': [],
            'test_nested_dict': {},
            'test_none': None,
            'test_str': '',
        })

    @add_fixtures(['test_site'])
    def test_user_file_local_sites(self):
        """Testing user FileAttachment create with local site"""
        user = User.objects.get(username='doc')
        local_site = LocalSite.objects.get(name='local-site-1')

        form = UploadUserFileForm(files={})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user, local_site)

        self.assertEqual(file_attachment.user, user)
        self.assertEqual(file_attachment.local_site, local_site)

    def test_user_file_update_with_extra_data(self):
        """Testing user FileAttachment update with extra data"""
        class TestObject():
            def to_json(self):
                return {
                    'foo': 'bar'
                }

        user = User.objects.get(username='doc')
        uploaded_file = self.make_uploaded_file()

        form = UploadUserFileForm(files={'path': uploaded_file})
        self.assertTrue(form.is_valid())

        file_attachment = form.create(user)
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {})

        form = UploadUserFileForm(
            data={
                'extra_data': {
                    'test_bool': True,
                    'test_date': datetime(2023, 1, 26, 5, 30, 3, 123456),
                    'test_int': 1,
                    'test_list': [1, 2, 3],
                    'test_nested_dict': {
                        'foo': 2,
                        'bar': 'baz',
                    },
                    'test_none': None,
                    'test_obj': TestObject(),
                    'test_str': 'test',
                }
            }
        )
        self.assertTrue(form.is_valid())

        file_attachment = form.update(file_attachment)
        file_attachment.refresh_from_db()

        self.assertEqual(file_attachment.extra_data, {
            'test_bool': True,
            'test_date': '2023-01-26T05:30:03.123',
            'test_int': 1,
            'test_list': [1, 2, 3],
            'test_nested_dict': {
                'foo': 2,
                'bar': 'baz',
            },
            'test_none': None,
            'test_obj': {
                'foo': 'bar',
            },
            'test_str': 'test',
        })

    @add_fixtures(['test_site'])
    def test_user_file_is_accessible_by(self):
        """Testing user FileAttachment.is_accessible_by"""
        creating_user = User.objects.get(username='doc')
        admin_user = User.objects.get(username='admin')
        same_site_user = User.objects.get(username='dopey')
        different_site_user = User.objects.get(username='grumpy')

        local_site = LocalSite.objects.get(name='local-site-1')
        local_site.users.add(same_site_user)

        form = UploadUserFileForm(files={})
        self.assertTrue(form.is_valid())
        file_attachment = form.create(creating_user, local_site)

        self.assertTrue(file_attachment.is_accessible_by(admin_user))
        self.assertTrue(file_attachment.is_accessible_by(creating_user))
        self.assertFalse(file_attachment.is_accessible_by(AnonymousUser()))
        self.assertFalse(file_attachment.is_accessible_by(same_site_user))
        self.assertFalse(file_attachment.is_accessible_by(different_site_user))

    @add_fixtures(['test_site'])
    def test_user_file_is_mutable_by(self):
        """Testing user FileAttachment.is_mutable_by"""
        creating_user = User.objects.get(username='doc')
        admin_user = User.objects.get(username='admin')
        same_site_user = User.objects.get(username='dopey')
        different_site_user = User.objects.get(username='grumpy')

        local_site = LocalSite.objects.get(name='local-site-1')
        local_site.users.add(same_site_user)

        form = UploadUserFileForm(files={})
        self.assertTrue(form.is_valid())
        file_attachment = form.create(creating_user, local_site)

        self.assertTrue(file_attachment.is_mutable_by(admin_user))
        self.assertTrue(file_attachment.is_mutable_by(creating_user))
        self.assertFalse(file_attachment.is_mutable_by(AnonymousUser()))
        self.assertFalse(file_attachment.is_mutable_by(same_site_user))
        self.assertFalse(file_attachment.is_mutable_by(different_site_user))


class MimetypeTest(MimetypeHandler):
    """Handler for all test mimetypes."""

    supported_mimetypes = ['test/*']


class TestAbcMimetype(MimetypeHandler):
    """Handler for the test/abc mimetype."""

    supported_mimetypes = ['test/abc']


class TestXmlMimetype(MimetypeHandler):
    """Handler for the test/xml mimetype."""

    supported_mimetypes = ['test/xml']


class Test2AbcXmlMimetype(MimetypeHandler):
    """Handler for the test/abc+xml mimetype."""

    supported_mimetypes = ['test2/abc+xml']


class StarDefMimetype(MimetypeHandler):
    """Handler for all /def mimetypes."""

    supported_mimetypes = ['*/def']


class StarAbcDefMimetype(MimetypeHandler):
    """Handler for all /abc+def mimetypes."""

    supported_mimetypes = ['*/abc+def']


class Test3XmlMimetype(MimetypeHandler):
    """Handler for the test3/xml mimetype."""

    supported_mimetypes = ['test3/xml']


class Test3AbcXmlMimetype(MimetypeHandler):
    """Handler for the test3/abc+xml mimetype."""

    supported_mimetypes = ['test3/abc+xml']


class Test3StarMimetype(MimetypeHandler):
    """Handler for all test3 mimetypes."""

    supported_mimetypes = ['test3/*']


class MimetypeHandlerTests(TestCase):
    """Tests for mimetype handlers."""

    def setUp(self):
        """Set up this test case."""
        super(MimetypeHandlerTests, self).setUp()

        # Register test cases in same order as they are defined
        # in this test
        register_mimetype_handler(MimetypeTest)
        register_mimetype_handler(TestAbcMimetype)
        register_mimetype_handler(TestXmlMimetype)
        register_mimetype_handler(Test2AbcXmlMimetype)
        register_mimetype_handler(StarDefMimetype)
        register_mimetype_handler(StarAbcDefMimetype)
        register_mimetype_handler(Test3XmlMimetype)
        register_mimetype_handler(Test3AbcXmlMimetype)
        register_mimetype_handler(Test3StarMimetype)

    def tearDown(self):
        """Tear down this test case."""
        super(MimetypeHandlerTests, self).tearDown()

        # Unregister test cases in same order as they are defined
        # in this test
        unregister_mimetype_handler(MimetypeTest)
        unregister_mimetype_handler(TestAbcMimetype)
        unregister_mimetype_handler(TestXmlMimetype)
        unregister_mimetype_handler(Test2AbcXmlMimetype)
        unregister_mimetype_handler(StarDefMimetype)
        unregister_mimetype_handler(StarAbcDefMimetype)
        unregister_mimetype_handler(Test3XmlMimetype)
        unregister_mimetype_handler(Test3AbcXmlMimetype)
        unregister_mimetype_handler(Test3StarMimetype)

    def _handler_for(self, mimetype):
        mt = mimeparse.parse_mime_type(mimetype)
        score, handler = MimetypeHandler.get_best_handler(mt)
        return handler

    def test_handler_factory(self):
        """Testing matching of factory method for mimetype handlers"""
        # Exact Match
        self.assertEqual(self._handler_for("test/abc"), TestAbcMimetype)
        self.assertEqual(self._handler_for("test2/abc+xml"),
                         Test2AbcXmlMimetype)
        # Handle vendor-specific match
        self.assertEqual(self._handler_for("test/abc+xml"), TestXmlMimetype)
        self.assertEqual(self._handler_for("test2/xml"), Test2AbcXmlMimetype)

    def test_handler_factory_precedence(self):
        """Testing precedence of factory method for mimetype handlers"""
        self.assertEqual(self._handler_for("test2/def"), StarDefMimetype)
        self.assertEqual(self._handler_for("test3/abc+xml"),
                         Test3AbcXmlMimetype)
        self.assertEqual(self._handler_for("test3/xml"), Test3XmlMimetype)
        self.assertEqual(self._handler_for("foo/abc+def"), StarAbcDefMimetype)
        self.assertEqual(self._handler_for("foo/def"), StarDefMimetype)
        # Left match and Wildcard should trump Left Wildcard and match
        self.assertEqual(self._handler_for("test/def"), MimetypeTest)

    def test_mimetype_match_scoring(self):
        """Testing score_match for different mimetype patterns"""
        def assert_score(pattern, test, score):
            self.assertAlmostEqual(
                score_match(mimeparse.parse_mime_type(pattern),
                            mimeparse.parse_mime_type(test)),
                score)

        assert_score('application/reviewboard+x-pdf',
                     'application/reviewboard+x-pdf', 2.0)
        assert_score('application/x-pdf', 'application/x-pdf', 1.9)
        assert_score('text/*', 'text/plain', 1.8)
        assert_score('*/reviewboard+plain', 'text/reviewboard+plain', 1.7)
        assert_score('*/plain', 'text/plain', 1.6)
        assert_score('application/x-javascript', 'application/x-pdf', 0)


class FileAttachmentManagerTests(BaseFileAttachmentTestCase):
    """Tests for FileAttachmentManager."""

    fixtures = ['test_users', 'test_scmtools', 'test_site']

    def test_create_from_filediff_sets_relation_counter(self):
        """Testing FileAttachmentManager.create_from_filediff sets
        ReviewRequest.file_attachment_count counter
        """
        user = User.objects.get(username='doc')
        repository = self.create_repository()
        review_request = self.create_review_request(repository=repository,
                                                    submitter=user)
        diffset_history = review_request.diffset_history

        filediff = self.make_filediff(diffset_history=diffset_history)

        self.assertEqual(review_request.file_attachments_count, 0)

        FileAttachment.objects.create_from_filediff(
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png')

        review_request.refresh_from_db()
        self.assertEqual(review_request.file_attachments_count, 1)

    def test_create_from_filediff_with_new_and_modified_true(self):
        """Testing FileAttachmentManager.create_from_filediff
        with new FileDiff and modified=True
        """
        filediff = self.make_filediff(is_new=True)
        self.assertTrue(filediff.is_new)

        file_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png')
        self.assertEqual(file_attachment.repository_id, None)
        self.assertEqual(file_attachment.repo_path, None)
        self.assertEqual(file_attachment.repo_revision, None)
        self.assertEqual(file_attachment.added_in_filediff, filediff)

    def test_create_from_filediff_with_new_and_modified_false(self):
        """Testing FileAttachmentManager.create_from_filediff
        with new FileDiff and modified=False
        """
        filediff = self.make_filediff(is_new=True)
        self.assertTrue(filediff.is_new)

        self.assertRaises(
            AssertionError,
            FileAttachment.objects.create_from_filediff,
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png',
            from_modified=False)

    def test_create_from_filediff_with_existing_and_modified_true(self):
        """Testing FileAttachmentManager.create_from_filediff
        with existing FileDiff and modified=True
        """
        filediff = self.make_filediff()
        self.assertFalse(filediff.is_new)

        file_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png')
        self.assertIsNone(file_attachment.repository_id)
        self.assertIsNone(file_attachment.repo_path)
        self.assertIsNone(file_attachment.repo_revision)
        self.assertEqual(file_attachment.added_in_filediff, filediff)

    def test_create_from_filediff_with_existing_and_modified_false(self):
        """Testing FileAttachmentManager.create_from_filediff
        with existing FileDiff and modified=False
        """
        filediff = self.make_filediff()
        self.assertFalse(filediff.is_new)

        file_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png',
            from_modified=False)
        self.assertEqual(file_attachment.repository, filediff.get_repository())
        self.assertEqual(file_attachment.repo_path, filediff.source_file)
        self.assertEqual(file_attachment.repo_revision,
                         filediff.source_revision)
        self.assertEqual(file_attachment.added_in_filediff_id, None)

    def test_get_for_filediff_with_new_and_modified_true(self):
        """Testing FileAttachmentManager.get_for_filediff
        with new FileDiff and modified=True
        """
        filediff = self.make_filediff(is_new=True)
        self.assertTrue(filediff.is_new)

        file_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png')

        self.assertEqual(
            FileAttachment.objects.get_for_filediff(filediff, modified=True),
            file_attachment)

    def test_get_for_filediff_with_new_and_modified_false(self):
        """Testing FileAttachmentManager.get_for_filediff
        with new FileDiff and modified=False
        """
        filediff = self.make_filediff(is_new=True)
        self.assertTrue(filediff.is_new)

        FileAttachment.objects.create_from_filediff(
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png')

        self.assertEqual(
            FileAttachment.objects.get_for_filediff(filediff, modified=False),
            None)

    def test_get_for_filediff_with_existing_and_modified_true(self):
        """Testing FileAttachmentManager.get_for_filediff
        with existing FileDiff and modified=True
        """
        filediff = self.make_filediff()
        self.assertFalse(filediff.is_new)

        file_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png')

        self.assertEqual(
            FileAttachment.objects.get_for_filediff(filediff, modified=True),
            file_attachment)

    def test_get_for_filediff_with_existing_and_modified_false(self):
        """Testing FileAttachmentManager.get_for_filediff
        with existing FileDiff and modified=False
        """
        filediff = self.make_filediff()
        self.assertFalse(filediff.is_new)

        file_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            file=self.make_uploaded_file(),
            mimetype='image/png',
            from_modified=False)

        self.assertEqual(
            FileAttachment.objects.get_for_filediff(filediff, modified=False),
            file_attachment)


class DiffViewerFileAttachmentTests(BaseFileAttachmentTestCase):
    """Tests for inline diff file attachments in the diff viewer."""

    def setUp(self):
        """Set up this test case."""
        super(DiffViewerFileAttachmentTests, self).setUp()

        # The diff viewer's caching breaks the result of these tests,
        # so be sure we clear before each one.
        cache.clear()

    def test_added_file(self):
        """Testing inline diff file attachments with newly added files"""
        # Set up the initial state.
        user = User.objects.get(username='doc')
        review_request = self.create_review_request(submitter=user,
                                                    target_people=[user])
        filediff = self.make_filediff(
            is_new=True,
            diffset_history=review_request.diffset_history)

        # Create a diff file attachment to be displayed inline.
        diff_file_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            orig_filename='my-file',
            file=self.make_uploaded_file(),
            mimetype='image/png')
        review_request.file_attachments.add(diff_file_attachment)
        review_request.save()
        review_request.publish(user)

        # Load the diff viewer.
        self.client.login(username='doc', password='doc')
        response = self.client.get('/r/%d/diff/1/fragment/%s/'
                                   % (review_request.pk, filediff.pk))
        self.assertEqual(response.status_code, 200)

        # The file attachment should appear as the right-hand side
        # file attachment in the diff viewer.
        self.assertEqual(response.context['orig_diff_file_attachment'], None)
        self.assertEqual(response.context['modified_diff_file_attachment'],
                         diff_file_attachment)

    def test_modified_file(self):
        """Testing inline diff file attachments with modified files"""
        # Set up the initial state.
        user = User.objects.get(username='doc')
        review_request = self.create_review_request(submitter=user)
        filediff = self.make_filediff(
            is_new=False,
            diffset_history=review_request.diffset_history)
        self.assertFalse(filediff.is_new)

        # Create diff file attachments to be displayed inline.
        uploaded_file = self.make_uploaded_file()

        orig_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            orig_filename='my-file',
            file=uploaded_file,
            mimetype='image/png',
            from_modified=False)
        modified_attachment = FileAttachment.objects.create_from_filediff(
            filediff,
            orig_filename='my-file',
            file=uploaded_file,
            mimetype='image/png')
        review_request.file_attachments.add(orig_attachment)
        review_request.file_attachments.add(modified_attachment)
        review_request.publish(user)

        # Load the diff viewer.
        self.client.login(username='doc', password='doc')
        response = self.client.get('/r/%d/diff/1/fragment/%s/'
                                   % (review_request.pk, filediff.pk))
        self.assertEqual(response.status_code, 200)

        # The file attachment should appear as the right-hand side
        # file attachment in the diff viewer.
        self.assertEqual(response.context['orig_diff_file_attachment'],
                         orig_attachment)
        self.assertEqual(response.context['modified_diff_file_attachment'],
                         modified_attachment)


class SandboxMimetypeHandler(MimetypeHandler):
    """Handler for image/png mimetypes, used for testing sandboxing."""

    supported_mimetypes = ['image/png']

    def get_icon_url(self):
        """Raise an exception to test sandboxing."""
        raise Exception

    def get_thumbnail(self):
        """Raise an exception to test sandboxing."""
        raise Exception

    def set_thumbnail(self, data):
        """Raise an exception to test sandboxing."""
        raise Exception


class SandboxTests(SpyAgency, BaseFileAttachmentTestCase):
    """Testing MimetypeHandler sandboxing."""

    def setUp(self):
        """Set up this test case."""
        super(SandboxTests, self).setUp()

        register_mimetype_handler(SandboxMimetypeHandler)

        user = User.objects.create_user(username='reviewboard',
                                        password='password',
                                        email='reviewboard@example.com')

        review_request = self.create_review_request(submitter=user)
        self.file_attachment = self.create_file_attachment(
            review_request=review_request)

    def tearDown(self):
        """Tear down this test case."""
        super(SandboxTests, self).tearDown()

        unregister_mimetype_handler(SandboxMimetypeHandler)

    def test_get_thumbnail(self):
        """Testing FileAttachment sandboxes MimetypeHandler.get_thumbnail"""
        self.spy_on(SandboxMimetypeHandler.get_thumbnail,
                    owner=SandboxMimetypeHandler)

        self.file_attachment.thumbnail
        self.assertTrue(SandboxMimetypeHandler.get_thumbnail.called)

    def test_set_thumbnail(self):
        """Testing FileAttachment sandboxes MimetypeHandler.set_thumbnail"""
        self.spy_on(SandboxMimetypeHandler.set_thumbnail,
                    owner=SandboxMimetypeHandler)

        self.file_attachment.thumbnail = None
        self.assertTrue(SandboxMimetypeHandler.set_thumbnail.called)

    def test_get_icon_url(self):
        """Testing FileAttachment sandboxes MimetypeHandler.get_icon_url"""
        self.spy_on(SandboxMimetypeHandler.get_icon_url,
                    owner=SandboxMimetypeHandler)

        self.file_attachment.icon_url
        self.assertTrue(SandboxMimetypeHandler.get_icon_url.called)


class TextMimetypeTests(SpyAgency, TestCase):
    """Unit tests for reviewboard.attachments.mimetypes.TextMimetype."""

    fixtures = ['test_users']

    def setUp(self):
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            b'<p>This is a test</p>',
            content_type='text/plain')

        review_request = self.create_review_request(publish=True)

        form = UploadFileForm(review_request, files={
            'path': uploaded_file,
        })
        self.assertTrue(form.is_valid())

        self.file_attachment = form.create()

    def test_get_thumbnail_uncached_is_safe_text(self):
        """Testing TextMimetype.get_thumbnail string type is SafeText
        without cached thumbnail
        """
        thumbnail = self.file_attachment.thumbnail

        self.assertIsInstance(thumbnail, SafeText)

    def test_get_thumbnail_cached_is_safe_text(self):
        """Testing TextMimetype.get_thumbnail string type is SafeText with
        cached thumbnail
        """
        # Django's in-memory cache won't mangle the string types, so we can't
        # rely on just calling thumbnail twice. We have to fake it, so that
        # that we simulate the real-world behavior of getting a raw string
        # back out of a real cache.
        self.spy_on(self.file_attachment.mimetype_handler._generate_thumbnail,
                    call_fake=lambda self: '<div>My thumbnail</div>')

        thumbnail = self.file_attachment.thumbnail

        self.assertIsInstance(thumbnail, SafeText)

    def test_get_raw_thumbnail_image_url(self) -> None:
        """Testing TextMimetype.test_get_raw_thumbnail_image_url"""
        mimetype_handler = self.file_attachment.mimetype_handler
        assert mimetype_handler

        message = (
            'TextMimetype does not support generating thumbnail images.'
        )

        with self.assertRaisesMessage(NotImplementedError, message):
            mimetype_handler.get_raw_thumbnail_image_url(width=300)


class ImageMimetypeTests(SpyAgency, BaseFileAttachmentTestCase):
    """Unit tests for reviewboard.attachments.mimetypes.ImageMimetype.

    Version Added:
        6.0
    """

    fixtures = ['test_scmtools', 'test_users']

    def setUp(self) -> None:
        """Set up the test case."""
        image_file = self.make_uploaded_file()

        review_request = self.create_review_request(publish=True)

        form = UploadFileForm(review_request, files={
            'path': image_file,
        })
        self.assertTrue(form.is_valid())

        self.file_attachment = form.create()

    def test_get_thumbnail(self) -> None:
        """Testing ImageMimetype.get_thumbnail"""
        file = self.file_attachment.file
        storage = file.storage
        filename_base = os.path.splitext(file.name)[0]
        download_url = 'http://example.com/r/1/file/1/download/?thumbnail=1'

        self.assertHTMLEqual(
            self.file_attachment.thumbnail,
            f'<div class="file-thumbnail">'
            f'<img src="{download_url}&width=300"'
            f' srcset="{download_url}&width=300 1x,'
            f' {download_url}&width=600 2x, {download_url}&width=900 3x"'
            f'alt="" width="300" />'
            f'</div>')

        # These shouldn't exist until the URLs are accessed.
        self.assertFalse(storage.exists(f'{filename_base}_300.png'))
        self.assertFalse(storage.exists(f'{filename_base}_600.png'))
        self.assertFalse(storage.exists(f'{filename_base}_900.png'))

    def test_get_raw_thumbnail_image_url(self) -> None:
        """Testing ImageMimetype.get_raw_thumbnail_image_url"""
        file = self.file_attachment.file
        storage = file.storage
        filename_base = os.path.splitext(file.name)[0]

        mimetype_handler = self.file_attachment.mimetype_handler
        assert mimetype_handler

        filename = mimetype_handler.get_raw_thumbnail_image_url(width=300)
        self.assertTrue(filename)
        self.assertTrue(storage.exists(f'{filename_base}_300.png'))

    def test_generate_thumbnail_image_with_create_if_missing_false(
        self,
    ) -> None:
        """Testing ImageMimetype.get_raw_thumbnail_image_url with
        create_if_missing=False
        """
        file = self.file_attachment.file
        storage = file.storage
        filename_base = os.path.splitext(file.name)[0]

        mimetype_handler = self.file_attachment.mimetype_handler
        assert mimetype_handler

        filename = mimetype_handler.generate_thumbnail_image(
            width=300,
            create_if_missing=False)

        self.assertIsNone(filename)
        self.assertFalse(storage.exists(f'{filename_base}_300.png'))

    def test_delete_associated_files(self) -> None:
        """Testing ImageMimetype.delete_associated_files"""
        file = self.file_attachment.file
        storage = file.storage

        mimetype_handler = self.file_attachment.mimetype_handler
        assert mimetype_handler

        filename_base = os.path.splitext(file.name)[0]
        filename_300 = f'{filename_base}_300.png'
        filename_600 = f'{filename_base}_600.png'

        mimetype_handler.generate_thumbnail_image(width=300)
        mimetype_handler.generate_thumbnail_image(width=600)

        self.assertTrue(storage.exists(filename_300))
        self.assertTrue(storage.exists(filename_600))

        mimetype_handler.delete_associated_files()

        self.assertFalse(storage.exists(filename_300))
        self.assertFalse(storage.exists(filename_600))

        self.spy_on(storage.delete)
        self.spy_on(mimetypes_logger.warning)

        # A second call shouldn't do anything, outside of checking thumbnail
        # existence.
        mimetype_handler.delete_associated_files()

        self.assertSpyNotCalled(storage.delete)
