from user.models import Employee

for e in Employee.objects.all():
    changed = False

    if not getattr(e, 'emp_id', None):
        e.emp_id = e.username or f"E{e.id}"
        changed = True

    if getattr(e, 'working_status', None) is None:
        e.working_status = True
        changed = True

    if changed:
        e.save()

print("DONE")
