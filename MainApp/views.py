import json
import os
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core.files import File
from .models import CSVUpload

# Create your views here.
def index(request):
    upload = {}
    dict_data = {}
    num =0
    if request.method == 'POST':
        try:
            csv_file = request.FILES.get('csv_file')
            timeframe = request.POST.get('timeframe')

            fs = FileSystemStorage()
            filename = fs.save('csv/'+csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)

            # read csv file
            pd.options.display.max_rows = int(timeframe)
            data = pd.read_csv(csv_file)
            
            # Create a DataFrame
            # data = data[['BANKNIFTY','DATE','TIME','OPEN','HIGH','LOW','CLOSE','VOLUME']]
            data = pd.DataFrame(data, index=[i for i in (0, int(timeframe)-1) ] , columns=['BANKNIFTY','DATE','TIME','OPEN','HIGH','LOW','CLOSE','VOLUME'])
            data = pd.DataFrame(data, dtype=object)
            data['HIGH'] = pd.to_numeric(data.HIGH)
            dict_data = {
                'BANKNIFTY':str(data['BANKNIFTY'].iloc[0]),
                'DATE':str(data['DATE'].iloc[0]),
                'TIME':str(data['TIME'].iloc[0]),
                'OPEN':data.OPEN.iloc[0],
                'HIGH':data.HIGH.max(),
                'LOW':data.LOW.min(),
                'CLOSE':data.CLOSE.iloc[-1],
                'VOLUME':data.VOLUME.iloc[-1]
                }
            
            # save json file
            json_file_path = 'media/json_output/'+str(os.path.splitext(csv_file.name)[0])+'.json'
            save_file = open(json_file_path, "w")
            json.dump(dict_data, save_file, indent = 4)
            save_file.close()
            

            upload = CSVUpload.objects.create(
                csv_file=uploaded_file_url,
                timeframe=timeframe,
                json_file=json_file_path
            )
            num=pd.options.display.max_rows
        except Exception as e:
            messages.error(request,"Unable to upload file. "+repr(e))
    return render(request, 'MainApp/index.html', {'data':dict_data, 'num':num, 'upload': upload})