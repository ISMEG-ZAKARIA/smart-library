from django.db import migrations, models


def rendre_les_livres_actifs_visibles(apps, schema_editor):
    Livre = apps.get_model("catalog", "Livre")
    Livre.objects.filter(actif=True).update(visible_client=True)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="livre",
            name="visible_client",
            field=models.BooleanField(
                db_index=True,
                default=True,
                help_text="Visible dans le catalogue client par défaut ; décochez uniquement pour un ouvrage interne.",
            ),
        ),
        migrations.RunPython(rendre_les_livres_actifs_visibles, migrations.RunPython.noop),
    ]
