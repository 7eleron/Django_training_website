from django.db import models


# Create your models here.
class CmsSlider(models.Model):
    cms_img = models.ImageField(upload_to='sliderimg/')
    cms_titel = models.CharField(max_length=200, verbose_name='Заголовок')
    cms_text = models.CharField(max_length=200, verbose_name='Текст')
    cms_css = models.CharField(max_length=200, null=True, default='-', verbose_name='CSS klass')
    cms_css = models.CharField(max_length=200, null=True, default='-', verbose_name='CSS klass')

    def __str__(self):
        return self.cms_titel

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'