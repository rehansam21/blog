from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from posts.models import Posts, Demo
from .forms import PostForms
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

try:
    from urllib import quote_plus
except:
    pass
from django.utils import timezone
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.form import CommentForm
from django.contrib.contenttypes.models import ContentType


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)  # which means that the object is
        # created but it's not actually saved to the db which is useful if you want to change some data before actually saving it
        # print form.cleaned_data.get('title')
        instance.save()
        print "Hi inside if_statement"
        messages.success(request, 'Posts Created Successfully')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        print "inside else"
    # messages.error(request, 'Not Created')
    context = {
        "form": form,
    }

    return render(request, 'post_form.html', context)


def post_detail(request, id=None):
    instance = get_object_or_404(Posts, id=id)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    initial_data = {
        "content_type": instance.get_content_type,  # look inside Post model function
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)  # this is comming from model
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        print content_data

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    # comments = Comment.objects.filter_by_instance(instance)
    comments = instance.comments
    context = {
        'obj_detail': instance,
        'title': instance.title,
        'share_string': share_string,
        'comments': comments,
        'form': form,
    }

    return render(request, 'detail.html', context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Posts.objects.active()  # Posts.objects.filter(publish__lte=timezone.now)
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Posts.objects.all()
    query = request.GET.get('query')  # search code starts from here
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    # if request.user.is_authenticated():
    # 	context = {
    # 				'list': 'my logged in user'
    # 	}
    # 	return render(request, 'index.html', context)
    # else:
    # 	context = {
    # 				'list' : 'list'
    # 	}
    context = {
        'obj_list': queryset,
        'today': today,
    }

    return render(request, 'list.html', context)


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Posts, id=id)
    form = PostForms(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)  # whatever the form data is we need to show in front end
        # so,we've saved into some instance & pass it as a context to template.
        instance.save()
        messages.success(request, 'Posts Edited Successfully')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
        'instance': instance,
    }

    return render(request, 'post_form.html', context)


def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Posts, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")


def entry_index(request, template='entry_index.html', page_template='entry_index_page.html'):
    context = {
        'entries': Demo.objects.all(),
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(
        template, context, context_instance=RequestContext(request))
