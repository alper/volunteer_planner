# coding=utf-8

import itertools
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.utils.safestring import mark_safe
from django.templatetags.l10n import localize
from scheduler.models import Shift
from news.models import NewsEntry
from google_tools.templatetags.google_links import google_maps_directions
from .models import Facility

class FacilityView(DetailView):
    template_name = 'facility.html'
    model = Facility

    def get_context_data(self, **kwargs):
        context = super(FacilityView, self).get_context_data(**kwargs)
        shifts = Shift.objects.filter(facility_id=self.object.pk)
        context['facility'] = get_facility_details(self.object, shifts)
        return context

def get_facility_details(facility, shifts):
    address_line = facility.address_line if facility.address else None
    shifts_by_date = itertools.groupby(shifts, lambda s: s.starting_time.date())
    return {
        'name': facility.name,
        'news': _serialize_news(NewsEntry.objects.filter(facility=facility)),
        'address_line': address_line,
        'contact_info': facility.contact_info,
        'google_maps_link': google_maps_directions(
            address_line) if address_line else None,
        'description': mark_safe(facility.description),
        'area_slug': facility.place.area.slug,
        'shifts': [{
                       'date_string': localize(shift_date),
                       'link': reverse('planner_by_facility', kwargs={
                           'pk': facility.pk,
                           'year': shift_date.year,
                           'month': shift_date.month,
                           'day': shift_date.day,
                       })
                   } for shift_date, shifts_of_day in shifts_by_date]
    }

def _serialize_news(news_entries):
    return [dict(title=news_entry.title,
                 date=news_entry.creation_date,
                 text=news_entry.text) for news_entry in news_entries]
