from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Test(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addTest',
        'del': 'delTest',
        'set': 'setTest',
        'search': 'get',
    }
    API_KEY = 'test'
    API_KEY_1 = 'monit'
    API_MOD = 'monit'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['type', 'condition', 'action', 'path']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'test'
    FIELDS_TYPING = {
        'select': ['type', 'action'],
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.test = {}
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        if self.p['state'] == 'present':
            if self.p['condition'] is None:
                self.m.fail_json(
                    "You need to provide a 'condition' to create a test!"
                )

            if self.p['action'] == 'execute' and self.p['path'] == '':
                self.m.fail_json(
                    "You need to provide the path to a executable to "
                    "create a test of type 'execute'!"
                )

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.test['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def update(self):
        self.b.update(enable_switch=False)
