-- Deploy fmc-db:3-create-tables-retr to pg
-- requires: 1-create-schema-fmc

BEGIN;

-- XXX Add DDLs here.


CREATE TABLE IF NOT EXISTS fmc.retr (
    sale_number TEXT PRIMARY KEY,
    year_captured TEXT,
    grantor_type SMALLINT,
    grantor_grantee_relation SMALLINT,
    weather_standards SMALLINT, -- yn
    energy_exclusion SMALLINT DEFAULT 11,
    section TEXT,
    township TEXT,
    range TEXT,
    property_type SMALLINT,
    predominate_use SMALLINT,
    multi_family_unit SMALLINT,
    agr_owner_lt_5_years SMALLINT DEFAULT 2, -- yn
    total_acres SMALLINT,
    water_front_indicator SMALLINT DEFAULT 2, -- yn
    transfer_type SMALLINT,
    owner_interest_transferred SMALLINT,
    grantor_rights_retained SMALLINT,
    personal_prop_value_excluded MONEY,
    personal_prop_value_exempt MONEY,
    total_real_estate_value MONEY,
    tansfer_fee MONEY,
    transfer_exemption_number TEXT,
    financing_code SMALLINT,
    document_number TEXT,
    date_recorded DATE,
    date_conveyed DATE,
    deed_date DATE,
    conveyance_code SMALLINT,
    parcel_identification TEXT, -- (Municipal Parcel Number) LET'S GO!
    multi_grantors SMALLINT DEFAULT 2, -- yn
    grantor_last_name TEXT,
    grantor_first_name TEXT,
    grantor_street_number TEXT,
    grantor_address TEXT,
    grantor_city TEXT,
    grantor_state TEXT,
    grantor_zip TEXT,
    certification_date DATE,
    multi_grantees SMALLINT DEFAULT 2, -- yn
    grantee_last_name TEXT,
    grantee_first_name TEXT,
    grantee_street_number TEXT,
    grantee_address TEXT,
    grantee_city TEXT,
    grantee_state TEXT,
    grantee_zip TEXT,
    grantee_certification_date DATE,
    grantee_primary_residence SMALLINT DEFAULT 2, -- yn
    tax_bill_grantee SMALLINT DEFAULT 2, -- yn
    city_yn SMALLINT DEFAULT 2, -- yn
    village_yn SMALLINT DEFAULT 2, -- yn
    town_yn SMALLINT DEFAULT 2, -- yn
    tvc_name TEXT, -- (city, village, town)
    county_name TEXT,
    property_address TEXT,
    lot_size_1 SMALLINT,
    lot_size SMALLINT,
    managed_forest_land_acres SMALLINT,
    volume_jacket TEXT,
    page_image TEXT,
    split_parcel SMALLINT DEFAULT 2, -- yn
    agent_for TEXT,
    agent_name TEXT,
    agent_street TEXT,
    agent_address TEXT,
    agent_city TEXT,
    agent_state TEXT,
    agent_zip TEXT,
    preparer_name TEXT,
    grantor_type_other_note TEXT,
    grantor_grantee_relation_other TEXT,
    tax_bill_name TEXT,
    tax_bill_street_number TEXT,
    tax_bill_address TEXT,
    tax_bill_city TEXT,
    tax_bill_state TEXT,
    tax_bill_zip TEXT,
    w12_document_number TEXT,
    property_type_other_note TEXT,
    misc_use_note TEXT,
    transer_type_other_note TEXT,
    owner_interest_other_note TEXT,
    grantor_rights_other_note TEXT,
    previous_document_number TEXT,
    conveyance_code_other_note TEXT,
    misc_county_tvc TEXT,
    multi_tvcs SMALLINT DEFAULT 2, -- yn
    water_front_feet SMALLINT
);

COMMENT ON TABLE fmc.retr IS 'RETR (Real Estate Transfer Return) data available from https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx#hist';

