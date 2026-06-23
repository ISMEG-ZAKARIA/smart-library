from django.db import migrations


TRIGGERS = ("smart_penalite_integrite_bi", "smart_penalite_integrite_bu")


def supprimer_triggers(schema_editor):
    if schema_editor.connection.vendor != "mysql":
        return
    with schema_editor.connection.cursor() as cursor:
        for nom in TRIGGERS:
            cursor.execute(f"DROP TRIGGER IF EXISTS {nom}")


def installer_triggers(apps, schema_editor):
    if schema_editor.connection.vendor != "mysql":
        return
    supprimer_triggers(schema_editor)
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TRIGGER smart_penalite_integrite_bi
            BEFORE INSERT ON penalties_penalite
            FOR EACH ROW
            BEGIN
                DECLARE role_client VARCHAR(12);
                DECLARE role_createur VARCHAR(12);
                DECLARE client_emprunt BIGINT;

                SELECT role INTO role_client FROM accounts_utilisateur WHERE id = NEW.client_id;
                IF role_client <> 'CLIENT' THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Une penalite doit appartenir a un client';
                END IF;

                IF NEW.creee_par_id IS NOT NULL THEN
                    SELECT role INTO role_createur FROM accounts_utilisateur WHERE id = NEW.creee_par_id;
                    IF role_createur NOT IN ('ADMIN', 'LIBRARIAN') THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Createur de penalite non autorise';
                    END IF;
                END IF;

                IF NEW.emprunt_id IS NOT NULL THEN
                    SELECT client_id INTO client_emprunt FROM loans_emprunt WHERE id = NEW.emprunt_id;
                    IF client_emprunt <> NEW.client_id THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Penalite et emprunt doivent avoir le meme client';
                    END IF;
                END IF;
            END
            """
        )
        cursor.execute(
            """
            CREATE TRIGGER smart_penalite_integrite_bu
            BEFORE UPDATE ON penalties_penalite
            FOR EACH ROW
            BEGIN
                IF OLD.client_id <> NEW.client_id
                   OR NOT (OLD.emprunt_id <=> NEW.emprunt_id)
                   OR NOT (OLD.creee_par_id <=> NEW.creee_par_id) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Relations de penalite immuables';
                END IF;
            END
            """
        )


def desinstaller_triggers(apps, schema_editor):
    supprimer_triggers(schema_editor)


class Migration(migrations.Migration):
    dependencies = [("penalties", "0001_initial")]
    operations = [migrations.RunPython(installer_triggers, desinstaller_triggers)]
