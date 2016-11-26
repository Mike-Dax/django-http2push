# django-http2push
Cloudflare supports sending Link headers to http2 push files direct to clients. This little app helps you do that in a less painful way with your django app.

## Installation

 - Download this repo, put the http2push app in your django app directory. 
 - Throw `http2push` in your installed apps in your settings file.
 - Set up cloudflare.

## Usage

In your template, instead of loading `static`, load `pushstatic` (or load both if you don't want to push everything). Throw this up the top of your template:

```
{% load pushstatic %}
```

When you need to include a file, simply call the pushstatic tag:

```
<script src="{% pushstatic 'js/project.js' %}"></script>
```

Then in your view simply attach the `pushstatic` decorator:

```
from django.shortcuts import render
from http2push.decorators import pushstatic

@pushstatic()
def home(request):
    return render(request, 'pages/home.html')
```

If you want to push files that aren't specified in the template, you can use the `push` decorator on your view:

```
from django.shortcuts import render
from http2push.decorators import push

@push(['css/project.css', 'js/project.js'])
def home(request):
    return render(request, 'pages/home.html')

```

## How it works.

The template tags call the regular `static` function, grabbing the url and resolving the extension to the type required. This data is stored in `request.META.link_entries`.

The `pushstatic` decorator takes those entries and spits out a Link header that contains all the entries formatted correctly.


## Filetypes supported

If there's one missing, feel free to make a pull request.

```
lookup_extension = {
    '.css': 'style',
    '.js': 'script',
    '.png': 'image',
    '.jpg': 'image',
    '.svg': 'image',
    '.woff2': 'font',
    '.woff': 'font',
    '.eot': 'font',
    '.ttf': 'font'
}
```