from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    # if the request method is POST, that means we'are receiving data from the form
    if request.method == 'POST':
        form = PostForm(request.POST)

        # validate if the form fields are filled correctly so the post can finally be saved
        if form.is_valid():
            # save the form information to the post instance
            # "commit=False" tells Django that we do not want to actually save it to the database yet
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            # actually saves the post
            post.save()

            # redirect us to the newly created post detail page
            return redirect('post_detail', pk=post.pk)
            
    # if it's not, that means we just need a new instance for the form (when plus button is clicked for the first time)
    else:
        form = PostForm()
    
    # returns the blank form page in order to add a new post
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    # gets a post which matches the pk passed as a parameter
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        # creates a form with the post instance catched earlier
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        # populates the form with the post instance
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})