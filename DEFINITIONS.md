Definitions





TA Technical Add-ons installed on: 
    Index servers
    Deployment Clients

    indexes.conf
    props.conf
    serverclass.conf

SA Search Apps installed on:
    Search Head servers
    





Database Field Definitons
ID; A number as a field type for unique records

Code; A string field type with a code





Table Definitions



ENV; Environments, every Splunk instance gets a environment code of 3 letters
    env_code
    env_description
    env_directory_da
    env_directory_ma
    env_directory_sa



LGF; Log files
    lgf_id
    lgf_path
    lgf_sourcetype



ELF; Environment Log File
CREATE TABLE `SPLUNK_ONBOARDING`.`environment_logfile_elf` (
  `elf_code` VARCHAR(16) NOT NULL,
  `elf_env_code` VARCHAR(3) NULL,
  `elf_lgf_id` INT NULL,
  `elf_is_created` INT NULL,
  PRIMARY KEY (`elf_code`));



IDX index_idx
    idx_id
    idx_env_code
    idx_name



SCS; Server Classes



CDA; create_deployment_app_cda
    cda_id
    cda_env_code
    cda_scs_code
    cda_lgf_id
    cda_is_created


CSC CREATE_SERVER_CLASS_CSC
    csc_id              INT
    csc_env_code        CHAR(3)
    csc_scs_code        CHAR(12)
    csc_is_created      INT         1=TRUE; 0=FALSE
    csc_rcd             DATETIME    CURRENT_TIMESTAMP


CNI CONGIGURATION_ITEM_CNI
    cni_code            CHAR(12)
    cni_description     CHAR(72)
    cni_cmdb_ci         CHAR(32)            Code in the Companies CMDB system



CTA CREATE_TECHNICAL_ADDON_CTA
    cta_id              INT
    cta_env_code        CHAR(3)
    cta_cni_code        CHAR(12)
    cta_is_created      INT         1=TRUE; 0=FALSE



Views
view_create_deployment_app
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `SPLUNK_ONBOARDING`.`view_create_new_da` AS
    SELECT 
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_id` AS `lgf_id`,
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_path` AS `lgf_path`,
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_env_code` AS `lgf_env_code`,
        `SPLUNK_ONBOARDING`.`environment_env`.`env_description` AS `env_description`,
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_sourcetype` AS `lgf_sourcetype`,
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_created` AS `lgf_created`,
        `SPLUNK_ONBOARDING`.`environment_env`.`env_directory_da` AS `env_directory_da`
    FROM
        (`SPLUNK_ONBOARDING`.`logfile_lgf`
        JOIN `SPLUNK_ONBOARDING`.`environment_env` ON ((`SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_env_code` = `SPLUNK_ONBOARDING`.`environment_env`.`env_code`)))
    WHERR cda_is_created=0


CREATE VIEW `view_create_server_class` AS
	SELECT
		csc_id,
        csc_env_code,
        csc_scs_code,
        csc_is_created
	FROM
		create_server_class_csc
	JOIN
		environment_env ON csc_env_code=env_code
	WHERE
		csc_is_create=0





INPUTS.CONF Example

[monitor:///var/log/syslog]
disabled = false
sourcetype = syslog
index = idxe_sandbox