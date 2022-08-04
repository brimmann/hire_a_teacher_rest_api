import arrow

from jobs.models import Interview

interview_time = Interview.objects.get(id=10).time

formatted = arrow.get(interview_time, "YYYY-MM-DD HH:mm A")


print(formatted.format("dddd, MMMM D, YYYY - hh:mm A"))

