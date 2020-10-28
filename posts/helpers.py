from django.core.exceptions import ValidationError
from os.path import splitext
from datetime import datetime


def valid_extension(value):
    file_name,extension = splitext(value.name)
    if extension.lower() not in('.png','.jpeg','.jpg'):
        raise ValidationError("Solo se permite archivos: png, jpg, jpeg")

def cover_name(instance, filename):
    datestamp = datetime.now()
    if instance.id:
        post = instance.id    
    else:
        post = "post"
    nameFinal = "%s_%s_%s_%s_%s_%s_%s" % (datestamp.year, datestamp.month, datestamp.day,datestamp.hour,datestamp.minute,datestamp.second, datestamp.microsecond)
    file_name,extension = splitext(filename)
    nameFinal = nameFinal + str(extension)
    return 'covers/{}/{}'.format(post,nameFinal)


def photo_profile_name(instance, filename):
    datestamp = datetime.now()
    if instance.id:
        user = instance.id    
    else:
        user = instance.name
    nameFinal = "%s_%s_%s_%s_%s_%s_%s" % (datestamp.year, datestamp.month, datestamp.day,datestamp.hour,datestamp.minute,datestamp.second, datestamp.microsecond)
    file_name,extension = splitext(filename)
    nameFinal = nameFinal + str(extension)
    return 'covers/{}/{}'.format(user,nameFinal)



