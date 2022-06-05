from .models import *


class HeaderView(object):
    def get_context_data(self, **kwargs):
        context = super(HeaderView, self).get_context_data(**kwargs)
        genders = Sex.objects.all()
        categories = Category.objects.all()
        context.update({
            'genders': genders,
            'categories': categories,
        })
        return context