CREATE TABLE IF NOT EXISTS fmc.retr_yes_no (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_grantor_type (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_grantor_grantee_relation (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_energy_exclusion (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_property_type (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_predominate_use (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_transfer_type (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_owner_interest_transferred (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_grantor_rights_retained (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_transfer_exemption_number (
    id TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_financing_code (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_conveyance_code (
    id SMALLINT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS fmc.retr_agent_for (
    id TEXT PRIMARY KEY,
    value TEXT
);


INSERT INTO fmc.retr_yes_no VALUES
    (1, 'Yes'),
    (2, 'No');

INSERT INTO fmc.retr_grantor_type VALUES
    (1, 'Individual'),
    (2, 'Partnership'),
    (3, 'Corporation'),
    (4, 'Limited liability co, trust, other');

INSERT INTO fmc.retr_grantor_grantee_relation VALUES
    (1, 'None'),
    (2, 'Financial'),
    (3, 'Partnership'),
    (4, 'Family'),
    (5, 'Corp-sharehold-subsidiary'),
    (6, 'Other');

INSERT INTO fmc.retr_energy_exclusion VALUES
    (0, 'Other'),
    (1, 'Owner Occupancy'),
    (2, 'Transfer Fee Exempt'),
    (3, 'Transfer Fee Exempt'),
    (4, 'Seasonal Use'),
    (5, 'Licensed Facilities'),
    (6, 'Bankruptcy'),
    (7, 'Non-Residential'),
    (8, 'Energy Code Compliant'),
    (9, 'No Majority Interest Change'),
    (11, 'Other'),
    (12, 'Pre-Existing Certificate of Compliance'),
    (13, 'Condo Exclusion');

INSERT INTO fmc.retr_property_type VALUES
    (1, 'Land Only'),
    (2, 'Land & Buildings'),
    (3, 'Condominium'),
    (4, 'Other');

INSERT INTO fmc.retr_predominate_use VALUES
    (1, 'Res Single family, (multi=<3), time share'),
    (2, 'Commercial & multi=>4'),
    (3, 'Mfg & telco'),
    (4, 'Agricultural'),
    (5, 'Utility & Misc.'),
    (6, 'Forest Land'),
    (7, 'Other (property classification for tax assessment completed by Co. or Local Official)');

INSERT INTO fmc.retr_transfer_type VALUES
    (1, 'Original sale'),
    (2, 'Gift'),
    (3, 'Exchange'),
    (4, 'Deed in satisfaction of land contract'),
    (5, 'Other');

INSERT INTO fmc.retr_owner_interest_transferred VALUES
    (1, 'Full'),
    (2, 'Partial'),
    (3, 'Other');

INSERT INTO fmc.retr_grantor_rights_retained VALUES
    (1, 'None'),
    (2, 'Life estate'),
    (3, 'Easement'),
    (4, 'Other');

INSERT INTO fmc.retr_transfer_exemption_number VALUES
    ('1', 'Prior to the effective date of this subchapter (October 1, 1969)'),
    ('2', 'From the United States or from this state or from any instrumentality, agency or subdivision of either'),
    ('2G', 'By gift, to the United States or to this state or to any instrumentality, agency or subdivision of either'),
    ('2R', 'Under state law (sec.236.29(1) or (2) or 236.34(1)(c, Wis. Stats.), or for the purpose of a road, street or highway, to the United States or to this state or to any instrumentality, agency or subdivision of either'),
    ('3', 'Which, executed for nominal, inadequate or no consideration, confirms, corrects or reforms a conveyance previously recorded'),
    ('4', 'On sale for delinquent taxes or assessments'),
    ('5', 'On partition (means the division among several persons of real property including noncontiguous real property that belongs to them as co-owners. See state law (sec77.21 (1k), Wis. Stats.)'),
    ('6', 'Pursuant to mergers of entities. "Mergers of entities" means the merger or combination of two or more corporations, non-stock corporations, limited liability companies, limited partnerships, or other entities, or any combination thereof, under a plan of merger or a plan of consolidation permitted by the laws that govern the entities'),
    ('6D', 'Pursuant to partnerships filing or cancelling a statement of qualification under state law (sec. 178.0901, Wis. Stats.) or a corresponding statement under the law of another jurisdiction'),
    ('6M', 'Pursuant to the conversion of a business entity to another form of business entity under state law (sec.178.1141, 179.76, 180.1161, 181.1161, or 183.1207, Wis. Stats.) if after the conversion, the ownership interests in the new entity are identical with the ownership interests in the original entity immediately preceding the conversion'),
    ('6Q', 'Pursuant to an interest exchange under state law (sec. 178.1131, Wis. Stats.)'),
    ('6T', 'Pursuant to a domestication under state law (sec. 178.1151, Wis. Stats.)'),
    ('7', 'By a subsidiary corporation to its parent for no consideration, nominal consideration or in sole consideration or cancellation, surrender or transfer of capital stock between parent and subsidiary corporation'),
    ('8', 'Between parent and child, stepparent and stepchild, parent and son-in-law or daughter-in- law for nominal or no consideration'),
    ('8M', 'Between spouse and spouse (effective September 1, 1996)'),
    ('8N', 'Between an individual and his or her domestic partner under Ch. 770'),
    ('9', 'Between agent and principal or from a trustee to a beneficiary without actual consideration'),
    ('10', 'Solely in order to provide or release security for a debt'),
    ('10M', 'Solely to designate a TOD beneficiary under state law (sec. 705.15, Wis. Stats.)'),
    ('11', 'By will, descent or survivorship'),
    ('11M', 'By non-probate transfer on death under state law (sec. 705.15, Wis. Stats.)'),
    ('12', 'Pursuant to or in lieu of condemnation'),
    ('13', 'Of real estate having a value of $100 or less'),
    ('14', 'Under a foreclosure or a deed in lieu of a foreclosure to a person holding a mortgage or to a seller under a land contract'),
    ('15', 'Between a corporation and its shareholders if all of the stock is owned by persons who are related to each other as spouses, lineal ascendants, lineal descendants or siblings, whether by blood or by adoption, or as spouses of siblings, if the transfer is for no consideration except the assumption of debt or stock of the corporation and if the corporation owned the property for at least three years'),
    ('15M', 'Between a partnership and one or more partners if all of the partners are related to each other as spouses, lineal ascendants, lineal descendants or siblings, whether by blood or by adoption, or as spouses of siblings and if the transfer is for no consideration other than the assumption of debt or an interest in the partnership (effective July 1, 1992)'),
    ('15S', 'Between a limited liability company and one or more of its members if all the members are related to each other as spouses, lineal ascendants, lineal descendants or siblings, whether by blood or by adoption, or as spouses of siblings and if the transfer is for no consideration other than the assumption of debt or an interest in the limited liability company (effective January 1, 1994)'),
    ('16', 'To a trust if a transfer from the grantor to the beneficiary of the trust would be exempt under this section'),
    ('17', 'Of a deed executed in fulfillment of a land contract if the proper fee was paid when the land contract or an instrument evidencing the land contract was recorded'),
    ('20', 'Made under state law ( s ec .184.15, W is . Stats . )'),
    ('21', 'Of transmission facilities or land rights to the transmission company, as defined in state law sec. 196.485(1)(ge), sec. 196.485(5)(b) or (c) or (6)(a)1, Wis. Stats.), in as defined in sec. 196.485(1)(fe), Wis. Stats');

INSERT INTO fmc.retr_financing_code VALUES
    (1, 'Financial Institution-Conventional'),
    (2, 'Financial Institution- Gov.'),
    (3, 'Obtained From Seller'),
    (4, 'Assumed Existing Financing'),
    (5, 'Other 3rd Party Financing'),
    (6, 'No Financing Involved');

INSERT INTO fmc.retr_conveyance_code VALUES
    (1, 'Warranty Deed'),
    (2, 'Land contract'),
    (3, 'Quit Claim Deed'),
    (4, 'Other');

INSERT INTO fmc.retr_agent_for VALUES
    ('R', 'Grantor'),
    ('E', 'Grantee'),
    ('B', 'Both');


DO $$
DECLARE
    colname TEXT;
BEGIN
    FOREACH colname IN ARRAY ARRAY[
        'weather_standards',
        'agr_owner_lt_5_years',
        'water_front_indicator',
        'multi_grantors',
        'multi_grantees',
        'grantee_primary_residence',
        'tax_bill_grantee',
        'city_yn',
        'village_yn',
        'town_yn',
        'split_parcel',
        'multi_tvcs'
    ]
    LOOP
        EXECUTE FORMAT (
            'ALTER TABLE fmc.retr ADD CONSTRAINT retr_%I_fkey
            FOREIGN KEY (%I) REFERENCES fmc.retr_yes_no (id)',
            colname, colname
        );
    END LOOP;

    FOREACH colname IN ARRAY ARRAY[
        'grantor_type',
        'grantor_grantee_relation',
        'energy_exclusion',
        'property_type',
        'predominate_use',
        'transfer_type',
        'owner_interest_transferred',
        'grantor_rights_retained',
        'transfer_exemption_number',
        'financing_code',
        'conveyance_code',
        'agent_for'
    ]
    LOOP
        EXECUTE FORMAT (
            'ALTER TABLE fmc.retr ADD CONSTRAINT retr_%I_fkey
            FOREIGN KEY (%I) REFERENCES fmc.retr_%I (id)',
            colname, colname, colname
        );
    END LOOP;
END $$;

COMMIT;
