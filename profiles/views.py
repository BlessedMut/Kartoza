import folium as folium
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    map1 = folium.Map(zoom_start=4, min_zoom=3, max_zoom=8,
                      attr='Mapbox attribution')
    icon = plugins.BeautifyIcon(icon="marker")

    folium.Marker(
        location=[location_details['latitude'], location_details['longitude']],
        popup=f"<img height='300' width='300' src='{{ user.profile.image.url }}'<br><p>Address: {location_details['address']}</p>"
              f"<br>Lon: {location_details['longitude']}<br>Lat: {location_details['latitude']}<br>"
              f"Last Update: {location_details['date_created']}").add_to(
        map1)

    map1 = map1._repr_html_()
    context = {
        'map1': map1, 'profile_data': location_details, 'title': 'Home'
    }

    return render(request, 'profiles/home/home.html', context)


@login_required
def all_profiles(request):
    location_details = list(
        Profile.objects.all().values('user__username', 'address', 'phone_number', 'location'))
    for i in range(len(location_details)):
        location_details[i]['longitude'] = location_details[i]['location'][0]
        location_details[i]['latitude'] = location_details[i]['location'][1]

    data_list, address_list = [], []
    for i in range(len(location_details)):
        data_list.append([location_details[i]['longitude'], location_details[i]['latitude']])
        address_list.append(location_details[i]['address'])

    map1 = folium.Map(location=[4.133, 22.450], zoom_start=4, min_zoom=2, max_zoom=8,
                      attr='Mapbox attribution')
    icon = plugins.BeautifyIcon(icon="marker")
    for i in range(0, len(data_list)):
        folium.Marker(
            location=[data_list[i][1], data_list[i][0]],
            popup=f"<p>Address: {address_list[i]}</p><a href="">**<button style='background-color:green;color:white;outline:none;'>Edit Profile</button></a>").add_to(
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
