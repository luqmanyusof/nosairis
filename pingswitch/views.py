from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.html import escape
from .forms import ImportForm, PingDataFilterForm
from io import TextIOWrapper
from datetime import datetime
from datetime import timedelta
from .models import PingData
import csv

def index(request):
    return render(request, 'pingswitch/index.html', {'text': 'here is the text of context'})

def dev(request):
    print('simple console log');
    return HttpResponse('Dev by Luqman Yusof')

def register(request):
    return HttpResponse(escape(repr(request.POST)))

def display_ping_data(request):
    ping_data_list = PingData.objects.all()
    return render(request, 'pingswitch/ping_data_display.html', {'ping_data_list': ping_data_list})

def ping_data_filter(request):
    print(request.GET);
    form = PingDataFilterForm(request.GET)
    queryset = PingData.objects.filter(ping_status='0')


    if form.is_valid():
        print('valid form')
        switch_label_param = request.GET.get('switch_label')
        ping_status_param = request.GET.get('ping_status')

        print(switch_label_param);

        queryset = PingData.objects.filter(switch_label=switch_label_param, ping_status=ping_status_param);
    else:
        error_message = form.errors.as_json()  # Or use as_text() to get as plain text
        return HttpResponse(f'Form is not valid, errors are: {error_message}')
    
    return render(request, 'pingswitch/ping_data_filter.html', {'form': form, 'ping_data_filter': queryset})

def upload_csv(request):
    error_message = None

    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            # return HttpResponse('valid')
            print('valid form');

            try:
                csv_file = request.FILES['ping_file']
                csv_reader = csv.reader(TextIOWrapper(csv_file.file, 'utf-8'))

                # Skip the header row
                next(csv_reader)

                for row in csv_reader:
                    if len(row) == 7:  
                        unix_timestamp = int(row[6])
                        ping_time = datetime.utcfromtimestamp(unix_timestamp)


                        sum_values = sum(int(value) for value in row[1:6] if value.isdigit())
                        ping_status = 1 if sum_values >= 1 else 0

                        PingData.objects.create(
                            switch_label=row[0],
                            t1=int(row[1]),
                            t2=int(row[2]),
                            t3=int(row[3]),
                            t4=int(row[4]),
                            t5=int(row[5]),
                            ping_time=ping_time,
                            ping_status=ping_status
                        )
                    else:
                        raise ValueError("Invalid number of columns in the CSV row")
                return HttpResponse('data has been loaded');
                
            except Exception as e:
                error_message = f"Upload failed: {str(e)}"
        else:
            error_message = "Form is not valid. Please check your file and try again."

    else:
        form = ImportForm()

    return render(request, 'pingswitch/upload_data.html', {'form': form, 'error_message': error_message})

def graph(request):

    s1_latest_ping_time = PingData.objects.filter(switch_label='S1').latest('ping_time').ping_time
    s2_latest_ping_time = PingData.objects.filter(switch_label='S2').latest('ping_time').ping_time
    s3_latest_ping_time = PingData.objects.filter(switch_label='S3').latest('ping_time').ping_time

    s1_twelve_hours_before_latest = s1_latest_ping_time - timedelta(hours=12)
    s2_twelve_hours_before_latest = s2_latest_ping_time - timedelta(hours=12)
    s3_twelve_hours_before_latest = s3_latest_ping_time - timedelta(hours=12)

    s1DataSet = PingData.objects.filter(switch_label='S1', ping_time__gte=s1_twelve_hours_before_latest).values('ping_time','ping_status').order_by('ping_time')
    s2DataSet = PingData.objects.filter(switch_label='S2', ping_time__gte=s2_twelve_hours_before_latest).values('ping_time','ping_status').order_by('ping_time')
    s3DataSet = PingData.objects.filter(switch_label='S3', ping_time__gte=s3_twelve_hours_before_latest).values('ping_time','ping_status').order_by('ping_time')

    s1_times = [str(data['ping_time']) for data in s1DataSet]
    s1_statuses = [data['ping_status'] for data in s1DataSet]

    s2_times = [str(data['ping_time']) for data in s2DataSet]
    s2_statuses = [data['ping_status'] for data in s2DataSet]

    s3_times = [str(data['ping_time']) for data in s3DataSet]
    s3_statuses = [data['ping_status'] for data in s3DataSet]

    context = {
        's1_times': s1_times,
        's1_statuses': s1_statuses,
        's2_times': s2_times,
        's2_statuses': s2_statuses,
        's3_times': s3_times,
        's3_statuses': s3_statuses
    }

    return render(request, 'pingswitch/graph.html', context)

def report(request):
    queryset = PingData.objects.filter(ping_status=0);
    return render(request, 'pingswitch/report.html', {'ping_data_filter': queryset})