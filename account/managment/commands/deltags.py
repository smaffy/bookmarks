# delete unused tags

from django.core.management.base import BaseCommand, CommandError
from taggit.models import Tag


class Command2(BaseCommand):
    """
    Delete unused tags (tags without objects)
    """
    def remove_all_tags_without_objects(self, *args, **kwargs):
        for tag in Tag.objects.all():
            if tag.taggit_taggeditem_items.count() == 0:
                self.stdout.write('Removing: {}'.format(tag))
                tag.delete()
            else:
                self.stdout.write('Keeping: {}'.format(tag))

