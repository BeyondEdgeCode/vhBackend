from api.app import ma
from api.models import Category, SubCategory


class SubCategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = SubCategory
        ordered = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(dump_only=True)


class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Category
        include_fk = True

    id = ma.auto_field()
    title = ma.auto_field()

    subcategories = ma.Nested(SubCategorySchema, dump_only=True, many=True)





