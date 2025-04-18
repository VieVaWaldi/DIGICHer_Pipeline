from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import (
    Integer,
    UniqueConstraint,
    ForeignKey,
    ARRAY,
    Float,
)
from sqlalchemy.orm import mapped_column, relationship, Mapped

from datamodels.base import Base


class Source_Type(str, Enum):
    arxiv = "arxiv"
    cordis = "cordis"
    core = "coreacuk"


"""
CORE Tables
"""


class Sources(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[Source_Type] = mapped_column(nullable=False)
    entity_table: Mapped[str] = mapped_column(nullable=False)
    entity_id: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint("source", "entity_table", "entity_id"),)


class People(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    telephone_number: Mapped[str] = mapped_column()

    researchoutputs: Mapped[List["ResearchOutputsPeople"]] = relationship(
        back_populates="person"
    )
    institutions: Mapped[List["InstitutionsPeople"]] = relationship(
        back_populates="person"
    )


class Topics(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    standardised_name: Mapped[str] = mapped_column()
    level: Mapped[int] = mapped_column(nullable=False)

    researchoutputs: Mapped[List["ResearchOutputsTopics"]] = relationship(
        back_populates="topic"
    )
    projects: Mapped[List["ProjectsTopics"]] = relationship(back_populates="topic")


class Weblinks(Base):
    __tablename__ = "weblinks"

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column()

    researchoutputs: Mapped["ResearchOutputsWeblinks"] = relationship(
        back_populates="weblink"
    )
    projects: Mapped[List["ProjectsWeblinks"]] = relationship(back_populates="weblink")


class Dois(Base):
    __tablename__ = "dois"

    id: Mapped[int] = mapped_column(primary_key=True)
    doi: Mapped[str] = mapped_column(unique=True, nullable=False)

    # One to Many references
    publications: Mapped[List["ResearchOutputs"]] = relationship(back_populates="doi")
    project: Mapped["Projects"] = relationship(back_populates="doi")


class ResearchOutputs(Base):
    __tablename__ = "researchoutputs"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_original: Mapped[str] = mapped_column(unique=True, nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    arxiv_id: Mapped[str] = mapped_column()

    doi_id: Mapped[int] = mapped_column(ForeignKey("dois.id"))
    doi: Mapped["Dois"] = relationship(back_populates="publications")

    title: Mapped[str] = mapped_column(nullable=False)
    publication_date: Mapped[datetime] = mapped_column()
    journal: Mapped[str] = mapped_column()
    abstract: Mapped[str] = mapped_column()
    summary: Mapped[str] = mapped_column()
    full_text: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column()

    people: Mapped[List["ResearchOutputsPeople"]] = relationship(
        back_populates="publication"
    )
    topics: Mapped[List["ResearchOutputsTopics"]] = relationship(
        back_populates="publication"
    )
    weblinks: Mapped[List["ResearchOutputsWeblinks"]] = relationship(
        back_populates="publication"
    )
    institutions: Mapped[List["InstitutionsResearchOutputs"]] = relationship(
        back_populates="publication"
    )
    projects: Mapped[List["ProjectsResearchOutputs"]] = relationship(
        back_populates="publication"
    )


class Institutions(Base):
    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    sme: Mapped[bool] = mapped_column()
    address_street: Mapped[str] = mapped_column()
    address_postbox: Mapped[str] = mapped_column()
    address_postalcode: Mapped[str] = mapped_column()
    address_city: Mapped[str] = mapped_column()
    address_country: Mapped[str] = mapped_column()
    address_geolocation: Mapped[list[float]] = mapped_column(
        ARRAY(Float), nullable=True
    )
    url: Mapped[str] = mapped_column()
    short_name: Mapped[str] = mapped_column()
    vat_number: Mapped[str] = mapped_column()

    updated_at: Mapped[datetime] = mapped_column()

    people: Mapped[List["InstitutionsPeople"]] = relationship(
        back_populates="institution"
    )
    researchoutputs: Mapped[List["InstitutionsResearchOutputs"]] = relationship(
        back_populates="institution"
    )
    projects: Mapped[List["ProjectsInstitutions"]] = relationship(
        back_populates="institution"
    )


class FundingProgrammes(Base):
    __tablename__ = "fundingprogrammes"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True, nullable=False)
    title: Mapped[str] = mapped_column()
    short_title: Mapped[str] = mapped_column()
    framework_programme: Mapped[str] = mapped_column()
    pga: Mapped[str] = mapped_column()
    rcn: Mapped[int] = mapped_column(Integer)

    projects: Mapped[List["ProjectsFundingProgrammes"]] = relationship(
        back_populates="fundingprogramme"
    )


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_original: Mapped[str] = mapped_column(unique=True, nullable=False)
    doi_id: Mapped[int] = mapped_column(ForeignKey("dois.id"), unique=True)
    acronym: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column()
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()
    ec_signature_date: Mapped[datetime] = mapped_column()
    total_cost: Mapped[int] = mapped_column()
    ec_max_contribution: Mapped[int] = mapped_column()
    objective: Mapped[str] = mapped_column()
    call_identifier: Mapped[str] = mapped_column()
    call_title: Mapped[str] = mapped_column()
    call_rcn: Mapped[str] = mapped_column()

    # One to One
    doi: Mapped["Dois"] = relationship(back_populates="project")

    # Many to Many
    topics: Mapped[List["ProjectsTopics"]] = relationship(back_populates="project")
    weblinks: Mapped[List["ProjectsWeblinks"]] = relationship(back_populates="project")
    researchoutputs: Mapped[List["ProjectsResearchOutputs"]] = relationship(
        back_populates="project"
    )
    institutions: Mapped[List["ProjectsInstitutions"]] = relationship(
        back_populates="project"
    )
    fundingprogrammes: Mapped[List["ProjectsFundingProgrammes"]] = relationship(
        back_populates="project"
    )


"""
JUNCTION Tables --- Publications
"""


class ResearchOutputsPeople(Base):
    __tablename__ = "researchoutputs_people"

    publication_id: Mapped[int] = mapped_column(
        ForeignKey("researchoutputs.id", ondelete="CASCADE"), primary_key=True
    )
    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"), primary_key=True
    )
    person_position: Mapped[int] = mapped_column(nullable=False)

    publication: Mapped["ResearchOutputs"] = relationship(back_populates="people")
    person: Mapped["People"] = relationship(back_populates="researchoutputs")


class ResearchOutputsTopics(Base):
    __tablename__ = "researchoutputs_topics"

    publication_id = mapped_column(
        Integer, ForeignKey("researchoutputs.id", ondelete="CASCADE"), primary_key=True
    )
    topic_id = mapped_column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True
    )

    publication: Mapped["ResearchOutputs"] = relationship(back_populates="topics")
    topic: Mapped["Topics"] = relationship(back_populates="researchoutputs")


