from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from django.utils.six import BytesIO  
from PIL import Image  
from members.models import Member


faker = Faker()


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'admin@admin.com', 'password')


    def test_post_should_return_unauthorized(self):
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 302)


    def test_post_form_should_be_loaded(self):
        self.client.login(username='admin', password='password')
        self.assertTrue(self.user.is_authenticated())
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 200)


    def test_post_should_not_be_created(self):
        self.client.login(username='admin', password='password')
        self.assertTrue(self.user.is_authenticated())
        response = self.client.post(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 400)    


    # def test_post_should_be_created(self):
    #     self.client.login(username='admin', password='password')
    #     self.assertTrue(self.user.is_authenticated())
    #     avatar = create_image(None, 'mediafiles/thumb.png')
    #     thumbnail = SimpleUploadedFile('thumb.png', avatar.getvalue())
    #     post = {
    #         'text_call': faker.sentence(),
    #         'title': faker.sentence(),
    #         'author': self.user.id,
    #         'text_content': faker.text(),
    #         'thumbnail': thumbnail
    #     }
    #     response = self.client.post(reverse('blog.add_post'), post)
    #     self.assertEqual(response.status_code, 200)
