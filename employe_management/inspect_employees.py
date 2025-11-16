from user.models import Employee
print([f.name for f in Employee._meta.get_fields()])
e = Employee.objects.first()
print("first record:", e)
print("vars:", vars(e))
print("emp_id:", getattr(e,'emp_id',None))
print("working_status:", getattr(e,'working_status',None))
