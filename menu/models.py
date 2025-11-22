from django.db import models

class MenuItem(models.Model):
    name = models.CharField('Название меню', max_length=50)
    title = models.CharField('Название пункта', max_length=100)
    parent = models.ForeignKey(
        'self', 
        verbose_name='Родитель', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    url = models.CharField('Ссылка (явная)', max_length=255, blank=True)
    named_url = models.CharField('Named URL', max_length=255, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'