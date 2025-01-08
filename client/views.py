from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET
from core.models import Province, Amphure, Tambon
from client.models import Addon, DataCostElecAC , DataPriceAC
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

def calculate_ev_cost(data, post_data):
    # Retrieve values from the database
    priceHV = data.priceHV
    pricetr100 = data.pricetr100
    pricetr160 = data.pricetr160
    pricetr250 = data.pricetr250
    pricetr315 = data.pricetr315
    priceTRtoMDB = data.priceTRtoMDB
    priceMDBtoEV = data.priceMDBtoEV
    priceEV7 = data.priceEV7
    priceEV22 = data.priceEV22
    pricePackage = data.pricePackage

    # Debug: print retrieved data
    print(f"priceHV: {priceHV}, pricetr100: {pricetr100}, pricetr160: {pricetr160}, pricetr250: {pricetr250}")
    
    # Transformer price selection
    transformer_type = post_data.get('transformerType')
    transformer_prices = {
        "100": float(pricetr100),
        "160": float(pricetr160),
        "250": float(pricetr250),
        "315": float(pricetr315),
    }
    selected_price = transformer_prices.get(transformer_type, 0)

    # EV selection
    ev_type = post_data.get('evselection')
    ev_prices = {
        "7": float(priceEV7),
        "22": float(priceEV22),
    }
    selected_price_ev = ev_prices.get(ev_type, 0)

    # Package selection
    packageadd = post_data.get('packageselection')
    selected_price_package = float(pricePackage) if packageadd == "add" else 0

    # Distance-based cost calculations
    disthvtotr = post_data.get('disthvtotr', 0)
    priceHV_dis = priceHV * float(disthvtotr) if disthvtotr else 0

    distrtomdb = post_data.get('distrtomdb', 0)
    priceTRtoMDB_dis = priceTRtoMDB * float(distrtomdb) if distrtomdb else 0

    numev = int(post_data.get('numev', 0))
    distmdbtoev = post_data.get('distmdbtoev', 0)
    priceMDBtoEV_dis = priceMDBtoEV * float(distmdbtoev) if distmdbtoev else 0

    # Calculate the total cost
    costtotal = (
        selected_price + priceHV_dis + 
        numev * (selected_price_ev + selected_price_package) +
        priceMDBtoEV_dis + priceTRtoMDB_dis
    )

    # Debug: print final calculated cost
    print(f"Final EV cost calculated: {costtotal}")
    return costtotal


def calculate_addon_cost(data_addon, post_data):
    addon_total = 0
    for i in range(1, 16):
        addon_price_field = f"addon{i}"
        addon_quantity_field = f"addon{i}"

        # Get the price for the current add-on from the database
        price_addon = getattr(data_addon, addon_price_field, 0)

        # Get the user input quantity for the current add-on
        num_addon = int(post_data.get(addon_quantity_field, 0))

        # Calculate the total for the current add-on
        addon_total += price_addon * num_addon

    return addon_total

@login_required(login_url='login')
def calcostev(request):
    context = {"error": None, "costtotal": 0, "addon_total": 0, "costtotal_addon": 0}

    if request.method == "POST":
        try:

            # If 'submittotal' is pressed, calculate the total cost
            if 'submittotal' in request.POST:
                data = DataPriceAC.objects.first()
                data_addon = Addon.objects.first()

                context["costtotal"] = calculate_ev_cost(data, request.POST)
                context["addon_total"] = calculate_addon_cost(data_addon, request.POST)
                context["costtotal_addon"] = context["costtotal"] + context["addon_total"]
                print(f"Total (Cost + Addon): {context['costtotal_addon']}")

        except Exception as e:
            context["error"] = f"An error occurred: {str(e)}"

    # Debug: check final context values
    print(f"Final context: {context}")
    return render(request, 'client/cost_ev.html', context)

def payback(request):
    context = {"error": None, "payback_period": None}

    if request.method == "POST":
        data_price_elec = DataCostElecAC.objects.first()
        if not data_price_elec:
            context["error"] = "Electricity cost data is missing. Please contact the administrator."
            return render(request, 'client/payback.html', context)

        fee = data_price_elec.fee
        unitperhour = data_price_elec.unnitperhour
        dayserviceperyear = data_price_elec.dayserviceperyear
        price22onpeak = data_price_elec.price22onpeak
        priceless22onpeak = data_price_elec.priceless22onpeak
        price22offpeak = data_price_elec.price22offpeak
        priceless22offpeak = data_price_elec.priceless22offpeak
        try:
            # Retrieve form data
            cost_total = float(request.POST.get('cost_total', 0))
            volt_type = request.POST.get('volt_selection')
            
            # Store cost_total in context
            context["cost_total"] = cost_total
            
            # Define electricity costs
            eleccost_onpeak = {
                "22": float(price22onpeak),
                "less22": float(priceless22onpeak),
            }
            eleccost_offpeak = {
                "22": float(price22offpeak),
                "less22": float(priceless22offpeak),
            }

            # Get the appropriate electricity cost based on voltage type
            price_onpeak = eleccost_onpeak.get(volt_type, 0)
            price_offpeak = eleccost_offpeak.get(volt_type, 0)

            # Retrieve other form values
            price_charge = float(request.POST.get('price_charge', 0))
            hour_onpeak = float(request.POST.get('hours_onpeak', 0))
            hour_offpeak = float(request.POST.get('hours_offpeak', 0))

            # Calculate the total cost of electricity
            total_elec_cost = (hour_onpeak * price_onpeak) + (hour_offpeak * price_offpeak)
            print(total_elec_cost)
            # Add percentage fee (convert fee to decimal if needed)
            cost_fee = price_charge * fee
            print(cost_fee)

            # Operating costs (weekly usage for 7 days, 120 weeks in total)
            operating_costs = (((cost_fee +  price_onpeak)*hour_onpeak)+((cost_fee+ price_offpeak)*hour_offpeak)) * unitperhour * dayserviceperyear

            # Calculate income (revenue from charging over the same period)
            income = price_charge * (hour_onpeak + hour_offpeak) * unitperhour * dayserviceperyear

            # Calculate profit (net income)
            profit = income - operating_costs

            # Calculate payback period (time to recover initial cost)
            if profit > 0:
                total_months = cost_total / profit * 12  # Convert payback period to months
                years = int(total_months // 12)          # Whole years
                months = int(total_months % 12)          # Remaining months
                payback_period = f"{years} ปี {months} เดือน "
                context["payback_period"] = payback_period
            else:
                context["payback_period"] = "No payback possible (operating at a loss)"

            # Store results in context
            
            context["income"] = income
            context["profit"] = f"{profit:.2f}"
            context["operating_costs"] = f"{operating_costs:.2f}"

        except Exception as e:
            import traceback
            context["error"] = f"An error occurred: {str(e)}"
            print(traceback.format_exc())

    return render(request, 'client/payback.html', context)

