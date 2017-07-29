from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from  comment.models import Comment
from django.contrib.contenttypes.models import ContentType


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # posts.objects.all() = return (PostManager, self).all() overiding the all() function
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length=200)
    # slug = models.SlugField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    image = models.FileField(null=True, blank=True, upload_to=upload_location)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})  # reverse is going to pass the id to url of named detail

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    class Meta:
        ordering = ['-create_date', ]


# def create_slug(instance, new_slug=None):
# 	slug = slugify(instance.title)
# 	if new_slug is not None:
# 		slug = new_slug
# 	qs = Posts.objects.filter(slug=slug).order_by("-id")
# 	exists = qs.exists()
# 	if exists:
# 		new_slug = "%s-%s" %(slug, qs.first().id)
# 		return create_slug(instance, new_slug=new_slug)
# 	return slug

# def pre_save_post_receiver(sender, instance, *args, **kwargs):
# 	if not instance.slug:
# 		instance.id = create_slug(instance)


# pre_save.connect(pre_save_post_receiver, sender=Posts)

class Demo(models.Model):
    title = models.CharField(max_length=200)
    # slug = models.SlugField(unique=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    # image = models.FileField(null=True, blank=True, upload_to=upload_location)
    content = models.TextField()

    # draft = models.BooleanField(default=False)
    # publish = models.DateField(auto_now=False,auto_now_add=False)
    # updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    # create_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __unicode__(self):
        return self.title
