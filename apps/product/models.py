from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from apps.account.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    order = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Category'
        ordering = ('order', 'id')

    def get_parents(self):
        parents = [self]
        category = self
        while category.parent:
            parents.append(category.parent)
            category = category.parent
            print(parents)
        return parents

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    views = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def average_rank(self):
        try:
            return sum(self.ranks.values_list('rank', flat=True))/self.ranks.count() or 0
        except ZeroDivisionError:
            return 0

    @property
    def get_like_count(self):
        return self.likes.count()

    @property
    def get_quantity(self) -> int:
        incomes = sum(self.trades.filter(action=1).values_list('quantity', flat=True))
        outcomes = sum(self.trades.filter(action=2).values_list('quantity', flat=True))
        return incomes - outcomes

    @property
    def is_available(self) -> bool:
        return self.get_quantity() > 0



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='images')
    image = models.ImageField(upload_to='product/')

    def __str__(self):
        return self.product.name


class Trade(models.Model):
    ACTION = (
        (1, _('Income')),
        (2, _('Outcome'))
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='trades')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.PositiveSmallIntegerField(choices=ACTION, default=1)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        incomes = Trade.objects.filter(product_id=self.product_id, action=1).count()
        outcomes = Trade.objects.filter(product_id=self.product_id, action=2).count()
        if incomes < outcomes:
            raise ValidationError(_('Outcomes cannnot be greater than Incomes'))
        super().save_base(force_insert=False, force_update=False, using=None, update_fields=None)


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='wishlist')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product.name


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product.name


class Rank(models.Model):
    RANK_CHOICES = ((r, r) for r in range(1,11))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='ranks')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rank = models.PositiveSmallIntegerField(default=0, choices=RANK_CHOICES, db_index=True)

    def __str__(self):
        return self.product.name

    def children(self):
        return Comment.objects.filter(top_level_comment_id=self.id)


class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    top_level_comment_id = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} ({self.product.id}-->{self.id})'

    @property
    def children(self):
        return Comment.objects.filter(top_level_comment_=self.id)


class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, related_name='images')
    image = models.ImageField(upload_to='comments/%Y/%m/%d/')


def comment_pre_save(sender, instance, created, *args, **kwargs):
    if created:
        if not instance:
            instance.top_level_comment_id = instance.parent.top_level_comment_id
        else:
            instance.top_level_comment_id = instance.id
        instance.save()


post_save.connect(comment_pre_save, sender=Comment)


