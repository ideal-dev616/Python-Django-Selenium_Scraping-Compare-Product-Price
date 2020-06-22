from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from datetime import datetime
from django.db import connection
from django.http import JsonResponse

def get_category():
    posts = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT categ_main FROM tbl_category GROUP BY categ_main")
        for obj in cursor.fetchall():
            posts.append({"categ_main": obj[0]})
    return posts

def get_favourite_list(user_id):
    fav_list = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, list_name, user_id FROM tbl_list WHERE user_id = " + str(user_id))
        for obj in cursor.fetchall():
            fav_list.append({"list_id" : obj[0], "fav_list" : obj[1]})
    print(fav_list)
    return fav_list

def add_favourite_list(request):
    if request.method == 'GET':
        nlist = request.GET['list']
        cursor = connection.cursor()
        query = "select id from tbl_list where list_name = '"+ nlist +"'"
        cursor.execute(query)
        # result = cursor.fetchone()
    return JsonResponse({'data':"result"})

def get_data_by_categ(request):
    result = ''
    if request.method == 'GET':
        category = request.GET['category']
        idx = request.GET['idx']
        cursor = connection.cursor()
        query = ""
        if int(idx) == 1:
            query = "SELECT a.image, a.product, a.price, a.discount, b.supermarket, b.id FROM tbl_products AS a LEFT JOIN tbl_category AS b ON a.category = b.id WHERE b.categ_main = '" + category + "'"
        elif int(idx) == 2:
            query = "SELECT a.image, a.product, a.price, a.discount, b.supermarket, b.id FROM tbl_products AS a LEFT JOIN tbl_category AS b ON a.category = b.id WHERE b.categ_main LIKE '%" + category + "%' OR b.categ_branch LIKE '%" + category + "%' OR a.product LIKE '%" + category + "%'"
        elif int(idx) == 3:
            categ = category.split(",")
            query = "SELECT a.image, a.product, a.price, a.discount, b.supermarket, b.id FROM tbl_products AS a LEFT JOIN tbl_category AS b ON a.category = b.id WHERE (b.categ_main LIKE '%" + categ[0].strip() + "%' OR b.categ_branch LIKE '%" + categ[0].strip() + "%' OR a.product LIKE '%" + categ[0].strip() + "%')"
            for i in range(1, len(categ)):
                query += " AND (b.categ_main LIKE '%" + categ[i].strip() + "%' OR b.categ_branch LIKE '%" + categ[i].strip() + "%' OR a.product LIKE '%" + categ[i].strip() + "%')"
        query += "  LIMIT 10"
        cursor.execute(query)
        for item in cursor.fetchall():
            result += '<tr><td><img src="'+item[0]+'" width="110px" height="110px" alt="--Product--"></td>'
            result += '<td>'+item[1]+'</td>'
            result += '<td><div class="currentprice_decoration">'+item[2]+'</div></td>'
            result += '<td><div class="discount_decoration">'+item[3]+'</div></td>'
            result += '<td><img src="/static/logo/'+str(item[4])+'.png" width="150px" height="60px" alt="--Supermarket--"></td>'
            result += '<td><a href="#" id="add_to_favorite" value="'+str(item[5])+'"  data-toggle="modal" data-target="#m_modal_4"  class="btn btn-outline-danger m-btn m-btn--icon m-btn--icon-only m-btn--custom m-btn--pill" title="Add to favorite"><i class="la la-heart-o"></i></a>&nbsp;&nbsp;'
            result += '<a href="pages/comparison.html" id="go_to_product" value="'+item[1]+'" class="btn btn-outline-info m-btn m-btn--icon m-btn--icon-only m-btn--custom m-btn--pill" title="Compare the best price"><i class="la la-balance-scale"></i></a></td></tr>'
        return JsonResponse({'data':result})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        if (User.objects.filter(username=username).exists()):
            user = User.objects.filter(username=username)[0]
            if password == user.password:
                request.session['username'] = username
                login(request, user)
                return redirect("index")
            else:
                return render(request, 'login.html', {'login_success': 'no'})
    return render(request, 'login.html', {'login_success': ''})
    
@csrf_protect
def signuppage(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        date_time = datetime.now()
        if (User.objects.filter(username=username).exists()):
            return render(request, 'signup.html', {'signup_success': 'exist'})
        else:
            if  password == rpassword:
                user = User.objects.create(first_name='', last_name='', is_staff=1, is_active=1, is_superuser=1, last_login=date_time, date_joined=date_time, password=password, email=email, username=username)
                user.save()
                request.session['username'] = username
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'signup.html', {'signup_success': 'no'})
    return render(request, 'signup.html', {'signup_success': ''})

# @login_required
def index(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        username = User.objects.filter(username=posts)
        user_id = User.objects.get(username=posts).pk
        return render(request, 'index.html', {"username": username, "category" : get_category(), "fav_lists": get_favourite_list(user_id)})
    else:
        return render(request, 'index.html', {'username': '', "category" : get_category()})

def comparison(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        username = User.objects.filter(username=posts) 
        # user_id = User.objects.get(username=posts).pk
        return render(request, 'comparison.html', {"username": username, "category" : get_category()})
    else:
        return render(request, 'comparison.html', {'username': '', "category" : get_category()})

@login_required
def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'login.html', {'login_success': ''})

def discounts(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        username = User.objects.filter(username=posts) 
        # user_id = User.objects.get(username=posts).pk
        return render(request, 'discounts.html', {"username": username, "category" : get_category()})
    else:
        return render(request, 'discounts.html', {'username': '', "category" : get_category()})

@login_required
def favourites(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        username = User.objects.filter(username=posts) 
        # user_id = User.objects.get(username=posts).pk
        return render(request, 'favourites.html', {"username": username, "category" : get_category()})
    else:
        return render(request, 'favourites.html', {'username': '', "category" : get_category()})

@login_required
def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        username = User.objects.filter(username=posts) 
        return render(request, 'profile.html', {"username": username})
    else:
        return render(request, 'profile.html', {'username': ''})