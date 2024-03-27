
WITH grantor_address AS (
  SELECT
    TRIM(
      COALESCE(grantor_street_number::TEXT, '') || ' ' ||
      grantor_address || ' ' ||
      grantor_city || ', ' ||
      grantor_state || ' ' ||
      grantor_zip
    ) address
  FROM wild.retr
),
grantee_address AS (
  SELECT
    TRIM(
      COALESCE(grantee_street_number::TEXT, '') || ' ' ||
      grantee_address || ' ' ||
      grantee_city || ', ' ||
      grantee_state || ' ' ||
      grantee_zip
    ) address
  FROM wild.retr
),
agent_address AS (
  SELECT
    TRIM(
      agent_street || ' ' ||
      agent_address || ' ' ||
      agent_city || ', ' ||
      agent_state || ' ' ||
      agent_zip
    ) address
  FROM wild.retr
),
tax_bill_address AS (
  SELECT
    TRIM(
      tax_bill_street_number || ' ' ||
      tax_bill_address || ' ' ||
      tax_bill_city || ', ' ||
      tax_bill_state || ' ' ||
      tax_bill_zip 
    ) address
  FROM wild.retr
),
distinct_addresses AS (
  SELECT * FROM grantor_address
  UNION
  SELECT * FROM grantee_address
  UNION
  SELECT * FROM agent_address
  UNION
  SELECT * FROM tax_bill_address
)
SELECT * FROM distinct_addresses;
