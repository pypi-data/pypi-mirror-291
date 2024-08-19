import csv
from prettytable import PrettyTable

from sshc.types import Sequence, Record, Row
from sshc.cipher import AESCipher
from sshc.constants import *
from sshc.utils import *

tab = USER_SSH_CFG_TAB


class ConfigLoader:

    def __init__(self, src=None) -> None:
        makedirs_ex(SSHC_CONFIG_DIR)
        self.src = src or SSHC_TSV
        self.headers = SSHC_TSV_HEADERS
        self.cipher = AESCipher.create_with_password("xQyo8K9Ar4z72R")

    def as_row(self, record: Record) -> Row:
        return [record.get(k, "") for k in self.headers]

    def as_record(self, row: Row) -> Record:
        return {k: v for k, v in zip(self.headers, row)}

    def _encrypt_record(self, record: Record):
        record["Password"] = self.cipher.encrypt(record["Password"])

    def _encrypt_records(self, records: Sequence[Record]):
        for record in records:
            record["Password"] = self.cipher.encrypt(record["Password"])

    def _decrypt_records(self, records: Sequence[Record]):
        for record in records:
            record["Password"] = self.cipher.decrypt(record["Password"])

    def _load_raw(self) -> Sequence[Record]:
        records = []
        if not exists(self.src):
            return self._dump([])
        reader = open(self.src, "r")
        generator = csv.reader(reader, delimiter="\t")
        try:
            next(generator)
        except StopIteration:
            return self._dump([])
        if len(self.headers) == 0:
            return self._dump([])
        for row in generator:
            records.append(self.as_record(row))
        reader.close()
        return records

    def _load_with_table(self):
        records = self._load_raw()
        table = PrettyTable(self.headers)
        return records, table

    def _dump(self, records: Sequence[Record]) -> Sequence[Record]:
        system(f"cp {self.src} {self.src}.{get_now_ts()}")
        file = open(self.src, "w")
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(self.headers)
        rows = [self.as_row(record) for record in records]
        writer.writerows(rows)
        file.close()
        return records

    def make(self, write=False):
        blocks = []
        for r in self._load_raw():
            e = "" if r["Enabled"] == "1" else "# "
            items = [f"{e}Host {r['Host']}"]
            items.append(f"{tab}{e}HostName {r['HostName']}")
            if r["Port"] != "22":
                items.append(f"{tab}{e}Port {r['Port']}")
            items.append(f"{tab}{e}User {r['User']}")
            blocks.append("\n".join(items))
        content = "\n\n".join(blocks)
        if write:
            with open(USER_SSH_CFG, "w") as wt:
                wt.write(content)
            os.chmod(USER_SSH_CFG, 0o600)
        else:
            print(content)

    def print(self, keyword=None):
        records, table = self._load_with_table()
        self._decrypt_records(records)
        if keyword is None:
            rows = [self.as_row(r) for r in records]
        else:
            filter = lambda r: keyword in r["Host"] or keyword in r["Name"]
            rows = [self.as_row(r) for r in records if filter(r)]
        table.add_rows(rows)
        print(table)

    def add_item_interactive(self):
        records, table = self._load_with_table()
        record = {}
        record["Host"] = input("Host Key: ").strip()
        record["HostName"] = input("Host Address: ").strip()
        _ = input("Host Port (default: 22): ").strip()
        record["Port"] = "22" if _ == "" else _
        _ = input("Host User (default: root): ").strip()
        record["User"] = "root" if _ == "" else _
        record["Password"] = input("Password (optional): ").strip()
        record["Name"] = input("Name (optional): ").strip()
        record["Desc"] = input("Description (optional): ").strip()
        _ = input("Enabled? (0/1, default: 1): ").strip()
        record["Enabled"] = "1" if _ == "" else _
        self._encrypt_record(record)
        table.add_row(self.as_row(record))
        self._dump([*records, record])
        print(table)

    def remove_item(self, key: str):
        records, table = self._load_with_table()
        removed_hosts = []
        left_records = []
        for record in records:
            if record["Host"] == key:
                table.add_row(self.as_row(record))
                removed_hosts.append(record["Host"])
            else:
                left_records.append(record)

        success = False
        if len(removed_hosts) == 0:
            print("[ERROR] invalid host keys: %s" % key)
        elif len(removed_hosts) == 1:
            success = True
        else:
            print("[ERROR] multiple matches: " + ", ".join(removed_hosts))

        if success:
            print(table)
            self._dump(left_records)

        return success

    def update(self, key: str, col: str, val):
        records, table = self._load_with_table()

        success = False
        new_records = []
        for record in records:
            if record["Host"] == key:
                success = True
                record[col] = val
                if "col" == "Password":
                    self._encrypt_record(record)
                table.add_row(self.as_row(record))
            new_records.append(record)

        if success:
            print(table)
            self._dump(new_records)

        return success

    def clean_all_backups(self):
        system(f"rm -rf {self.src}.*")

    def open_in_editor(self, fp: str):
        if system(f"code {fp}") == 0:
            return
        if system(f"nano {fp}") == 0:
            return
        if system(f"vim {fp}") == 0:
            return
        if system(f"vi {fp}") == 0:
            return
