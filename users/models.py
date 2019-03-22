from django.db import models
from registro.models import Finca
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        (1, 'Administrador'),
        (2, 'Trabajador'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trabaja_en = models.ForeignKey(Finca, on_delete=models.CASCADE, blank=True, null=True)
    rol = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)

    def __str__(self):
        return 'Perfil de {}'.format(self.user.username)

    #image = models.ImageField('imagen',default='/profile_pics/default.jpg', upload_to='profile_pics')
    #def save(self):
    #    super().save()
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)"""




