from django.shortcuts import render
import markdown2
from django.template import RequestContext

from . import util


def index(request):
    if request.method == "POST":
        search = request.POST['q']
        return render(request, "encyclopedia/entry_data.html", {
            "entry_data": markdown2.markdown(util.get_entry(search)),
            "entry": search
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry_view(request, entry):
    if not util.get_entry(entry):
        return render (request, "encyclopedia/not_found.html")
    else:
        return render(request, "encyclopedia/entry_data.html", {
            "entry_data": markdown2.markdown(util.get_entry(entry)),
            "entry": entry
    })


def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")