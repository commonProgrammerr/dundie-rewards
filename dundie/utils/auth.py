import os
from functools import wraps

from dundie.database import get_session
from dundie.models import Person
from sqlalchemy.orm import selectinload
from sqlmodel import select


class AuthError(Exception):
    pass


def requires_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        email = os.getenv("DUNDIE_USER")
        password = os.getenv("DUNDIE_PASSWORD")

        if not all((email, password)):  # Check if both are set
            raise AuthError("DUNDIE_USER and DUNDIE_PASSWORD must be set")

        with get_session() as session:
            person = session.exec(
                select(Person)
                .options(
                    selectinload(Person.balance),
                    selectinload(Person.user),
                    selectinload(Person.movement),
                )
                .where(Person.email == email)
            ).first()

            if not person:
                raise AuthError("User not found")

            if person.user[0].password != password:
                raise AuthError("Authentication failed!")

        return f(*args, from_person=person, **kwargs)

        # return f(*args, from_person=None, **kwargs)

    return decorator
