from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET
from core.models import Province, Amphure, Tambon
from django.contrib import messages
import logging
from account.models import LocationData
from .forms import LocationDataForm

import pandas as pd
from django_pandas.io import read_frame
from .data_models.utils import get_lat_lon_geopy  # Assuming you placed the function in utils.py



logger = logging.getLogger(__name__)
@login_required(login_url='login')
def client_dashboard(request):
    
    return render(request, 'client/client-dashboard.html')


@login_required(login_url='login')
def create_report(request):
    provinces = Province.objects.all().order_by('name_en')  # Ordering for better UX
    
    province_id = request.GET.get('province')
    amphure_id = request.GET.get('amphure')

    province_selected = None
    amphure_selected = None

    if province_id:
        try:
            province = Province.objects.get(pk=province_id)
            province_selected = province.name_th
        except Province.DoesNotExist:
            pass
    
    if amphure_id:
        try:
            amphure = Amphure.objects.get(pk=amphure_id)
            amphure_selected = amphure.name_th
        except Amphure.DoesNotExist:
            pass

    context = {
        'provinces': provinces,
        'province_selected': province_selected,
        'amphure_selected': amphure_selected
    }

    return render(request, 'client/create-report.html', context)


@login_required(login_url='login')
@require_GET
def amphures(request):
    province_id = request.GET.get('province')
    btn_allow = 'disable'
    if not province_id:
        # Handle missing province parameter
        return render(request, 'client/partials/amphures.html', {'amphures': [], 'error': 'No province selected.'})
    
    try:
        province = Province.objects.get(pk=province_id)
        btn_allow = 'enable'
    except Province.DoesNotExist:
        # Handle invalid province ID
        btn_allow = 'disable'
        return render(request, 'client/partials/amphures.html', {'amphures': [], 'error': 'Invalid province selected.'})
    
    amphures = Amphure.objects.filter(province=province).order_by('name_th')
    
    context = {
        'amphures': amphures,
        'province': province.name_th # Pass province name for display
    
    }
    
    return render(request, 'client/partials/amphures.html', context)


# @login_required(login_url='login')
# @require_GET
# def summary_data(request):
#     province_id = request.GET.get('province')
#     amphure_id = request.GET.get('amphure')

#     logger.debug(f"Received amphure_id: {amphure_id}")
#     logger.debug(f"Received province_id: {province_id}")

#     if not province_id.isdigit() or not amphure_id.isdigit():
#         logger.error("Invalid amphure_id received")
#         # Add a warning message
#         messages.warning(request, "กรุณาเลือกอำเภอที่ถูกต้อง")  # "Please select a valid district"

#         # Redirect to the create report page
#         return redirect('/client/create-report') # Replace with the correct URL name
#         # return HttpResponseBadRequest("Invalid amphure_id")

#     else :
#         province_selected = None
#         amphure_selected = None

#         if province_id:
#             province = get_object_or_404(Province, pk=province_id)
#             # province = Province.objects.get(pk=province_id)
#             province_selected = province.name_th

#         if amphure_id:
#             amphure = get_object_or_404(Amphure, pk=amphure_id)
#             amphure_selected = amphure.name_th

#         context = {
#             'province_selected': province_selected,
#             'amphure_selected': amphure_selected
#         }

#         return render(request, 'client/create-report.html', context)

# @login_required(login_url='login')
# def upload_file(request):
#     if request.method == "POST":
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             return JsonResponse({"status": "success", "message": "File uploaded successfully!"})
#     else:
#         form = FileUploadForm()

#     return render(request, "client/client-upload.html", {"form": form})

@login_required(login_url='my-login')
def add_location(request):
    if request.method == 'POST':
        form = LocationDataForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user  # Assign the logged-in user
            location.save()
            messages.success(request, "Location data has been added successfully.")
            return redirect('location-analysis')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LocationDataForm()

    context = {'form': form}
    return render(request, 'client/add-location.html', context)


@login_required(login_url='login')  # Ensure only logged-in users can access
def user_locations(request):
    # Fetch all LocationData entries for the logged-in user
    locations = LocationData.objects.filter(user=request.user)
    context = {'locations': locations}
    return render(request, 'client/user-locations.html', context)



@login_required(login_url='login')
def location_analysis(request):
  
    # Pass the logged-in user to the form
    locations = LocationData.objects.filter(user=request.user)
    context = {'locations': locations}
    return render(request, 'client/location_analysis.html', context)


def load_amphures(request):
    province_id = request.GET.get('province')
    amphures = Amphure.objects.filter(province_id=province_id).order_by('name_th')
    return render(request, "client/amphure_option.html", {'amphures': amphures})

def load_tambons(request):
    # Retrieve the amphure ID from the GET parameters
    amphure_id = request.GET.get('amphure')

    # Query the Tambon model for the selected amphure
    tambons = Tambon.objects.filter(amphure_id=amphure_id).order_by('name_th')

    # Render the template with the list of tambons
    return render(request, "client/tambon_option.html", {'tambons': tambons})




@login_required(login_url='login')
def edit_location(request, pk):
    # Retrieve the location by date and user
    location = get_object_or_404(LocationData, date=pk, user=request.user)

    if request.method == 'POST':
        # Bind the form to the POST data
        form = LocationDataForm(request.POST, instance=location, user=request.user)
        if form.is_valid():
            form.save()  # Save the changes
            return redirect('user-locations')  # Redirect to the locations list
    else:
        # Prepopulate the form with the current location data
        form = LocationDataForm(instance=location, user=request.user)

    return render(request, 'client/edit_location.html', {'form': form, 'location': location})

@login_required(login_url='login')
def delete_location(request, pk):
    # `pk` will be a datetime object parsed by the converter
    location = get_object_or_404(LocationData, date=pk, user=request.user)  # Match on `date` field
    if request.method == 'POST':
        location.delete()
        return redirect('user-locations')  # Redirect after successful deletion
    return redirect('user-locations')  # Redirect if accessed via GET

@login_required(login_url='login')
def analytics_report(request):
    # Retrieve all locations for the logged-in user
    locations = LocationData.objects.filter(user=request.user)
    return render(request, 'client/analytics_report.html', {'locations': locations})


@login_required(login_url='login')
def analytics_location(request, pk):
    # Retrieve the location using the primary key (date)
    location = get_object_or_404(LocationData, date=pk, user=request.user)
    return render(request, 'client/analytics_location.html', {'location': location})


def display_dataframe(request):
    # Example DataFrame
    data = {
        'Date': ['2025-01-01', '2025-01-02', '2025-01-03'],
        'Province': ['Bangkok', 'Chiang Mai', 'Phuket'],
        'Amphure': ['Phra Nakhon', 'Mueang Chiang Mai', 'Mueang Phuket'],
        'Tambon': ['Wat Pho', 'Tambon San Sai', 'Tambon Patong'],
        'Latitude': [13.7467, 18.7883, 7.8804],
        'Longitude': [100.5018, 98.9853, 98.3923]
    }
    df = pd.DataFrame(data)
    
    # Convert DataFrame to HTML
    df_html = df.to_html(classes='table table-striped table-bordered table-hover', index=False)
    # df_html = df.to_html(classes='table table-striped', index=False)
    
    context = {
        'table': df_html
    }
    return render(request, 'analytics/display_dataframe.html', context)

# def start_task(request):
#     if request.method == 'POST':
#         # Start the long-running task
#         long_running_task.delay()
#         return JsonResponse({'status': 'Task started'})
#     return render(request, 'client/start_task.html')