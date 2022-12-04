-- Revert fmc-db:3-create-tables-retr from pg

BEGIN;

-- XXX Add DDLs here.

DROP TABLE fmc.retr_yes_no CASCADE;
DROP TABLE fmc.retr_grantor_type CASCADE;
DROP TABLE fmc.retr_grantor_grantee_relation CASCADE;
DROP TABLE fmc.retr_energy_exclusion CASCADE;
DROP TABLE fmc.retr_property_type CASCADE;
DROP TABLE fmc.retr_predominate_use CASCADE;
DROP TABLE fmc.retr_transfer_type CASCADE;
DROP TABLE fmc.retr_owner_interest_transferred CASCADE;
DROP TABLE fmc.retr_grantor_rights_retained CASCADE;
DROP TABLE fmc.retr_transfer_exemption_number CASCADE;
DROP TABLE fmc.retr_financing_code CASCADE;
DROP TABLE fmc.retr_conveyance_code CASCADE;
DROP TABLE fmc.retr_agent_for CASCADE;

DROP TABLE fmc.retr;

COMMIT;
