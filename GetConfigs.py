import yaml


class GetConfigs:
    def __init__(self, path):
        self.receiver = None
        self.subject = None
        self.text_plain = None
        self.text_html = None
        self.attachment = None

        self._set_fields(self._read_configs(path))

    def _read_configs(self, path):
        with open(path, "r") as config:
            try:
                return yaml.safe_load(config)
            except yaml.YAMLError as e:
                print(e)

    def _set_fields(self, configs: dict):
        cfgs = configs
        self.receiver = cfgs.get('receiver')
        self.subject = cfgs.get('subject')
        self.text_plain = cfgs.get("text-plain")
        self.text_html = cfgs.get("text-html")
        self.attachment = cfgs.get("attachment")
