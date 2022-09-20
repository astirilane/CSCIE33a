from pickle import NONE
from django.shortcuts import render
import markdown2
from django.template import RequestContext
from django import forms

from . import util


# Create new entry form class for wiki entries
class NewEntryForm(forms.Form):
    name = forms.CharField(label="New Entry Title")
    entry_info = forms.CharField(widget=forms.Textarea, label="Wiki Entry Data")


# Index display page and search
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


# Display searched wiki entry
def entry_view(request, entry):
    if not util.get_entry(entry):
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry_data.html", {
            "entry_data": markdown2.markdown(util.get_entry(entry)),
            "entry": entry
    })


# Add a new wiki entry 
def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            entry_info = form.cleaned_data["entry_info"]
            if util.get_entry(name):
                dupe = True
                return render(request, "encyclopedia/error.html", {
                    "dupe": dupe
                })
            else:
                util.save_entry(name, entry_info)
                return render(request, "encyclopedia/entry_data.html", {
                    "entry_data": markdown2.markdown(util.get_entry(name)),
                    "entry": name
                })
        else:
            return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/new_entry.html", {
            "form": NewEntryForm
        })