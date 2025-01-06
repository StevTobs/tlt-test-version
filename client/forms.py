from django import forms
from account.models import LocationData
from core.models import Province, Amphure, Tambon
import logging
from .data_models.utils import get_lat_lon_geopy  # Assuming you placed the function in utils.py

# Initialize logger
log = logging.getLogger(__name__)

# =============
# class LocationDataForm(forms.Form):

#     PROVINCE_CHOICES = [('', 'กรุณาเลือกจังหวัด')] + [(province.pk, province.name_th) for province in Province.objects.all().order_by('name_th')]

#     province = forms.ChoiceField(
#         choices=PROVINCE_CHOICES,
#         widget=forms.Select(attrs={'hx-get': "/client/load-amphures/", 'hx-target': '#id_amphure', 'class': 'form-select'}),
#         label="จังหวัด"
#     )

#     amphure = forms.ModelChoiceField(queryset=Amphure.objects.none(), 
#                                     empty_label="กรุณาเลือกอำเภอ" , 
#                                     label="อำเภอ",
#                                     widget=forms.Select(
#                                         attrs={'hx-get': "/client/load-tambons/", 
#                                             'hx-target': '#id_tambon', 
#                                                 'class': 'form-select'}),) 

#     tambon = forms.ModelChoiceField(queryset=Tambon.objects.none(), empty_label="กรุณาเลือกตำบล", label="ตำบล")
#     lat = forms.FloatField(widget=forms.HiddenInput(), label="Latitude")
#     lng = forms.FloatField(widget=forms.HiddenInput(), label="Longitude")

    
# =============


class LocationDataForm(forms.ModelForm):
        # PROVINCE_CHOICES = [('', 'กรุณาเลือกจังหวัด')] + [(province.pk, province.name_th) for province in Province.objects.all().order_by('name_th')]

    # lat_label = '-'
    # lng_label = '-'
    #  province = forms.ModelChoiceField(
    #     queryset=Province.objects.filter(deleted_at__isnull=True),
    #     widget=forms.Select(attrs={
    #         'hx-get': "/client/load-amphures/",
    #         'hx-target': '#id_amphure',
    #         'class': 'form-select'
    #         }),
    #     empty_label='กรุณาเลือกจังหวัด',
    #     to_field_name='id',
    #     label='Province'
    #     )

    province = forms.ModelChoiceField(
        queryset=Province.objects.filter(deleted_at__isnull=True),
        empty_label='กรุณาเลือกจังหวัด',
        widget=forms.Select(attrs={
            'hx-get': "/client/load-amphures/",
            'hx-target': '#id_amphure',
            'class': 'form-select'
        }),
        label="จังหวัด"
    )


    amphure = forms.ModelChoiceField(
        queryset=Amphure.objects.none(),
        empty_label="กรุณาเลือกอำเภอ",
        widget=forms.Select(attrs={
            'hx-get': "/client/load-tambons/",
            'hx-target': '#id_tambon',
            'class': 'form-select'
        }),
        label="อำเภอ"
    )

    tambon = forms.ModelChoiceField(
        queryset=Tambon.objects.none(),
        empty_label="กรุณาเลือกตำบล",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="ตำบล"
    )
    
    # Hidden Fields for Latitude and Longitude
    lat = forms.FloatField(widget=forms.HiddenInput(), label="Latitude", required=False)
    lng = forms.FloatField(widget=forms.HiddenInput(), label="Longitude", required=False)
    
    # if province!='' and amphure!='' and  tambon!='' :
    #     lat_label, lng_label = get_lat_lon_geopy(province, amphure, tambon)


 
    class Meta:
        
        model = LocationData
        fields = ['province', 'amphure', 'tambon', 'lat', 'lng']
        widgets = {
            'lat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'เว้นว่างไว้ กรณีไม่ทราบ' }),
            'lng': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'เว้นว่างไว้ กรณีไม่ทราบ'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from kwargs
        
        super().__init__(*args, **kwargs)

        # Prepopulate amphure and tambon dropdowns based on form data
        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['amphure'].queryset = Amphure.objects.filter(province_id=province_id).order_by('name_th')
            except (ValueError, TypeError):
                self.fields['amphure'].queryset = Amphure.objects.none()

        if 'amphure' in self.data:
            try:
                amphure_id = int(self.data.get('amphure'))
                self.fields['tambon'].queryset = Tambon.objects.filter(amphure_id=amphure_id).order_by('name_th')
            except (ValueError, TypeError):
                self.fields['tambon'].queryset = Tambon.objects.none()

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Assign the actual model instances to the ForeignKey fields
        instance.province = self.cleaned_data.get('province')
        instance.amphoe = self.cleaned_data.get('amphoe')
        instance.tambon = self.cleaned_data.get('tambon')

        # Compute latitude and longitude based on selected province, amphoe, and tambon
        if instance.province and instance.amphoe and instance.tambon:
            try:
                lat, lng = get_lat_lon_geopy(instance.province.name_th, instance.amphoe.name_th, instance.tambon.name_th)
                instance.lat = lat
                instance.lng = lng
            except Exception as e:
                log.error(f"Error fetching coordinates: {e}")
                raise forms.ValidationError(f"Could not retrieve coordinates: {e}")
        else:
            log.warning("Province, Amphoe, or Tambon not selected.")
            instance.lat = None
            instance.lng = None

        # Attach the logged-in user to the instance if applicable
        if self.user:
            instance.user = self.user

        if commit:
            instance.save()
        return instance
        instance = super().save(commit=False)

        # Retrieve the selected instances
        province_instance = self.cleaned_data.get('province')
        amphure_instance = self.cleaned_data.get('amphoe')
        tambon_instance = self.cleaned_data.get('tambon')

        # Assign the actual model instances to the ForeignKey fields
        instance.province = province_instance.name_th
        instance.amphoe = amphure_instance.name_th
        instance.tambon = tambon_instance.name_th

        # Compute latitude and longitude based on selected province, amphoe, and tambon
        if province_instance and amphure_instance and tambon_instance:
            lat, lon = get_lat_lon_geopy(province_instance.name_th, amphure_instance.name_th, tambon_instance.name_th)
            if lat and lon:
                instance.lat = lat
                instance.lng = lon
            else:
                log.warning(f"Could not retrieve coordinates for {province_instance.name_th}, {amphure_instance.name_th}, {tambon_instance.name_th}.")
                instance.lat = None
                instance.lng = None
        else:
            log.warning("Province, Amphoe, or Tambon not selected.")
            instance.lat = None
            instance.lng = None

        # Attach the logged-in user to the instance if applicable
        if self.user:
            instance.user = self.user  # Ensure the model has a 'user' field

        if commit:
            instance.save()
        return instance