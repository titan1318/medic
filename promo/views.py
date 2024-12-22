
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from promo.forms import PromoForm
from promo.models import Promo


class PromoListView(ListView):
    model = Promo

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset


class PromoCreateView(PermissionRequiredMixin, CreateView):
    model = Promo
    form_class = PromoForm
    permission_required = 'promo.set_promo_active_status'
    success_url = reverse_lazy('promo:promos')


class PromoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Promo
    form_class = PromoForm
    permission_required = 'promo.set_promo_active_status'
    success_url = reverse_lazy('promo:promos')


class PromoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Promo
    permission_required = 'promo.set_promo_active_status'
    success_url = reverse_lazy('promo:promos')


@permission_required('promo.set_promo_active_status')
def toggle_active(request, pk):
    promo = Promo.objects.get(pk=pk)
    # Переключаем статус is_active
    promo.is_active = {promo.is_active: False,
                   not promo.is_active: True}[True]
    promo.save()
    return redirect(reverse('promo:promos'))

