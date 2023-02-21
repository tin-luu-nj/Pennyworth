import yaml, csv

LOGGING_LEVEL_CRITICAL = 50
LOGGING_LEVEL_ERROR = 40
LOGGING_LEVEL_WARNING = 30
LOGGING_LEVEL_INFO = 20
LOGGING_LEVEL_DEBUG = 10
LOGGING_LEVEL_NOTSET = 0
LOGGING_LEVEL_LIST = [
    LOGGING_LEVEL_CRITICAL,
    LOGGING_LEVEL_ERROR,
    LOGGING_LEVEL_WARNING,
    LOGGING_LEVEL_INFO,
    LOGGING_LEVEL_DEBUG,
    LOGGING_LEVEL_NOTSET,
]
LOG_LEVEL_KEYWORD = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]


def config_generate(cfg: dict):
    for key in cfg:
        if not key == "version":
            with open("./generated/{file}.py".format(file=key.upper()), "w") as stream:
                write_config(cfg, key, stream)


def write_config(public_cfg, cfg_name, stream):
    WRITE = stream.write
    WRITE('CONFIG_VERSION = "{0}"\n\n'.format(public_cfg["version"]))
    for cfg in unnest(public_cfg[cfg_name]):
        left_side = cfg_name.upper()
        right_side = cfg[-1]
        for iid in range(len(cfg) - 1):
            left_side = left_side + "_" + cfg[iid].upper()
        if type(right_side) in [int, float, bool, list] or right_side == "None":
            WRITE("{0} = {1}\n".format(left_side, right_side))
        else:
            WRITE('{0} = "{1}"\n'.format(left_side, right_side))


def unnest(d, keys=[]):
    result = []
    for k, v in d.items():
        if isinstance(v, dict):
            result.extend(unnest(v, keys + [k]))
        else:
            result.append(tuple(keys + [k, v]))
    return result


def load_DTC_csv():
    csv_db = []
    with open("./config/DTC.csv", mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            csv_db.append(row)
            line_count += 1
    return csv_db


def generate_DTC_py(csv_db):
    with open("./pyDiagnostic/DTC.py", "w") as stream:
        WRITE = stream.write

        event_id_list = []
        current_event_status = 0
        for entry in csv_db:
            if not entry["EVENT ID"] in event_id_list:
                event_id_list.append(entry["EVENT ID"])
                current_event_status = 0
            else:
                current_event_status += 1

            DEM_EVENT = "{0}_{1}".format(entry["EVENT ID"], entry["EVENT STATUS"])
            WRITE(
                'DEM_EVENT_{0: <60}= ({2}, {3}, {4}, "{1}")\n'.format(
                    DEM_EVENT,
                    DEM_EVENT,
                    LOGGING_LEVEL_LIST[LOG_LEVEL_KEYWORD.index(entry["LOG LEVEL"])],
                    len(event_id_list),
                    current_event_status,
                )
            )


def main() -> None:
    with open("./config/public_cfg.yml", "r") as stream:
        cfg = yaml.load(stream, Loader=yaml.CLoader)
        config_generate(cfg)

    with open("./config/private_cfg.yml", "r") as stream:
        cfg = yaml.load(stream, Loader=yaml.CLoader)
        config_generate(cfg)

    csv_db = load_DTC_csv()
    generate_DTC_py(csv_db)


if "__main__" == __name__:
    main()
