-- Revert wild-db:3-create-tables-retr from pg

BEGIN;

-- XXX Add DDLs here.

DROP TABLE wild.retr_yes_no CASCADE;
DROP TABLE wild.retr_grantor_type CASCADE;
DROP TABLE wild.retr_grantor_grantee_relation CASCADE;
DROP TABLE wild.retr_energy_exclusion CASCADE;
DROP TABLE wild.retr_property_type CASCADE;
DROP TABLE wild.retr_predominate_use CASCADE;
DROP TABLE wild.retr_transfer_type CASCADE;
DROP TABLE wild.retr_owner_interest_transferred CASCADE;
DROP TABLE wild.retr_grantor_rights_retained CASCADE;
DROP TABLE wild.retr_transfer_exemption_number CASCADE;
DROP TABLE wild.retr_financing_code CASCADE;
DROP TABLE wild.retr_conveyance_code CASCADE;
DROP TABLE wild.retr_agent_for CASCADE;

DROP TABLE wild.retr;

COMMIT;
