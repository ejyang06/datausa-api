from datausa.database import db
from datausa.attrs.models import Geo
from datausa import cache

from datausa.core.models import BaseModel
from datausa.attrs.consts import STATE, COUNTY, ALL
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData

SCHEMA_NAME = 'dartmouth'
CACHE_KEY = '{}_metadata'.format(SCHEMA_NAME)
metadata = cache.get(CACHE_KEY)
if not metadata:
    metadata = MetaData(schema=SCHEMA_NAME, bind=db.engine)
    metadata.reflect()
    cache.set(CACHE_KEY, metadata)

AutomapBase = automap_base(bind=db.engine, metadata=metadata)


class DartmouthBase(db.Model, BaseModel):
    __abstract__ = True
    __table_args__ = {"schema": SCHEMA_NAME, "extend_existing": True}
    source_title = 'Dartmouth Atlas of Health Care'
    source_link = 'http://www.dartmouthatlas.org'
    source_org = 'Dartmouth College'

    @declared_attr
    def year(cls):
        return db.Column(db.Integer(), primary_key=True)

    @declared_attr
    def geo(cls):
        return db.Column(db.String(), db.ForeignKey(Geo.id), primary_key=True)

    @classmethod
    def get_supported_levels(cls):
        return {"geo": [ALL, STATE, COUNTY]}

    @classmethod
    def geo_filter(cls, level):
        if level == ALL:
            return True
        level_map = {STATE: "040", COUNTY: "050"}
        level_code = level_map[level]
        return cls.geo.startswith(level_code)


# class YgAmiPD(AutomapBase, DartmouthBase):
#     __tablename__ = 'yg_ami_post_discharge'
#     median_moe = 1
#
#
# class YgChfPD(AutomapBase, DartmouthBase):
#     __tablename__ = 'yg_chf_post_discharge'
#     median_moe = 1

#
# class YgMedicalPD(AutomapBase, DartmouthBase):
#     __tablename__ = 'yg_medical_post_discharge'
#     median_moe = 1
#
#
# class YgPneumoniaPD(AutomapBase, DartmouthBase):
#     __tablename__ = 'yg_pneumonia_post_discharge'
#     median_moe = 1


class YgPrimaryCare(AutomapBase, DartmouthBase):
    __tablename__ = 'yg_prim_care_access'
    median_moe = 1


class YgReimbursements(AutomapBase, DartmouthBase):
    __tablename__ = 'yg_reimbursements'
    median_moe = 1


# class YgSurgicalPD(AutomapBase, DartmouthBase):
#     __tablename__ = 'yg_surgical_post_discharge'
#     median_moe = 1


AutomapBase.prepare(db.engine, reflect=False)
