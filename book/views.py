from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm,ChngPass,UsrLogin
from .models import Types,Novel,Series,Movies,Collection,Category
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.core.exceptions import ValidationError
from PyPDF2 import PdfReader
from django.contrib import messages
from django.http import FileResponse
from urllib.parse import quote

##################################### SIGN IN ###########################################################

# def sign_up(request):
#     if request.method == "POST":
#         fm=UserCreationForm(request.POST)
#         if fm.is_valid():
#             fm.save()
#     else:
#         fm=UserCreationForm()
#     return render(request,"login.html", {"form": fm})

def sign_up(request):
    if request.method == "POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,"account created successfully!!")
            fm.save()
    else:
        fm=SignUpForm()
    return render(request,"signin.html", {"form": fm})

##################################### USER LOGIN ###########################################################
def user_login(request):
    if request.method =="POST":
        fm=UsrLogin(request=request, data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
            user=authenticate(username=uname, password=upass)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/book/type/')
    else:
        fm=UsrLogin()
    return render(request,"login.html", {"form": fm})

###################################### TYPE ###########################################################
def type(request):
    types=Types.objects.all()
    return render(request,"type.html", {"types":types})

##################################### ADD TYPE ###########################################################
def add_type(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        desc=request.POST.get('desc')
        img=request.FILES.get('img')

        if not img:
            messages.error(request,"Image not uploaded")
        if img.size>2*1024*1024:
            messages.error(request,"The image size is larger than required")
        valid_type=['image/jpeg','image/jpg']
        if img.content_type not in valid_type:
            messages.error(request,"The file type is not supported")
        
        from PIL import Image
        from io import BytesIO

        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000
        if image.width>max_width or image.height>max_height:
            messages.error(request,f"The dimention should not increase {max_width}*{max_height}")
        img.seek(0)

        Types.objets.create(
            type_name=name,
            type_img=img,
            desc=desc
        )
        return redirect("type")
    return render(request,"add_type.html")

##################################### NOVEL ###########################################################
def novel(request):
    novel=Novel.objects.all()
    return render(request,"novel.html", {"novel":novel})

##################################### ADD NOVEL ###########################################################
def add_novel(request):
    categories = Types.objects.all()
    type=Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        cat_id = request.POST.get("cat")
        type_id = request.POST.get("type")
        desc = request.POST.get("desc")
        img = request.FILES.get("img")

        if not cat_id:
            return render(request,"add_novel.html",{"category": categories,"error": "Please select a category"})
        if not type_id:
            return render(request,"add_novel.html",{"type": type,"error": "Please select a Type"})

        category_obj = get_object_or_404(Types, id=cat_id)
        type_obj = get_object_or_404(Category, id=type_id)

        if not img:
            raise ValidationError("Image not uploaded")
        if img.size>2*1024*1024:
            raise ValidationError("The image size is larger than required")
        valid_type=['image/jpeg','image/jpg']
        if img.content_type not in valid_type:
            raise ValidationError("The file type is not supported")
        
        from PIL import Image
        from io import BytesIO

        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000
        if image.width>max_width or image.height>max_height:
            raise ValidationError(f"The dimention should not increase {max_width}*{max_height}")
        img.seek(0)

        Novel.objects.create(
            name=name,
            cat=category_obj,
            type=type_obj,
            desc=desc,
            img=img
        )
        return redirect("novel")
    return render(request, "add_novel.html", {"category": categories})

##################################### UPDATE NOVEL ###########################################################
def update_novel(request,id):
    details=Novel.objects.filter(id=id).first()
    cat=Types.objects.all()
    type=Category.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        cat=request.POST.get("cat")
        desc=request.POST.get("desc")
        type=request.POST.get("type")
        img=request.FILES.get("img")

        cat_id=Types.objects.get(id=cat)
        type_id=Category.objects.get(id=type)

        if not img:
            raise ValidationError("Image not uploaded")
        if img.size>2*1024*1024:
            raise ValidationError("The image size is larger than required")
        valid_type=['image/jpeg','image/jpg']
        if img.content_type not in valid_type:
            raise ValidationError("The file type is not supported")
        
        from PIL import Image
        from io import BytesIO

        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000
        if image.width>max_width or image.height>max_height:
            raise ValidationError(f"The dimension should not increase {max_width}*{max_height}")
        img.seek(0)
        
        details.name=name
        details.cat=cat_id
        details.type=type_id
        details.desc=desc
        details.img=img
        details.save()
        return redirect("novel")
    return render(request,"update_novel.html",{"details":details, "category":cat, "type":type})

##################################### VIEW NOVEL ###########################################################
def view_novel(request,id):
    details=Novel.objects.get(id=id)
    return render(request,"novel_view.html",{"details":details})

##################################### DELETE NOVEL ###########################################################
def delete_novel(request,id):
    details=Novel.objects.get(id=id)
    details.delete()
    return redirect("novel")

##################################### SERIES ###########################################################
def series(request):
    series=Series.objects.all()
    return render(request,"series.html", {"series":series})

##################################### ADD SERIES ###########################################################
def add_series(request):
    cat=Category.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        cate=request.POST.get("cat")
        desc=request.POST.get("desc")
        img=request.FILES.get("img")

        cat_id=Types.objects.get(id=cate)

        if not img:
            raise ValidationError("Image not Uploaded")
        if img.size>2*1024*1024:
            raise ValidationError("Image size is too big")
        valid_format=['img/jpeg', 'img/jpg']
        if img.content_type not in valid_format:
            raise ValidationError("Image is not in supported format")
        
        from PIL import Image
        from io import BytesIO

        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000

        if image.width>max_width or image.height>max_height:
            raise ValidationError(f"The dimension should not increase {max_width}*{max_height}")
        img.seek(0)

        Series.objects.create(
            name=name,
            cat=cat_id,
            desc=desc,
            img=img
        )
        return redirect("series")
    return render(request,"add_series.html",{'category':cat})
##################################### UPDATE SERIES ###########################################################
def update_series(request,id):
    details=Series.objects.filter(id=id).first()
    cat=Types.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        cat=request.POST.get("cat")
        desc=request.POST.get("desc")
        img=request.FILES.get("img")

        cat_id=Types.objects.get(id=cat)

        if not img:
            raise ValidationError("Image not uploaded")
        if img.size>2*1024*1024:
            raise ValidationError("The image size is larger than required")
        valid_type=['image/jpeg','image/jpg']
        if img.content_type not in valid_type:
            raise ValidationError("The file type is not supported")
        
        from PIL import Image
        from io import BytesIO

        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000
        if image.width>max_width or image.height>max_height:
            raise ValidationError(f"The dimention should not increase {max_width}*{max_height}")
        img.seek(0)
        
        details.name=name
        details.cat=cat_id
        details.desc=desc
        details.img=img
        details.save()
        return redirect("series")
    return render(request,"update_series.html",{"details":details, "category":cat})
##################################### MOVIES ###########################################################
def movies(request):
    movies=Movies.objects.all()
    return render(request,"movies.html", {"movies":movies})

##################################### ADD MOVIES ###########################################################
def add_movies(request):
    cat=Category.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        cate=request.POST.get("cat")
        desc=request.POST.get("desc")
        img=request.FILES.get("img")

        cat_id=Types.objects.get(id=cate)

        if not img:
            raise ValidationError("Image not Uploaded")
        if img.size>2*1024*1024:
            raise ValidationError("Image size is too big")
        valid_format=['img/jpeg', 'img/jpg']
        if img.content_type not in valid_format:
            raise ValidationError("Image is not in supported format")
        
        from PIL import Image
        from io import BytesIO

        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000

        if image.width>max_width or image.height>max_height:
            raise ValidationError(f"The dimension should not increase {max_width}*{max_height}")
        img.seek(0)

        Movies.objects.create(
            name=name,
            cat=cat_id,
            desc=desc,
            img=img
        )
        return redirect("movies")
    return render(request,"add_movies.html",{'category':cat})
##################################### UPDATE MOVIES ###########################################################

##################################### UR OWN ###########################################################
def ur_own(request):
    category=Types.objects.all()

    if request.method == "POST":
        name = request.POST['name']
        category= request.POST['category']
        desc= request.POST['desc']
        img= request.FILES['img']
        pdf= request.FILES['pdf']

        category_obj = Types.objects.get(id=category)

        if not img:
            raise ValidationError("Please upload image")
        if img.size>2*1024*1024:
            raise ValidationError("File size is too big")
        valid_type = ["image/jpeg","image/jpg"]
        if img.content_type not in valid_type:
            raise ValidationError("The file format is not suppoted")
        
        from PIL import Image
        from io import BytesIO
        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000

        if image.width>max_width or image.height>max_height:
            raise ValidationError(f"Image should not exceed the dimention {max_width}*{max_height}")
        
        img.seek(0)

        if not pdf:
            raise ValidationError("Pdf not Uploaded")
        if not pdf.name.lower().endswith(".pdf"):
            raise ValidationError("Invalid")
        if pdf.size>5*1024*1024:
            raise ValidationError("The uploaded pdf is too big")

        try:
            pdf.seek(0)
            pdf_reader=PdfReader(pdf)
            _=pdf_reader.metadata

        except:
            raise ValidationError("Invalid Pdf")
        
        pages=len(pdf_reader.pages)
        max_pages=50
        if pages>max_pages:
            raise ValidationError("Pdf should not exceed more than 50 pages")
        pdf.seek(0)

        my_coll=Collection(
            name = name,
            category=category_obj,
            desc= desc,
            img= img, 
            pdf=pdf
        )

        my_coll.save()
        return redirect("mine_list")
    return render(request,"ur_own.html", {'category': category})

##################################### MINE LIST ###########################################################
def mine_list(request):
    collection=Collection.objects.all()
    return render(request,"mine_list.html", {'collection' : collection})

##################################### MINE LIST UPDATE ###########################################################
def mine_list_update(request, id):
    details=Collection.objects.filter(id=id).first()
    category=Types.objects.all()
    if request.method=='POST':
        name=request.POST.get('name')
        category=request.POST.get('category')
        desc=request.POST.get('desc')
        img=request.FILES.get('img')
        pdf=request.FILES.get('pdf')

        category_id=Types.objects.get(id=category)

        details.name=name
        details.category=category_id
        details.desc=desc
        details.img=img
        details.pdf=pdf

        details.save()
        return redirect("mine_list")
    return render(request,"mine_list_update.html", {"details": details, "category": category})

##################################### MINE LIST DELETE ###########################################################
def mine_list_delete(request, id):
    details=Collection.objects.get(id=id)
    details.delete()
    return redirect("mine_list")

##################################### MINE LIST VIEW ###########################################################
def mine_list_view(request, id):
    details=Collection.objects.filter(id=id).first()
    return render(request, "mine_list_view.html", {"details":details})


##################################### DOWNLOAD OWN COLLECTION PDF ###########################################################
def download_pdf(request, id):
    details = Collection.objects.get(id=id)
    file_path = details.pdf.path
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    
    # Force the browser to use your desired filename
    filename = f"{details.name}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
    return response

##################################### CATEGORY ###########################################################
def category(request):
    categories=Category.objects.all()
    # selected_type=Types.objects.get(id=type_id)
    return render(request, "collection.html", {"categories":categories 
                                            #    , "type":selected_type
                                               })

##################################### ADD CATEGORY ###########################################################
def add_category(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        desc=request.POST.get('desc')
        img=request.FILES.get('img')

        if not img:
            messages.error(request,"Image not uploaded")
            return redirect('add_category')
        if img.size>2*1024*1024:
            messages.error(request,"Image should be less than 2MB")
            return redirect('add_category')
        valid_type = ['image/jpeg', 'image/jpg']
        if img.content_type not in valid_type:
            messages.error(request,"The uploaded format doesnt supported")      
            return redirect('add_category')                           
        
        from PIL import Image
        from io import BytesIO

        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000
        if image.width>max_width or image.height>max_height:
            messages.error(request,f"The file dimension should not exceed {max_width}*{max_height}")
            return redirect('add_category')
        img.seek(0)

        cat=Category(
            name=name,
            desc=desc,
            img=img
        )

        cat.save()
        return redirect('category')
    return render(request, "add_collection.html")

##################################### UPDATE CATEGORY ###########################################################
def update_category(request,id):
    details=Category.objects.filter(id=id).first()

    if request.method=="POST":
        name=request.POST.get('name')
        desc=request.POST.get('desc')
        img=request.FILES.get('img')

        if not img:
            messages.error(request,"Image not uploaded")
            return redirect('update_category',id=id)
        if img.size>2*1024*1024:
            messages.error(request,"Image should be less than 2MB")
            return redirect('update_category',id=id)
        valid_type=['image/jpeg']
        if img.content_type not in valid_type:
            messages.error(request,"The uploaded format doesnt supported")       
            return redirect('update_category',id=id)
    
        from PIL import Image
        from io import BytesIO

        image=Image.open(BytesIO(img.read()))
        max_width=2000
        max_height=2000
        if image.width>max_width or image.height>max_height:
            messages.error(request,f"The file dimension should not exceed {max_width}*{max_height}")
            return redirect('update_category',id=id)
        img.seek(0)

        details.name=name
        details.desc=desc
        details.img=img
        details.save()
        return redirect('category')
    return render(request, "update_collection.html",{'details':details})

##################################### DELETE CATEGORY ###########################################################
def delete_category(request,id):
    details=Category.objects.get(id=id)
    details.delete()
    return redirect("category")

##################################### ITEMS ###########################################################

# def items(request, type_id, category):
#     selected_type = Types.objects.get(id=type_id)

#     if category.lower() == "book":
#         items = Novel.objects.filter(type=selected_type)
#     elif category.lower() == "movie":
#         items = Movies.objects.filter(type=selected_type)
#     elif category.lower() == "series":
#         items = Series.objects.filter(type=selected_type)
#     else:
#         items = []

#     return render(request, "items.html", {
#         "items": items,
#         "type": selected_type,
#         "category": category
#     })

##################################### CHANGE PASSWORD ###########################################################
def change_pass(request):
    if request.method == 'POST':
        fm=ChngPass(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            return redirect("user_login")
    else:        
        fm=ChngPass(user=request.user)
    return render(request,"change_pass.html",{'form':fm})

##################################### LOGOUT ###########################################################
def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")

##################################### FORGET PASSWORD ###########################################################
def forget_password(request):
    if request.method=="POST":
        email=request.POST.get['email']

        if SignUpForm.objects.filter(email=email).exist():
            print("User exist")
        return render(request,"forget_password.html")
    return render(request,"forget_password.html")

##################################### BUYER ###########################################################
def buyer(request):
    category=Category.objects.all()
    type=Types.objects.all()
    item=Novel.objects.all()

    context={
        'category':category,
        'type':type,
        'item':item
    }
    return render(request,"buyer.html",context)