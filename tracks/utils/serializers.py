class TableSerializer:
    """ Make ability serialize data from model """

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ModelSerializer:
    """ Make ability serialize data from model """

    @property
    def serialize(self):
        return self.__dict__
