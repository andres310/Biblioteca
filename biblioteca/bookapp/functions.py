from pathlib import Path

def handle_uploaded_file(f):
    route = Path('bookapp/static/upload')
    with open(route.joinpath(f.name), 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  