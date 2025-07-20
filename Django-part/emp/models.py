from django.db import models

class employees(models.Model):
    emp_name=models.CharField(max_length=100)
    emp_id=models.CharField(max_length=50, unique=True)
    def __str__(self):
        return str(self.emp_id)
    
class emp_details(models.Model):
    emp_num=models.BigIntegerField()
    emp_email=models.CharField(max_length=50)
    emp_add=models.CharField(max_length=100)
    empid=models.ForeignKey(employees,on_delete=models.CASCADE,to_field='emp_id')
    def __str__(self):
        return str(self.empid)
