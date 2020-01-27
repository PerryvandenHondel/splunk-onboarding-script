Definitions







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


JO
SCS; Server Classes

CDA; create_deployment_app_cda
    cda_id
    cda_env_code
    cda_scs_code
    cda_lgf_id
    cda_is_created





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

