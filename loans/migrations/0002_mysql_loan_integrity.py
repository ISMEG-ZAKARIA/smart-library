from django.db import migrations


TRIGGERS = (
    "smart_emprunt_integrite_bi",
    "smart_emprunt_stock_ai",
    "smart_emprunt_integrite_bu",
    "smart_emprunt_stock_au",
)


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
            CREATE TRIGGER smart_emprunt_integrite_bi
            BEFORE INSERT ON loans_emprunt
            FOR EACH ROW
            BEGIN
                DECLARE role_client VARCHAR(12);
                DECLARE role_validateur VARCHAR(12);
                DECLARE reservation_client BIGINT;
                DECLARE reservation_livre BIGINT;
                DECLARE reservation_statut VARCHAR(12);

                SELECT role INTO role_client FROM accounts_utilisateur WHERE id = NEW.client_id;
                IF role_client <> 'CLIENT' THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un emprunt doit appartenir a un client';
                END IF;

                IF NEW.valide_par_id IS NOT NULL THEN
                    SELECT role INTO role_validateur FROM accounts_utilisateur WHERE id = NEW.valide_par_id;
                    IF role_validateur NOT IN ('ADMIN', 'LIBRARIAN') THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Validateur emprunt non autorise';
                    END IF;
                END IF;

                IF NEW.reservation_id IS NOT NULL THEN
                    SELECT client_id, livre_id, statut
                    INTO reservation_client, reservation_livre, reservation_statut
                    FROM reservations_reservation WHERE id = NEW.reservation_id;
                    IF reservation_client <> NEW.client_id OR reservation_livre <> NEW.livre_id OR reservation_statut <> 'ACTIVE' THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Reservation incompatible avec emprunt';
                    END IF;
                END IF;
            END
            """
        )
        cursor.execute(
            """
            CREATE TRIGGER smart_emprunt_stock_ai
            AFTER INSERT ON loans_emprunt
            FOR EACH ROW
            BEGIN
                IF NEW.statut IN ('ACTIVE', 'INSPECTION') THEN
                    UPDATE catalog_livre
                    SET stock_disponible = stock_disponible - 1,
                        statut = CASE WHEN stock_disponible - 1 = 0 THEN 'UNAVAILABLE' ELSE statut END,
                        modifie_le = CURRENT_TIMESTAMP(6)
                    WHERE id = NEW.livre_id AND stock_disponible > 0;
                    IF ROW_COUNT() = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuffisant pour creer emprunt';
                    END IF;
                END IF;
            END
            """
        )
        cursor.execute(
            """
            CREATE TRIGGER smart_emprunt_integrite_bu
            BEFORE UPDATE ON loans_emprunt
            FOR EACH ROW
            BEGIN
                IF OLD.client_id <> NEW.client_id OR OLD.livre_id <> NEW.livre_id
                   OR NOT (OLD.reservation_id <=> NEW.reservation_id) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Relations emprunt immuables';
                END IF;
            END
            """
        )
        cursor.execute(
            """
            CREATE TRIGGER smart_emprunt_stock_au
            AFTER UPDATE ON loans_emprunt
            FOR EACH ROW
            BEGIN
                IF OLD.statut <> 'RETURNED' AND NEW.statut = 'RETURNED' THEN
                    UPDATE catalog_livre
                    SET stock_disponible = LEAST(stock_total, stock_disponible + 1),
                        statut = CASE
                            WHEN actif = 0 THEN 'UNAVAILABLE'
                            WHEN statut = 'MAINTENANCE' THEN 'MAINTENANCE'
                            ELSE 'AVAILABLE'
                        END,
                        modifie_le = CURRENT_TIMESTAMP(6)
                    WHERE id = NEW.livre_id;
                END IF;
            END
            """
        )


def desinstaller_triggers(apps, schema_editor):
    supprimer_triggers(schema_editor)


class Migration(migrations.Migration):
    dependencies = [("loans", "0001_initial")]
    operations = [migrations.RunPython(installer_triggers, desinstaller_triggers)]
