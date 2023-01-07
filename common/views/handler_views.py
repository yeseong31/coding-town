from django.shortcuts import render


def bad_request_page(request, exception):
    return render(request, 'errors/400.html', {})


def page_not_found_page(request, exception):
    return render(request, 'errors/404.html', {})


def server_error_page(request):
    return render(request, 'errors/500.html', {})
