from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MissingPersonForm
from .models import MissingPerson
from matching.utils import encode_face_from_fieldfile


@login_required
def register_person(request):
    """UC-01: Register Missing Person. See Report Section 4.6."""
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save(commit=False)
            person.reported_by = request.user
            person.save()

            encoding = encode_face_from_fieldfile(person.photo)
            if encoding is None:
                form.add_error('photo', 'No face could be detected in this photo. '
                                         'Please upload a clear, front-facing photograph.')
                person.photo.delete(save=False)
                person.delete()
                return render(request, 'registry/register_person.html', {'form': form})

            person.encoding = encoding.tobytes()
            person.save()
            return redirect('register_success', person_id=person.id)
    else:
        form = MissingPersonForm()
    return render(request, 'registry/register_person.html', {'form': form})


@login_required
def register_success(request, person_id):
    person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
    return render(request, 'registry/register_success.html', {'person': person})


@login_required
def case_dashboard(request):
    """UC-03: View Status."""
    cases = MissingPerson.objects.filter(reported_by=request.user)
    return render(request, 'registry/case_dashboard.html', {'cases': cases})


@login_required
def case_detail(request, person_id):
    person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
    return render(request, 'registry/case_detail.html', {'person': person})
