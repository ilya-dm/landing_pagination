import csv
import pprint

from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect, HttpResponse
from django.urls import reverse


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    data = list()
    current_page = int(request.GET.get('page', 1))
    with open('data-398-2018-08-30.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for line in reader:
            data.append({x:line[x] for x in ["Name", "Street", "District"]})
    paginator = Paginator(data, 10)
    b_stations = paginator.get_page(current_page)
    next_page_url = current_page
    prev_page_url = current_page
    if b_stations.has_next():
        next_page_url = b_stations.next_page_number()
    if b_stations.has_previous():
        prev_page_url = b_stations.previous_page_number()
    return render_to_response('index.html', context={
         'bus_stations': b_stations,
        'current_page': current_page,
        'prev_page_url': f"{reverse(bus_stations)}?page={prev_page_url}",
        'next_page_url': f"{reverse(bus_stations)}?page={next_page_url}",
    })


def pagi_view(request):
    data = list()
    with open('data-398-2018-08-30.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for line in reader:
            data.append(line)
    page = int(request.GET.get('page'))
    name = [i['Name'] for i in data]
    street = [i['Street'] for i in data]
    district = [i['District'] for i in data]
    paginator = Paginator(name, 10)
    msg = '<br/>'.join(paginator.get_page(page))
    return HttpResponse(msg)