class ResearchOutputsWeblinks(Base):
    __tablename__ = "researchoutputs_weblinks"

    publication_id = mapped_column(
        Integer, ForeignKey("researchoutputs.id", ondelete="CASCADE"), primary_key=True
    )
    weblink_id = mapped_column(
        Integer, ForeignKey("weblinks.id", ondelete="CASCADE"), primary_key=True
    )

    publication: Mapped["ResearchOutputs"] = relationship(back_populates="weblinks")
    weblink: Mapped["Weblinks"] = relationship(back_populates="researchoutputs")


"""
JUNCTION Tables --- Institutions
"""


class InstitutionsPeople(Base):
    __tablename__ = "institutions_people"

    institution_id = mapped_column(
        Integer, ForeignKey("institutions.id", ondelete="CASCADE"), primary_key=True
    )
    person_id = mapped_column(
        Integer, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True
    )

    institution: Mapped["Institutions"] = relationship(back_populates="people")
    person: Mapped["People"] = relationship(back_populates="institutions")


class InstitutionsResearchOutputs(Base):
    __tablename__ = "institutions_researchoutputs"

    institution_id = mapped_column(
        Integer, ForeignKey("institutions.id", ondelete="CASCADE"), primary_key=True
    )
    publication_id = mapped_column(
        Integer, ForeignKey("researchoutputs.id", ondelete="CASCADE"), primary_key=True
    )

    institution: Mapped["Institutions"] = relationship(back_populates="researchoutputs")
    publication: Mapped["ResearchOutputs"] = relationship(back_populates="institutions")


"""
JUNCTION Tables --- Projects
"""


class ProjectsTopics(Base):
    __tablename__ = "projects_topics"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True
    )

    project: Mapped["Projects"] = relationship(back_populates="topics")
    topic: Mapped["Topics"] = relationship(back_populates="projects")


class ProjectsWeblinks(Base):
    __tablename__ = "projects_weblinks"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    weblink_id: Mapped[int] = mapped_column(
        ForeignKey("weblinks.id", ondelete="CASCADE"), primary_key=True
    )

    project: Mapped["Projects"] = relationship(back_populates="weblinks")
    weblink: Mapped["Weblinks"] = relationship(back_populates="projects")


class ProjectsResearchOutputs(Base):
    __tablename__ = "projects_researchoutputs"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    publication_id: Mapped[int] = mapped_column(
        ForeignKey("researchoutputs.id", ondelete="CASCADE"), primary_key=True
    )

    project: Mapped["Projects"] = relationship(back_populates="researchoutputs")
    publication: Mapped["ResearchOutputs"] = relationship(back_populates="projects")


class ProjectsInstitutions(Base):
    __tablename__ = "projects_institutions"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institutions.id", ondelete="CASCADE"), primary_key=True
    )
    institution_position: Mapped[int] = mapped_column()
    ec_contribution: Mapped[int] = mapped_column()
    net_ec_contribution: Mapped[int] = mapped_column()
    total_cost: Mapped[int] = mapped_column()
    type: Mapped[str] = mapped_column()
    organization_id: Mapped[str] = mapped_column()
    rcn: Mapped[int] = mapped_column()

    project: Mapped["Projects"] = relationship(back_populates="institutions")
    institution: Mapped["Institutions"] = relationship(back_populates="projects")


class ProjectsFundingProgrammes(Base):
    __tablename__ = "projects_fundingprogrammes"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    fundingprogramme_id: Mapped[int] = mapped_column(
        ForeignKey("fundingprogrammes.id", ondelete="CASCADE"), primary_key=True
    )

    project: Mapped["Projects"] = relationship(back_populates="fundingprogrammes")
    fundingprogramme: Mapped["FundingProgrammes"] = relationship(
        back_populates="projects"
    )
