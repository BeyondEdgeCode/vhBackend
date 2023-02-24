from api.app import db
from apifairy import body, response
from .schema import SpecificationSchema, SpecificationValuesSchema,\
    SpecificationFullSchema, SpecificationToProductSchema
from flask_jwt_extended import jwt_required
from api.utils import permission_required
from api.models import Specification, SpecificationValue, SpecificationToProduct


@jwt_required()
@permission_required('admin.specifications.add')
@body(SpecificationSchema)
@response(SpecificationSchema)
def create_specification(data):
    spec = Specification(**data)
    db.session.add(spec)
    db.session.commit()
    return spec


@jwt_required()
@permission_required('admin.specifications.add')
@body(SpecificationValuesSchema)
@response(SpecificationValuesSchema)
def create_spec_value(data):
    spec_value = SpecificationValue(**data)
    db.session.add(spec_value)
    db.session.commit()
    return spec_value


@jwt_required()
@permission_required('admin.specifications.assign')
@body(SpecificationToProductSchema)
@response(SpecificationToProductSchema)
def assign_spec_to_product(data):
    spec_to_product = SpecificationToProduct(**data)
    db.session.add(spec_to_product)
    db.session.commit()
    return spec_to_product


@response(SpecificationSchema(many=True))
def get_all_specifications():
    all_specs = db.session.scalars(Specification.select())
    return all_specs
