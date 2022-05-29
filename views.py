from django.shortcuts import render
from home import bestfew
from home import collab

# Create your views here.
def index(request):
    context={
        'var':"sdfdf",
        'var2':"sdfsf sdfsdfs sdfs"
    }
    return render(request, 'index.html')

def trending(request):
    d = bestfew.trend()
    context={
        "v1": str(d[0:1])[2:-2],
        "v2": str(d[1:2])[2:-2],
        "v3": str(d[2:3])[2:-2],
        "v4": str(d[3:4])[2:-2],
        "v5": str(d[4:5])[2:-2],
        "v6": str(d[5:6])[2:-2],
        "v7": str(d[6:7])[2:-2],
        "v8": str(d[7:8])[2:-2],
        "v9": str(d[8:9])[2:-2],
        "v10": str(d[9:10])[2:-2],
        "v11": str(d[10:11])[2:-2],
        "v12": str(d[11:12])[2:-2],
        "v13": str(d[12:13])[2:-2],
        "v14": str(d[13:14])[2:-2],
        "v15": str(d[14:15])[2:-2]
    }
    return render(request, 'trending.html', context)


def lastread(request):
    text = request.GET.get('text')
    if text:
         d = collab.final(text)
         #print(d)
         context = {
            "h": "Top 10 recommended books:-",
            "v1": str(d[0:1])[2:-2],
            "v2": str(d[1:2])[2:-2],
            "v3": str(d[2:3])[2:-2],
            "v4": str(d[3:4])[2:-2],
            "v5": str(d[4:5])[2:-2],
            "v6": str(d[5:6])[2:-2],
            "v7": str(d[6:7])[2:-2],
            "v8": str(d[7:8])[2:-2],
            "v9": str(d[8:9])[2:-2],
            "v10": str(d[9:10])[2:-2]
         }
    else:
        context = {
            "h": "",
            "v1": "",
            "v2": "",
            "v3": "",
            "v4": "",
            "v5": "",
            "v6": "",
            "v7": "",
            "v8": "",
            "v9": "",
            "v10": ""
        }

    return render(request, 'lastread.html',context)


