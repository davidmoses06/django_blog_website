from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,Http404
from django.urls import reverse
import logging
from .models import Post
from django.core.paginator import Paginator
from .forms import ContactForm
from .models import AboutUs


# Static Demo Data
# posts=[
#         {'id':1,'title': 'post1','content': 'content of post1'},
#         {'id':2,'title': 'post2','content': 'content of post2'},
#         {'id':3,'title': 'post3','content': 'content of post3'},
#         {'id':4,'title': 'post4','content': 'content of post4'},
        
#     ]

# Create your views here.
def index(request):
    blog_title="Latest Posts"
    # Getting Data From Post models
    all_posts=Post.objects.all()
    # Paginate
    paginator=Paginator(all_posts,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request,'index.html',{'blog_title':blog_title,'page_obj':page_obj})
def details(request,slug):
    # Static Data
    # post= next((item for item in posts if item['id']==post_id),None)
    try:
        # Getting Data form model by post Id
        post = Post.objects.get(slug=slug)
        related_posts=Post.objects.filter(category=post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404("Post doesnot exist")
    # 
    # logger.debug(f'post variable is {post}')
    return render(request,'detail.html',{'post':post,'related_posts':related_posts})
def old_url_redirect(request):
    return redirect(reverse("blog_app:new_page_url"))
def new_url_view(request):
    return HttpResponse("This is the new url")

def contact_view(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        logger=logging.getLogger('TESTING')
        if form.is_valid():
            
            logger.debug(f'POST data is {form.cleaned_data['name']}{form.cleaned_data['email']} {form.cleaned_data['message']}')
            success_message="your form is submitted"
            # send email or save in database
        else:
          
          logger.debug("form validation failure")
        return render(request,'contact.html',{'form':form,'success_message':success_message})
            
    return render(request,'contact.html')

def about(request):
    about_content= AboutUs.objects.first().content
    return render(request,'about.html',{'about_content':about_content})

