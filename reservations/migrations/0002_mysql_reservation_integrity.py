from django.db import migrations


TRIGGERS = ("smart_reservation_integrite_bi", "smart_reservation_integrite_bu")


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
            CREATE TRIGGER smart_reservation_integrite_bi
            BEFORE INSERT ON reservations_reservation
            FOR EACH ROW
            BEGIN
                DECLARE role_client VARCHAR(12);
                DECLARE livre_actif BOOLEAN;
                DECLARE statut_livre VARCHAR(15);
                DECLARE stock_livre INT;
                DECLARE reservations_actives INT;

                SELECT role INTO role_client FROM accounts_utilisateur WHERE id = NEW.client_id;
                IF role_client <> 'CLIENT' THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Une reservation doit appartenir a un client';
                END IF;

                IF NEW.statut = 'ACTIVE' THEN
                    SELECT actif, statut, stock_disponible
                    INTO livre_actif, statut_livre, stock_livre
                    FROM catalog_livre WHERE id = NEW.livre_id FOR UPDATE;
                    IF livre_actif = 0 OR statut_livre = 'MAINTENANCE' OR stock_livre < 1 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Livre indisponible pour reservation';
                    END IF;
                    SELECT COUNT(*) INTO reservations_actives
                    FROM reservations_reservation
                    WHERE livre_id = NEW.livre_id AND statut = 'ACTIVE' AND verrou_actif = 1;
                    IF reservations_actives >= stock_livre THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock deja entierement reserve';
                    END IF;
                END IF;
            END
            """
        )
        cursor.execute(
            """
            CREATE TRIGGER smart_reservation_integrite_bu
            BEFORE UPDATE ON reservations_reservation
            FOR EACH ROW
            BEGIN
                IF OLD.client_id <> NEW.client_id OR OLD.livre_id <> NEW.livre_id THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Relations de reservation immuables';
                END IF;
            END
            """
        )


def desinstaller_triggers(apps, schema_editor):
    supprimer_triggers(schema_editor)


class Migration(migrations.Migration):
    dependencies = [("reservations", "0001_initial")]
    operations = [migrations.RunPython(installer_triggers, desinstaller_triggers)]
