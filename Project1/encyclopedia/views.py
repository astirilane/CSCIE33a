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
    # POST reqeust display
    # Pull search query and find it among the entries to display
    if request.method == "POST":
        search = request.POST['q']
        # Show entry data, and convert markdown syntax to HTML
        return render(request, "encyclopedia/entry_data.html", {
            "entry_data": markdown2.markdown(util.get_entry(search)),
            "entry": search
        })
    # GET request display
    # Display list of all entries
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


# Display searched wiki entry via direct / entry in URL bar
def entry_view(request, entry):
    # If there's no entry on this path then display error
    if not util.get_entry(entry):
        return render(request, "encyclopedia/error.html")
    # Otherwise display the entry from the path
    else:
        return render(request, "encyclopedia/entry_data.html", {
            "entry_data": markdown2.markdown(util.get_entry(entry)),
            "entry": entry
    })


# Add a new wiki entry 
def new_entry(request):
    # POST request display
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
    # GET request display
    # Show form for new wiki entry
    else:
        return render(request, "encyclopedia/new_entry.html", {
            "form": NewEntryForm
        })