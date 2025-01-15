from django.urls import path, register_converter
from django.utils.dateparse import parse_datetime
from . import views
# Custom datetime converter
from django.utils.dateparse import parse_datetime

class DateTimeConverter:
    # Regex to match ISO 8601 datetime strings, including optional milliseconds and time zone
    regex = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?([+-]\d{2}:\d{2}|Z)?'

    def to_python(self, value):
        # Convert the string to a datetime object
        return parse_datetime(value)

    def to_url(self, value):
        # Ensure the value is an ISO 8601 string
        if isinstance(value, str):
            return value  # If already a string, return it
        return value.isoformat()  # Convert datetime to ISO 8601 string

# Register the custom converter
register_converter(DateTimeConverter, 'datetime')
 # Generates '/client/client-upload/'
urlpatterns = [
    path('home/', views.client_dashboard, name="home"),
    # path('create-report', views.create_report, name="create-report"),
    # path('amphures/', views.amphures, name='amphures'),
    # path('summary-data/', views.summary_data, name='summary-data'),
    # path('client-upload/', views.upload_file, name="client-upload"),
    path('add-location/', views.add_location, name="add-location"),
    path('user-locations/', views.user_locations, name='user-locations'),
    path('location-analysis/', views.location_analysis, name='location-analysis'),
    path('load-amphures/', views.load_amphures, name='load-amphures'),
    path('load-tambons/', views.load_tambons, name='load-tambons'),
    path('edit-location/<datetime:pk>/', views.edit_location, name='edit-location'),
    path('delete-location/<datetime:pk>/', views.delete_location, name='delete-location'),
    path('analytics-location/<datetime:pk>/', views.analytics_location, name='analytics-location'),
    path('display-dataframe/', views.display_dataframe, name='display-dataframe'),
    path('cost-ev/',views.calcostev,name='cost-ev'),
    path('cost-ev-dc/',views.cost_dc,name='cost_dc'),
    path('payback/',views.payback,name='payback'),
    path('payment/<int:payment_id>/', views.payment_page, name='payment_page'),
    path('create_qrcode/<int:payment_id>', views.create_qrcode, name='create_qrcode'),
    path('pay', views.payment, name='payment'),
]