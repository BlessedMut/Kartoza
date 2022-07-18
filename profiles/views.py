import folium as folium
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from folium import plugins

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile


def root(request):
    return render(request, 'profiles/index.html', {})


@login_required
def home(request):
    location_details = list(
        Profile.objects.filter(user=request.user).values())
    location_details = location_details[0]
    location_details['longitude'] = location_details['location'][0]
    location_details['latitude'] = location_details['location'][1]
    map1 = folium.Map(location=[-26.195246, 28.034088], zoom_start=10, min_zoom=3, max_zoom=18,
                      attr='Mapbox attribution', tiles="OpenStreetMap")
    icon = plugins.BeautifyIcon(icon="marker")

    folium.Marker(
        location=[location_details['latitude'], location_details['longitude']],
        popup=f"<img height='0' width='300'><h5 align='center'><strong><b>{request.user.first_name} {request.user.last_name}'s Profile</h5><p></b><hr>Address</strong>: {request.user.profile.address}</p>"
              f"<hr><strong>Coordinates</strong>: {location_details['latitude']} {location_details['longitude']}"
              f"<br><hr><strong>Phone Number</strong>: {request.user.profile.phone_number}"
              f"<br><hr><strong>Last Updated</strong>: {request.user.profile.date_created}").add_to(
        map1)

    map1 = map1._repr_html_()
    context = {
        'map1': map1, 'profile_data': location_details, 'title': 'Home'
    }

    return render(request, 'profiles/home/home.html', context)


@login_required
def all_profiles(request):
    location_details = list(
        Profile.objects.all().values())
    for i in range(len(location_details)):
        location_details[i]['longitude'] = location_details[i]['location'][0]
        location_details[i]['latitude'] = location_details[i]['location'][1]

    data_list, address_list, other = [], [], []
    for i in range(len(location_details)):
        other.append(
            [location_details[i]['phone_number'], location_details[i]['date_created'],
             User.objects.filter(pk=location_details[i]['user_id']).values()[0]['first_name'],
             User.objects.filter(pk=location_details[i]['user_id']).values()[0]['last_name']])
        data_list.append([location_details[i]['longitude'], location_details[i]['latitude']])
        address_list.append(location_details[i]['address'])

    map1 = folium.Map(location=[-26.195246, 28.034088], zoom_start=10, min_zoom=2, max_zoom=18,
                      attr='Mapbox attribution', tiles="OpenStreetMap")
    icon = plugins.BeautifyIcon(icon="marker")
    for i in range(0, len(data_list)):
        folium.Marker(
            location=[data_list[i][1], data_list[i][0]],
            popup=f"<img height='0' width='300'><h5 align='center'><strong><b>{other[i][2]} {other[i][3]}'s Profile</h5><p></b><hr>Address</strong>: {address_list[i]}</p>"
                  f"<hr><strong>Coordinates</strong>: {data_list[i][0]} {data_list[i][1]}"
                  f"<br><hr><strong>Phone Number</strong>: {other[i][0]}"
                  f"<br><hr><strong>Last Updated</strong>: {other[i][1]}").add_to(
            map1)

    map1 = map1._repr_html_()
    context = {
        'map1': map1,
    }
    return render(request, 'profiles/home/profiles.html', context)


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account updated successfully')
            return redirect('profiles-settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Profile',
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profiles/home/profile.html', context)
