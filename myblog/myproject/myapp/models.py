from django.db import models
from django.contrib.auth.models import User


class BlogManager(models.Manager):
    def top_3_most_viewed(self):
        return self.order_by("-views")[:3]

    def filter_by_category(self, category):
        return self.filter(category=category)


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ("food", "Еда"),
        ("life", "Жизнь"),
        ("sport", "Спорт"),
        ("travel", "Путешествия"),
        ("hobby", "Хобби"),
        ("stars", "Звезды"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    body = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="life")
    likes = models.ManyToManyField(User, related_name="blog_likes", blank=True)
    views = models.PositiveIntegerField(default=0)

    objects = BlogManager()

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def increment_views(self):
        self.views += 1
        self.save()


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author} к {self.blog}"
