# Generated by Django 4.2.8 on 2023-12-24 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supply_chain', '0002_supplychain_suppliers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplychainlink',
            name='parent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child', to='supply_chain.supplychainlink'),
        ),
        migrations.AlterField(
            model_name='supplychainlink',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='supply_chain.supplier'),
        ),
        migrations.AddConstraint(
            model_name='supplychainlink',
            constraint=models.CheckConstraint(check=models.Q(('level__lte', 4)), name='level__lte__4'),
        ),
        migrations.AddConstraint(
            model_name='supplychainlink',
            constraint=models.UniqueConstraint(fields=('supply_chain', 'supplier'), name='unique_chain_supplier'),
        ),
        migrations.AddConstraint(
            model_name='supplychainlink',
            constraint=models.UniqueConstraint(fields=('supply_chain', 'parent'), name='unique_chain_parent'),
        ),
    ]