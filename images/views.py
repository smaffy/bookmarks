import redis

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify

from images.models import Image
from .forms import ImageCreateForm, ImageAddForm, ImageEditForm
from common.decorators import ajax_required
from actions.utils import create_action


# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required
def image_create(request):
    """
    View for creating an Image using the JS Bookmarklet.
    """
    if request.method == 'POST':
        # form sended
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # set user
            new_item.user = request.user
            request.user.profile.rating += 3
            request.user.profile.save()
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)

            messages.success(request, 'Image added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


@login_required
def image_add(request):
    """
    View for simple creating image.
    """
    if request.method == 'POST':
        # form sended
        form = ImageAddForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            new_item = Image(image=request.FILES['image'], user=request.user, title=form.cleaned_data['title'])
            new_item.description = form.cleaned_data['description']
            request.user.profile.rating += 3
            request.user.profile.save()
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)

            messages.success(request, 'Image added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageAddForm()
        return render(request, 'images/image/addnew.html', {'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # views +1
    total_views = r.incr('image:{}:views'.format(image.id))
    # raiting +1 r.zincrby('image_ranking', image.id, 1)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images', 'image': image, 'total_views': total_views})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                request.user.profile.rating += 1
                request.user.profile.save()
                if not request.user == image.user:
                    image.user.profile.rating += 1
                    image.user.profile.save()
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
    images = Image.objects.order_by('-total_likes')
    paginator = Paginator(images, 10)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                  {'section': 'images', 'images': images})


@login_required
def image_delete(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    try:
        image.delete()
        messages.success(request, 'Image deleted.')
        request.user.profile.rating -= 2
        request.user.profile.save()
        return redirect('profile')
    except:
        messages.error(request, 'You can not delete this image.')
        return redirect('images:detail', id=image.id, slug=image.slug)


@login_required
def image_edit(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    if request.user:
        if request.method == 'POST':
            form = ImageEditForm(instance=request.user, data=request.POST, files=request.FILES)

            if form.is_valid():
                form.save()
                messages.success(request, 'Image updated successfully.')
                return redirect('images:detail', id=image.id, slug=image.slug)

            else:
                messages.error(request, 'Error updating your image.')

        else:
            form = ImageEditForm(instance=image)

        return render(request, 'images/image/edit.html', {'form': form, 'image': image})
    else:
        messages.error(request, 'You can not edit this image.')
        return redirect('images:detail', id=image.id, slug=image.slug)



"""
@login_required
def image_ranking(request):
    # get dict of rang img
    image_ranking = r.zrange('image_ranking', 0, 20, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed img
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'section': 'images', 'most_viewed': most_viewed})
"""