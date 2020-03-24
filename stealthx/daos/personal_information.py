from stealthx.models import PersonalInformation
from .base import BaseDAO


class PersonalInformationDAO(BaseDAO):
    def init_personal_info(self, **kwargs):
        obj = self.model(**kwargs)
        self.add_commit_obj(obj)

    def update_personal_info(self, user_id, **kwargs):
        obj = self.model.query.filter_by(user_id=user_id)
        obj.update(kwargs)


personal_info_dao = PersonalInformationDAO(PersonalInformation)
