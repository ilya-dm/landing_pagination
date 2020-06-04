from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()
request_lst =list()

def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing

    show = request.GET.get('from-landing')
    # request_lst.append(a)
    # for word in request_lst:
    counter_click[show] += 1
    print(counter_click)
    return render_to_response('index.html')
def name_view(request):
    Name = request.GET.get('name', 'Аноним')
    return HttpResponse(f'Привет, {Name}')


def landing(request):
    version = request.GET.get('ab-test-arg', 'original')
    counter_show[version] += 1
    print(counter_show)
    if version == 'original':
        return render_to_response('landing.html')
    else:
        return render_to_response('landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    return render_to_response('stats.html', context={
        'test_conversion': counter_click['test']/counter_show['test'],
        'original_conversion': counter_click['original']/counter_show['original'],
    })
