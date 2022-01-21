#!/usr/bin/env python

"""Tests for `sqla2uml` package."""
import importlib

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from sqla2uml.scanner import Scanner

Base = declarative_base()


class Blog(Base):
    __tablename__ = "blog"

    id = sa.Column(sa.Integer, primary_key=True, unique=True, autoincrement=True)

    name = sa.Column(sa.UnicodeText, nullable=False, default="")
    description = sa.Column(sa.UnicodeText, nullable=False, default="")


class BlogPost(Base):
    __tablename__ = "blog_post"

    id = sa.Column(sa.Integer, primary_key=True, unique=True, autoincrement=True)

    title = sa.Column(sa.UnicodeText, nullable=False, default="")
    content = sa.Column(sa.UnicodeText, nullable=False, default="")
    summary = sa.Column(sa.UnicodeText, nullable=False, default="")


# class BlogPostWithPicture(BlogPost):
#     __tablename__ = "blog_post_w_picture"
#
#     picture = sa.Column(sa.LargeBinary)


def test_scanner():
    scanner = Scanner()
    root_module = importlib.import_module("tests")
    scanner.scan(root_module)
