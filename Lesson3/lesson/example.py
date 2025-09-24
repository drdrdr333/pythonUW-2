import os
# usually you will see from peewee import *
import peewee as pw
from loguru import logger
from datetime import date

file = 'personjobdept.db'
if os.path.exists(file):
    os.remove(file)

db = pw.SqliteDatabase(file)


class BaseModel(pw.Model):
    logger.info("allows database to be defined changed) in one place")

    class Meta:
        database = db


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info("notice peewee data type")

    person_name = pw.CharField(primary_key = True, max_length = 30)
    lives_in_town = pw.CharField(max_length = 40)
    nickname = pw.CharField(max_length = 20, null = True)

    logger.info("can add methods too")

    def show(self):
        """ display an instance """
        print(self.person_name, self.lives_in_town, self.nickname)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    job_name = pw.CharField(primary_key = True, max_length = 30)
    start_date = pw.DateField(formats = 'YYYY-MM-DD')
    end_date = pw.DateField(formats = 'YYYY-MM-DD', null = True)

    salary = pw.DecimalField(max_digits = 7, decimal_places = 2)
    person_employed = pw.ForeignKeyField(
        Person, related_name='was_filled_by', null = False)


class Department(BaseModel):
    """
        Defines department, maintains departments
        in which jobs exist, and person tied to those jobs
    """
    dept_number = pw.CharField(primary_key = True, max_length = 4)
    dept_name = pw.CharField(max_length = 30)
    dept_manager = pw.CharField(max_length = 30)
    end_date = pw.DateField(null = True)

def main():
    """ add and print some records """
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    db.create_tables([
        Job,
        Person,
        Department
    ])

    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', None),
        ('Susan', 'Boston', 'Beannie'),
        ('Steven', 'Colchester', None),
        ('Peter', 'Seattle', None),
    ]

    for person in people:
        try:
            with db.transaction():
                new_person = Person.create(
                    person_name = person[0],
                    lives_in_town = person[1],
                    nickname = person[2],)
                new_person.save()

        except Exception as e:
            logger.info(f'Error creating person = {person[0]}')
            logger.info(e)
            logger.info('See how the datbase protects our data')

    for person in Person:
        person.show()

    jobs = [
        ('Analyst', '2017-02-01', '2019-07-31', 34.999, 'Andrew'),
        ('Developer', '2017-02-01', '2019-07-31', 34.999, 'Susan'),
        ('Tester', '2019-11-01', '2019-07-31', 34.999, 'Steven'),
        ('Creator', '2019-11-01', None, 34.999, 'Peter'),
    ]

    for job in jobs:
        try:
            with db.transaction():
                new_job = Job.create(
                    job_name = job[0],
                    start_date = job[1],
                    end_date = job[2],
                    salary = job[3],
                    person_employed = job[4],
                )
                # print(dir(new_job), '/n\n', new_job.start_date)
                new_job.save()

        except Exception as e:
            logger.info(f'Error creating job = {job[0]}')
            logger.info(e)
            logger.info('See how the datbase protects data across tables')

    depts = [
        ('D432', 'Hospitality', 'Greg Newman', ''),
        ('D100', 'Operations', 'Nelly Mingo', ''),
        ('4312', 'Finance', 'Tom Yaris', '')
    ]
    for job in range(len(depts)):
        try:
            with db.transaction():
                if jobs[job][2] is None:
                    new_dept = Department.create(
                        dept_number = depts[job][0],
                        dept_name = depts[job][1],
                        dept_manager = depts[job][2],
                        end_date = None
                    )
                else:
                    end = date.fromisoformat(jobs[job][2])
                    start = date.fromisoformat(jobs[job][1])
                    finish = end - start

                    new_dept = Department.create(
                            dept_number = depts[job][0],
                            dept_name = depts[job][1],
                            dept_manager = depts[job][2],
                            end_date = str(finish.days)
                    )
                new_dept.save()

        except Exception as e:
            logger.info(f"Error creating department - {depts[0]}")
            logger.info(e)

    logger.info("don't forget - but can you find a better way?")
    db.close()


if __name__ == "__main__":
    main()