from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(
        verbose_name='Имя на русском',
        max_length=200)
    title_en = models.CharField(
        verbose_name='Имя на английском',
        max_length=200, default="default title")
    title_jp = models.CharField(
        verbose_name='Имя на японском',
        max_length=200,
        default="default title")
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='pokemons',
        null=True)
    description = models.TextField(
        verbose_name='Описание',
        default="default description")
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name= 'Из кого эволюционировал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='next_evolutions')

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='Долгота')
    lon = models.FloatField(verbose_name='Широта')
    appeared_at = models.DateTimeField(verbose_name='Когда появился')
    disappeared_at = models.DateTimeField(verbose_name='Когда исчезнет')
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strength = models.IntegerField(verbose_name='Атака')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Выносливость')
    
    def __str__(self):
        return f'{self.pokemon}'