from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import os

class Pet(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    SIZE_CHOICES = [
        ('miniatura', 'Miniatura'),
        ('pequeno', 'Pequeno'),
        ('médio', 'Médio'),
        ('grande', 'Grande'),
    ]

    TYPE_CHOICES = [
        (1, 'cachorro'),
        (2, 'gato'),
        (3, 'outro'),
    ]

    BREED_CHOICES = [
        (1, 'SRD'),
        (2, 'akita'),
        (3, 'basset hound'),
        (4, 'beagle'),
        (5, 'bernese mountain dog'),
        (6, 'bichon frise'),
        (7, 'bloodhound'),
        (8, 'border collie'),
        (9, 'boston terrier'),
        (10, 'boxer'),
        (11, 'bulldog'),
        (12, 'cavalier king charles spaniel'),
        (13, 'chihuahua'),
        (14, 'chow chow'),
        (15, 'cocker spaniel'),
        (16, 'collie'),
        (17, 'corgi'),
        (18, 'dachshund'),
        (19, 'dalmatian'),
        (20, 'doberman'),
        (21, 'english mastiff'),
        (22, 'german shepherd'),
        (23, 'golden retriever'),
        (24, 'great dane'),
        (25, 'husky'),
        (26, 'irish setter'),
        (27, 'italian greyhound'),
        (28, 'jack russell terrier'),
        (29, 'labrador retriever'),
        (30, 'maltese'),
        (31, 'newfoundland'),
        (32, 'pomeranian'),
        (33, 'poodle'),
        (34, 'pug'),
        (35, 'rhodesian ridgeback'),
        (36, 'rottweiler'),
        (37, 'saint bernard'),
        (38, 'samoyed'),
        (39, 'shar pei'),
        (40, 'shiba inu'),
        (41, 'shih tzu'),
        (42, 'siberian husky'),
        (43, 'staffordshire bull terrier'),
        (44, 'vizsla'),
        (45, 'weimaraner'),
        (46, 'yorkshire terrier'),
        (47, 'australian shepherd'),
        (48, 'border terrier'),
        (49, 'brittany spaniel'),
        (50, 'cane corso'),
        (51, 'cavalier king charles spaniel'),
        (52, 'chinese crested'),
        (53, 'english bulldog'),
        (54, 'french bulldog'),
        (55, 'german shorthaired pointer'),
        (56, 'irish wolfhound'),
        (57, 'italian greyhound'),
        (58, 'japanese chin'),
        (59, 'keeshond'),
        (60, 'labrador retriever'),
        (61, 'maltese'),
        (62, 'newfoundland'),
        (63, 'norwegian elkhound'),
        (64, 'otterhound'),
        (65, 'papillon'),
        (66, 'pekingese'),
        (67, 'pomeranian'),
        (68, 'poodle'),
        (69, 'pug'),
        (70, 'redbone coonhound'),
        (71, 'rhodesian ridgeback'),
        (72, 'saluki'),
        (73, 'samoyed'),
        (74, 'schipperke'),
        (75, 'scottish deerhound'),
        (76, 'shiba inu'),
        (77, 'shihtzu'),
        (78, 'siberian husky'),
        (79, 'silky terrier'),
        (80, 'staffordshire bull terrier'),
        (81, 'tibetan mastiff'),
        (82, 'vizsla'),
        (83, 'weimaraner'),
        (84, 'whippet'),
        (85, 'yorkshire terrier'),
        (86, 'affenpinscher'),
        (87, 'airedale terrier'),
        (88, 'akita'),
        (89, 'alaskan malamute'),
        (90, 'american eskimo dog'),
        (91, 'american pit bull terrier'),
        (92, 'american staffordshire terrier'),
        (93, 'anatolian shepherd dog'),
        (94, 'australian cattle dog'),
        (95, 'australian shepherd'),
        (96, 'australian terrier'),
        (97, 'basenji'),
        (98, 'basset hound'),
        (99, 'beagle'),
        (100, 'bedlington terrier'),
    ]
    
    PERSONALITY_CHOICES = [
        (1, 'calmo'),
        (2, 'agitado'),
        (3, 'assustado'),
        (4, 'amoroso'),
        (5, 'enérgico'),
        (6, 'quieto'),
        (7, 'dócil'),
        (8, 'bravo'),
        (9, 'sociável'),
        (10, 'não sociável'),
    ]

    GET_ALONG_CHOICES = [
        (1, 'cachorros'),
        (2, 'gatos'),
        (3, 'crianças'),
    ]

    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age_year = models.IntegerField()
    age_month = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    breed = models.IntegerField(choices=BREED_CHOICES, default=1)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    personality = ArrayField(models.IntegerField(choices=PERSONALITY_CHOICES), default=list)
    get_along = ArrayField(models.IntegerField(choices=GET_ALONG_CHOICES), default=list)
    description = models.TextField()
    is_active = models.BooleanField(default=True)


class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pet_images/')
    order = models.IntegerField(default=0)
    custom_name = models.CharField(max_length=255, blank=True, null=True)

    def delete(self, *args, **kwargs):
        # Remove o arquivo de imagem associado
        if self.image:
            try:
                os.remove(self.image.path)
            except FileNotFoundError:
                pass  # Se o arquivo não existir, não há necessidade de removê-lo

        # Chama o método delete da classe pai para excluir a instância do modelo
        super(PetImage, self).delete(*args, **kwargs)