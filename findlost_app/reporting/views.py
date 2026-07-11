from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SightingReportForm
from matching.utils import encode_face_from_fieldfile
from matching.engine import run_matching


def home(request):
    """Public landing page."""
    return render(request, 'home.html')


@login_required
def submit_report(request):
    """UC-02: Upload Sighting Report. See Report Section 4.6 and
    Appendix A.3."""
    if request.method == 'POST':
        form = SightingReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()

            encoding = encode_face_from_fieldfile(report.photo)
            if encoding is None:
                form.add_error('photo', 'No face detected in the uploaded image. '
                                         'Please try a clearer photograph.')
                report.photo.delete(save=False)
                report.delete()
                return render(request, 'reporting/submit_report.html', {'form': form})

            report.encoding = encoding.tobytes()
            report.save()

            # UC-04: automatically trigger the matching engine (Sec. 7.1.4)
            matches = run_matching(report)
            return redirect('report_success', report_id=report.id)
    else:
        form = SightingReportForm()
    return render(request, 'reporting/submit_report.html', {'form': form})


@login_required
def report_success(request, report_id):
    return render(request, 'reporting/report_success.html', {'report_id': report_id})
