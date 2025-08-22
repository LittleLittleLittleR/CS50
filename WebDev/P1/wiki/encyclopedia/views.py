from django.shortcuts import render
import markdown2
import random

from . import util

def md_to_html(content):
    return markdown2.markdown(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    
    content = md_to_html(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

def search(request):
    title = request.POST.get('q')
    if util.get_entry(title):
        return entry(request, title)
    else:
        title_lst = util.list_entries()
        search_lst = []
        for x in title_lst:
            if title.lower() in x.lower():
                search_lst.append(x)
        return render(request, "encyclopedia/search.html", {
        "entries": search_lst
        })
    
def new(request):
    return render(request, "encyclopedia/new.html", {
        "title_error":False
    })

def save_new(request):
    title = request.POST.get("title")
    content = request.POST.get("new_entry")
    if util.get_entry(title):
        return render(request, "encyclopedia/new.html", {
            "title_error":True
        })
    else:
        util.save_entry(title, content)
        return entry(request, title)

def edit(request, title):
    content = util.get_entry(title)
    content = '\n'.join([line.lstrip() for line in content.splitlines() if line.strip()])
    return render(request, "encyclopedia/edit.html", {
        "title":title,
        "content":content
    })

def save_edit(request):
    title = request.POST.get("title")
    content = request.POST.get("new_entry")
    util.save_entry(title, content)
    return entry(request, title)

def random_entry(request):
    title = random.choice(util.list_entries())
    return entry(request, title)