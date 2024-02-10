from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.html import escape
from .forms import ImportForm
from io import TextIOWrapper
from datetime import datetime
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
                    if len(row) == 7:  # Ensure that the row has the expected number of columns
                        # Convert Unix timestamp to datetime
                        unix_timestamp = int(row[6])
                        ping_time = datetime.utcfromtimestamp(unix_timestamp)

                        # Calculate the sum of values in columns 1 to 5
                        sum_values = sum(int(value) for value in row[1:6] if value.isdigit())

                        # Set ping_status based on the sum
                        ping_status = 1 if sum_values >= 1 else 0

                        # Create PingData object and save to the database
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
                # Handle any exceptions or errors that may occur during the upload process
                error_message = f"Upload failed: {str(e)}"
        else:
            error_message = "Form is not valid. Please check your file and try again."

    else:
        form = ImportForm()

    return render(request, 'pingswitch/upload_data.html', {'form': form, 'error_message': error_message})

    