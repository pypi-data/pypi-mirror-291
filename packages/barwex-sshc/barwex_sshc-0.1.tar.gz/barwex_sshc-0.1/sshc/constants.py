import os

USER_HOME_DIR = os.environ.get("HOME")
USER_SSH_DIR = os.path.join(USER_HOME_DIR, ".ssh")
USER_SSH_CFG = os.path.join(USER_SSH_DIR, "config")
USER_SSH_CFG_TAB = " " * 4

SSHC_CONFIG_DIR = os.path.join(USER_HOME_DIR, ".config", "barwex", "sshc")
SSHC_TSV = os.path.join(SSHC_CONFIG_DIR, "sshc.tsv")
SSHC_TSV_HEADERS = ("Enabled", "Name", "Host", "HostName", "Port", "User", "Password", "Desc")
