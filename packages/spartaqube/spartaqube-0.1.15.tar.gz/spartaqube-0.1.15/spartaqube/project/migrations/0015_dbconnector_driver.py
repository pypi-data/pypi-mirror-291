from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('project','0014_dbconnector_lib_dir')];operations=[migrations.AddField(model_name='dbconnector',name='driver',field=models.CharField(max_length=100,null=True))]