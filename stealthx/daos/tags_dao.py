from stealthx.models import Tags
from .base import BaseDAO


class TagsDAO(BaseDAO):
    def new(self, tag):
        """
        Create new tag if it doesn't exists
        :param tag: name
        :return tag_obj:
        """
        exist_tag_obj = self.model.query.filter_by(name=tag).first()
        if not exist_tag_obj:
            obj = self.model(name=tag)
            self.add_commit_obj(obj)

            return obj

        return exist_tag_obj


tags_dao = TagsDAO(Tags)
