from sqlalchemy.orm import registry, mapped_column, Mapped
from sqlalchemy import Integer, String, create_engine

mapper_registry = registry()

@mapper_registry.mapped
class Topic(object):
    __tablename__ = 'topics'

    id = mapped_column(Integer, primary_key=True)
    update_time = mapped_column(String, primary_key=True)

    title: Mapped[str]
    url: Mapped[str]
    create_time: Mapped[str]
    content: Mapped[str]
    author_name: Mapped[str]
    author_id: Mapped[str]
    author_uid: Mapped[str]
    author_url: Mapped[str]
    author_true_url: Mapped[str]
    author_avatar: Mapped[str]

    def to_dict(self):
        return {ele.name:getattr(self,ele.name) for ele in self.__table__.columns}

def get_comment_model(tid):

    class comment_model(object):
        __tablename__ = tid

        reply_id = mapped_column(String,primary_key=True)

        author_name:Mapped[str]
        author_avatar:Mapped[str]
        author_id:Mapped[str]
        author_uid:Mapped[str]
        author_url:Mapped[str]
        author_true_url:Mapped[str]
        author_register_time:Mapped[str]
        reply_text:Mapped[str]
        reply_time:Mapped[str]

        ref_id = mapped_column(String,nullable=True)
        ref_storge = mapped_column(String,nullable=True)
        photo = mapped_column(String,nullable=True)

        def to_dict(self):
            return {ele.name: getattr(self, ele.name) for ele in self.__table__.columns}

    mapper_registry.mapped(comment_model)

    return comment_model



if __name__ == "__main__":
    engine = create_engine('sqlite:///./Experiment.db', echo='debug')
    mapper_registry.metadata.create_all(bind=engine)
