Definitions







Database
ID; A number as a field type for unique records

Code; A string field type with a code


Tables

ENV; Environments, every Splunk instance gets a environment code of 3 letters

LGF; Log files


ELF; Environment Log File
CREATE TABLE `SPLUNK_ONBOARDING`.`environment_logfile_elf` (
  `elf_code` VARCHAR(16) NOT NULL,
  `elf_env_code` VARCHAR(3) NULL,
  `elf_lgf_id` INT NULL,
  `elf_is_created` INT NULL,
  PRIMARY KEY (`elf_code`));



SCS; Server Classes


